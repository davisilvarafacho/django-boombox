from django.utils import timezone

from rest_framework.exceptions import ValidationError

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import pkcs12


class CertificadoDigital:
    def __init__(self, arquivo, senha, cnpj):
        self.arquivo = arquivo
        self.cnpj = cnpj
        self.senha = senha.encode()
        self.private_key = None
        self.certificado = None
        self.valido_ate = None
        self._carregar_certificado()

    def _carregar_certificado(self):
        try:
            pfx_data = self.arquivo.read()
            pfx = pkcs12.load_key_and_certificates(pfx_data, self.senha, backend=default_backend())

            self.private_key, self.certificado, _ = pfx
            self.valido_ate = self.certificado.not_valid_after
        except Exception as e:
            if str(e) == "Invalid password or PKCS12 data":
                raise ValidationError({"mensagem": "A senha do certificado é inválida"})
            else:
                raise ValueError(f"Erro ao carregar o arquivo PFX: {e}")
    
    def validar(self):    
        now = timezone.now()

        not_after = self.certificado.not_valid_after
        not_before = self.certificado.not_valid_before

        if now < not_before:
            raise ValidationError({"mensagem": "O certificado ainda não é válido"})
        elif now > not_after:
            raise ValidationError({"mensagem": "O certificado expirou"})
        
        dados = self.extrair_dados()
        cnpj_certificado = dados["subject"].split(":")[1][:14]
        if self.cnpj != cnpj_certificado:
            raise ValidationError({"mensagem": "O CNPJ da filial não bate com o CNPJ do certificado"})

    def extrair_dados(self):
        try:
            cert = self.certificado
            subject = cert.subject.rfc4514_string()
            issuer = cert.issuer.rfc4514_string()
            serial_number = cert.serial_number
            not_before = cert.not_valid_before
            not_after = cert.not_valid_after
            
            public_key = cert.public_key()
            public_key_info = public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ).decode()
            
            cert_info = {
                "subject": subject,
                "issuer": issuer,
                "serial_number": serial_number,
                "not_valid_before": not_before,
                "not_valid_after": not_after,
                "public_key": public_key_info,
            }
            
            return cert_info
        except Exception as e:
            raise ValueError(f"Erro ao extrair informações do certificado: {e}")
    
    def get_private_key(self):
        try:
            private_key_info = self.private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ).decode()
            
            return private_key_info
        except Exception as e:
            raise ValueError(f"Erro ao extrair a chave privada: {e}")

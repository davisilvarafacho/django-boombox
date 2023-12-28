FROM python:3.8

# setando o diretório de trabalho
WORKDIR /code

# variáveis necesárias para o Django rodar no Docker
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copiando o projeto
COPY . .

# instalando as dependências
RUN pip install -r requirements.txt

# criando e aplicando as migrações
RUN python manage.py makemigrations
RUN python manage.py migrate
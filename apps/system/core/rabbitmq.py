import os
import json
import uuid
import pika


class ConnectionAMQP:
    def __init__(self):
        host = os.environ.get('RABBITMQ_HOST')
        usuario = os.environ.get('RABBITMQ_USER')
        senha = os.environ.get('RABBITMQ_PSSWD')
        porta = os.environ.get('RABBITMQ_PORT')

        credentials = pika.PlainCredentials(usuario, senha)
        self.conn = pika.BlockingConnection(pika.ConnectionParameters(host, porta, '/', credentials))
        self.channel = self.conn.channel()


class Consumer(ConnectionAMQP):
    def __init__(self, queue, callback):
        super().__init__()
        self.queue = queue
        self.callback = callback
        self.channel.queue_declare(queue=self.queue)

    def start_server(self):
        self.channel.basic_consume(queue=self.queue, on_message_callback=self.callback, auto_ack=True)
        print('[*] Iniciando consumo da queue "%s"...' % self.queue)
        print('[*] Aguardando mensagens. Para sair pressione CTRL+C')
        self.channel.start_consuming()

    @staticmethod
    def byte2str(data):
        return data.decode('utf-8')

    @staticmethod
    def byte2dict(data):
        data = Consumer.byte2str(data)
        data = data.replace("'", '"')
        return json.loads(data)


class Publisher(ConnectionAMQP):
    def __init__(self, routing_key):
        super().__init__()

        self.routing_key = routing_key
        self.channel.queue_declare(queue=self.routing_key)

    def publish(self, body=''):
        print('[*] Publicando mensagem na queue "%s"...' % self.routing_key)
        if isinstance(body, dict):
            body = str(body)

        self.channel.basic_publish(
            exchange='',
            routing_key=self.routing_key,
            body=body,
        )

    def config_rpc(self):
        queue_info = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = queue_info.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self._on_response,
            auto_ack=True,
        )

    def _on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body.decode('utf-8')

    def rpc_publish(self, body=''):
        print('[*] Publicando mensagem na queue "%s"...' % self.routing_key)
        if isinstance(body, dict):
            body = str(body)
        
        self.response = None 
        self.corr_id = str(uuid.uuid4())        
        
        self.channel.basic_publish(
            exchange='',
            routing_key=self.routing_key,
            body=body,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
        )

        while self.response is None:
            self.conn.process_data_events()

        return self.response

    @staticmethod
    def byte2str(data):
        return data.decode('utf-8')

    @staticmethod
    def byte2dict(data):
        data = Consumer.byte2str(data)
        data = data.replace("'", '"')
        return json.loads(data)

import pika, json, uuid

class Publish(object):

    def __init__(self):
        params = pika.URLParameters('amqps://hcihsiuu:eJ7FAp2_yF3Wuxq698SQdP18ytWz-zdw@cattle.rmq2.cloudamqp.com/hcihsiuu')

        self.connection = pika.BlockingConnection(params)

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, value):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='stock_service',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=value)
        while self.response is None:
            self.connection.process_data_events()
        return json.loads(self.response)

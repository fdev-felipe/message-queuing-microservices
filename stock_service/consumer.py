import pika, json, requests, csv
import urllib.request
from bs4 import BeautifulSoup as bs

params = pika.URLParameters('amqps://hcihsiuu:eJ7FAp2_yF3Wuxq698SQdP18ytWz-zdw@cattle.rmq2.cloudamqp.com/hcihsiuu')
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='stock_service')

def callback(ch, method, properties, body):
    try:
        stock_code = str(body.decode("utf-8"))
        CSV_URL = f'https://stooq.com/q/l/?s={stock_code}&f=sd2t2ohlcv&h=&e=csv'

        with requests.Session() as s:
            download = s.get(CSV_URL)
            decoded_content = download.content.decode('utf-8')
            cr = csv.reader(decoded_content.splitlines(), delimiter=',')

        data = list(cr)
        stock_values = dict(zip(data[0], data[1]))

        #Get stock name using web scraping
        url = f'https://stooq.com/q/?s={stock_code}'
        page = urllib.request.urlopen(url)
        html = bs(page.read(), "html.parser")
        stock_values['name'] = str(html.find_all('meta')[1].get('content').split(',')[0].upper())
        stock_values = json.dumps(stock_values, indent=4)

        if json.loads(stock_values)['Date'] == 'N/D':
            stock_values = json.dumps({"message": "Stock not found!"})
    except:
        stock_values = json.dumps({"message": "Stock not found!"})
    ch.basic_publish(exchange='',
                     routing_key=properties.reply_to,
                     properties=pika.BasicProperties(correlation_id=properties.correlation_id),
                     body=stock_values)
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='stock_service', on_message_callback=callback)
channel.start_consuming()
channel.close()

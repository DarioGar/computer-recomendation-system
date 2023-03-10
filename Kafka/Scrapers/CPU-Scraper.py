import json
import re
from bs4 import BeautifulSoup
import urllib.request
from kafka import KafkaProducer

SERVERS = 'localhost:9092'

def clean_string(string):
    return re.sub(r'[^a-zA-Z0-9()\-,. ]', '', string)

def build_CPU(data,index,CPU):
    if(index%2==0):
        return
    if(index==1):
        CPU['name'] = clean_string(data)
    elif(index==3):
        if data != 'Launched':
            CPU['status'] = 'Old'
        else:
            CPU['status'] = data
    elif(index==7):
        CPU['cores'] = data
    elif(index==9):
        CPU['turbo'] = data
    elif(index==11):
        CPU['base'] = data
    elif(index==13):
        CPU['cache'] = clean_string(data)
    elif(index==15):
        CPU['tdp'] = data
    elif(index==19):
        CPU['price'] = data
        


with open('CPU-Pages.py','r') as pages:
    webs = pages.read()
    page = urllib.request.urlopen("https://www.intel.com/content/www/us/en/products/details/processors/core/i5/products.html")
    mybytes = page.read()
    content = mybytes.decode("utf8")
    page.close()


    soup = BeautifulSoup(content,'lxml')


    producer = KafkaProducer(bootstrap_servers=SERVERS,value_serializer=lambda v: json.dumps(v).encode('utf-8'))

    table_content = soup.find('tbody')
    for cpu in table_content.find_all('tr'):#TR
        CPU = {}
        link = cpu.find('a')
        CPU['link'] = None if link is None else 'https://www.intel.com' + link['href']
        for index,data in enumerate(cpu):#TD
            cpu = build_CPU(data.text.strip().split('\n')[0],index,CPU)
        
        if CPU['status'] == 'Launched':
            producer.send('cpu',CPU)
            print(CPU)
            print("=============================")


    

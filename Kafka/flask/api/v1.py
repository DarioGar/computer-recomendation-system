from flask_restx import Api
import psycopg2 as psycopg2
import pymongo

PASSWORD = "jXueDSBPLJMtzjGl"
WOL_USER = "postgres"
WOL_DB_NAME = "pc_components"
WOL_PORT = 5432
WOL_HOST = "localhost"



api = Api(version='1.0',
        title = 'Computer components API',
        description='Manages all components found by scraping official websites')


client = pymongo.MongoClient("mongodb+srv://dgmalpicaing:" + PASSWORD + "@cluster.icx398j.mongodb.net/?retryWrites=true&w=majority")
mydb = client["components"]
cpu_collection = mydb["cpu"]


con = psycopg2.connect(dbname=WOL_DB_NAME,user=WOL_USER,password="12345",host=WOL_HOST,port=WOL_PORT)
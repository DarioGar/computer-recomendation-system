import threading
import json
import api.reusable
from flask_restx import Resource
from flask import jsonify, make_response
from flask_restx import cors
from flask_cors import cross_origin
from kafka import KafkaConsumer
from api.arguments.cpu_arguments import new_cpu_arguments
from api.v1 import api
from core import limiter, cache
from utils import handle400error, handle404error, handle500error
from api.models.mongo.CPU import CPU

cpus_ns = api.namespace('cpu',description='Manages processor components',decorators=[cors.crossdomain(origin="*")])

def deserializeCPU(serializedCPU):
	deserializedCPU = json.loads(serializedCPU.decode('utf-8'))
	split = deserializedCPU['name'].split('Processor')[0].strip().split(' ')[2]
	deserializedCPU['name'] = split
	return deserializedCPU

def consumer():
	consumer = KafkaConsumer('cpu',
						value_deserializer=deserializeCPU,
                         bootstrap_servers=['localhost:9092'])
	print(consumer)

	for message in consumer:
		# message value and key are raw bytes -- decode if necessary!
		# e.g., for unicode: `message.value.decode('utf-8')`
		print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
											message.offset, message.key,
											message.value))
		data = message.value
		cpu = CPU(data['name'],data['link'],data['cores'],data['turbo'],data['base'],data['cache'],data['tdp'],data['price'])
		id = cpu.register()

		

job_thread = threading.Thread(target=consumer)
job_thread.daemon = True
job_thread.start()


@cpus_ns.route('',methods=['GET','POST','OPTIONS'])
class CPUData(Resource):

	@cross_origin()
	@limiter.limit('1000/hour')
	@api.expect(new_cpu_arguments)
	@api.response(200, 'OK')
	@api.response(404, 'Data not found')
	@api.response(500, 'Unhandled errors')
	@api.response(400, 'Invalid parameters')
	@cache.cached(timeout=1, query_string=True)

	def post(self):
		"""
		Creates a cpu component
		"""
		#Retrieve arguments
		try:
			args = new_cpu_arguments.parse_args()
			name = args['name']
		except:
			return handle400error(cpus_ns,"The provided arguments are not correct. Please, check the swagger documentation at /v1")
		# Build the cpu
		try:
			cpu = CPU(name)
			id = cpu.register()
			response = jsonify(str(id))
			return make_response(response, 201)
		except:
			return handle500error(cpus_ns)


	@limiter.limit('1000/hour')
	@api.response(200, 'OK')
	@api.response(404, 'Data not found')
	@api.response(500, 'Unhandled errors')
	@api.response(400, 'Invalid parameters')
	@cache.cached(timeout=1, query_string=True)
	def get(self):
		"""
		Gets all cpus
		"""
		try:
			responseData = CPU.fetchAll()
			dataList = []
			for x in responseData:
				dataList.append(x)
			if(len(dataList) > 0):
				response = jsonify(dataList)
			else:	
				response = jsonify()
			return make_response(response, 200)
		except:
			return handle500error(cpus_ns)
		
		
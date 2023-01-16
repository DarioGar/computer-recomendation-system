from flask_restx import reqparse

new_cpu_arguments = reqparse.RequestParser()

new_cpu_arguments.add_argument('name',
							location='json',
							type=str,
							required=True,
							help='Processor name')

from flask_restx import reqparse

new_gpu_arguments = reqparse.RequestParser()

new_gpu_arguments.add_argument('name',
							location='json',
							type=str,
							required=True,
							help='Graphic\'s card name')

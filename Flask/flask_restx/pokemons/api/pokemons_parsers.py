#!/usr/bin/python3

# Copyright 2020 BISITE Research Group
# See LICENSE for details.

from flask_restx import reqparse
# Argumentos que se esperan en la query en los distintos tipos HTTP
pokemon_args_name_arguments = reqparse.RequestParser()

pokemon_args_name_arguments.add_argument('pokemon',
							location='args',
							type=str,
							required=False,
							help='Pokemons\'s name')

pokemon_body_name_arguments = reqparse.RequestParser()

pokemon_body_name_arguments.add_argument('pokemon',
							location='json',
							type=str,
							required=True,
							help='Pokemon\'s name')

pokemon_arguments = reqparse.RequestParser()

pokemon_arguments.add_argument('pokemon',
							location='json',
							type=str,
							required=True,
							help='Pokemon\'s name')

pokemon_arguments.add_argument('properties',
							location='json',
							type=dict,
							required=True,
							help='Pokemon\'s properties like name,type,region and height.')
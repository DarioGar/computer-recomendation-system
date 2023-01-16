#!/usr/bin/python3

# Copyright 2020 BISITE Research Group
# See LICENSE for details.

from flask_restx import fields
from pokemons.api.v1 import api

pokemon_model = api.model('Adress information', {
	'name': fields.String(example='Pikachu'),
	'type': fields.List(cls_or_instance=fields.String,example='Electro'),
    'region': fields.String(example='Johto'),
    'height': fields.Float(example='0.40')
}, description='A pokemon\'s information')

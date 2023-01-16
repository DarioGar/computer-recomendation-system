#!/usr/bin/python3

# Copyright 2020 BISITE Research Group
# See LICENSE for details.

import datetime
from flask_restx import Resource
import numpy as np
import json
import psycopg2 as psycopg2
import psycopg2.extras
from psycopg2.extensions import AsIs
from api.v1 import api
from pokemons.core import cache, limiter
from pokemons.api.pokemons_models import pokemon_model
from pokemons.api.pokemons_parsers import pokemon_args_name_arguments, pokemon_body_name_arguments, pokemon_arguments
from pokemons.utils import handle400error, handle404error, handle500error

pokemons_ns = api.namespace('pokemons', description='Provides pokemons information')
con = psycopg2.connect(database= "pokemon",user="postgres",password="563412",host="127.0.0.1",port="5432")

@pokemons_ns.route('/pokemons')
class pokemonsCollection(Resource):

    @limiter.limit('1000/hour') 
    @api.expect(pokemon_args_name_arguments)
    @api.response(200, 'OK')
    @api.response(404, 'Data not found')
    @api.response(500, 'Unhandled errors')
    @api.response(400, 'Invalid parameters')
    @cache.cached(timeout=1, query_string=True)
    @api.marshal_with(pokemon_model, code=200, description='OK', as_list=True)
    def get(self):
        """
        Returns a pokemon if that pokemon exists in the database, else returns all pokemons in the database
        """
        # retrieve and chek arguments
        try:
            args = pokemon_args_name_arguments.parse_args()
            cur = con.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
            if args['pokemon'] is not None:
                query= "select * from public.pokemon where name = %s"
                cur.execute(query,(args['pokemon'],))
                rows = cur.fetchall()
                if len(rows) != 0:
                    pokemon_name = rows
                else:
                    pokemon_name = None
            else:
                pokemon_name = None
            #print(pokemon_name)
        except:
            return handle400error(pokemons_ns, 'The provided arguments are not correct. Please, check the swagger documentation at /v1')

        # check parameters
        if pokemon_name is None and (args['pokemon']) is not None:
            return handle404error(pokemons_ns, 'The provided pokemon was not found.')

        # build result 
        try:
            if pokemon_name is None:
                query= "select * from public.pokemon"
                cur=con.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
                cur.execute(query)
                rows = cur.fetchall()
                pokemons = rows
            else:
                pokemons = pokemon_name
        except:
            return handle500error(pokemons_ns)
        # if there is not pokemons found, return 404 error
        if not pokemons:
            return handle404error(pokemons_ns, 'No pokemons founds.')

        return pokemons

    @limiter.limit('1000/hour') 
    @api.expect(pokemon_arguments)
    @api.response(200, 'OK')
    @api.response(404, 'Data not found')
    @api.response(500, 'Unhandled errors')
    @api.response(400, 'Invalid parameters')
    @cache.cached(timeout=1, query_string=True)
    def post(self):
        """
        Creates a pokemon
        
        """
        # retrieve and chek arguments
        try:
            args = pokemon_arguments.parse_args()
            pokemon_name = args['pokemon']
            pokemon_properties = args['properties']
        except:
            return handle400error(pokemons_ns, 'The provided arguments are not correct. Please, check the swagger documentation at /v1')

        # check parameters
        cur = con.cursor()
        if args['pokemon'] is not None:
            query= "select count(1) from public.pokemon where name = %s"
            cur.execute(query,(pokemon_name,))
            rows = cur.fetchall()
        if rows[0] != (0,):
            return handle400error(pokemons_ns, 'The provided pokemon was already created')

        # build the pokemon
        try:
            cur = con.cursor()
            name = args['pokemon']
            types = args['properties']['type']
            if len(types) <=2:
                region = args['properties']['region']
                height = float(args['properties']['height'])
                query = "insert into public.pokemon values (%s,'{%s}',%s,%s)"
                retorno = cur.execute(query,(name,AsIs(json.dumps(types)[1:-1]),region,height))
                con.commit()
        except:
            return handle500error(pokemons_ns)

        if len(types) > 2:
            return handle400error(pokemons_ns, "The provided arguments are not correct. Pokemon's can't have more than two types ...yet")
    @limiter.limit('1000/hour') 
    @api.expect(pokemon_arguments)
    @api.response(200, 'OK')
    @api.response(404, 'Data not found')
    @api.response(500, 'Unhandled errors')
    @api.response(400, 'Invalid parameters')
    @cache.cached(timeout=1, query_string=True)
    def put(self):
        """
        Updates an existing pokemon
        """

        # retrieve and chek arguments
        try:
            args = pokemon_arguments.parse_args()
            pokemon_name = args['pokemon']
            pokemon_properties = args['properties']
        except:
            return handle400error(pokemons_ns, 'The provided arguments are not correct. Please, check the swagger documentation at /v1')

        # check parameters
        cur = con.cursor()
        if args['pokemon'] is not None:
            query= "select count(1) from public.pokemon where name = %s"
            cur.execute(query,(pokemon_name,))
            rows = cur.fetchall()
        if rows[0] == (0,):
            return handle404error(pokemons_ns, 'The provided pokemon was not found')

        # update cat 
        try:
            cur = con.cursor()
            name = args['pokemon']
            types = args['properties']['type']
            if len(types) <= 2:
                region = args['properties']['region']
                height = float(args['properties']['height'])
                query = "update public.pokemon set name = %s , type = '{%s}' , region = %s , height = %s where name = %s"
                cur.execute(query,(name,AsIs(json.dumps(types)[1:-1]),region,height,name))
                con.commit()
        except:
            return handle500error(pokemons_ns)
        
        if len(types) > 2:
            return handle400error(pokemons_ns, "The provided arguments are not correct. Pokemon's can't have more than two types ...yet")

    @limiter.limit('1000/hour') 
    @api.expect(pokemon_body_name_arguments)
    @api.response(200, 'OK')
    @api.response(404, 'Data not found')
    @api.response(500, 'Unhandled errors')
    @api.response(400, 'Invalid parameters')
    @cache.cached(timeout=1, query_string=True)
    def delete(self):
        """
        Deletes an existing pokemon
        """

        # retrieve and chek arguments
        try:
            args = pokemon_body_name_arguments.parse_args()
            pokemon_name = args['pokemon']
        except:
            return handle400error(pokemons_ns, 'The provided arguments are not correct. Please, check the swagger documentation at /v1')

        # check parameters
        cur = con.cursor()
        if args['pokemon'] is not None:
            query= "select count(1) from public.pokemon where name = %s"
            cur.execute(query,(pokemon_name,))
            rows = cur.fetchall()
        if rows[0] == (0,):
            return handle404error(pokemons_ns, 'The provided cat was not found')

        # update cat 
        try:
            cur = con.cursor()
            query= "delete from public.pokemon where name = %s"
            cur.execute(query,(args['pokemon'],))
            con.commit()
        except:
            return handle500error(pokemons_ns)

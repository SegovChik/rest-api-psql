from flask import Flask, request
from flask import current_app as app

# from app.controllers.actor import *
# from app.controllers.movie import *

from controllers.actor import *
from controllers.movie import *

@app.route('/api/movies', methods=['GET'])
def movies():
    """
    Get all actors in db
    """
    return get_all_movies()

@app.route('/api/movie', methods=['GET'])
def movie_by_id():
    return get_movie_by_id()

@app.route('/api/movie', methods=['POST'])
def post_add_movie():
    return add_movie()


@app.route('/api/actors', methods=['GET'])
def actors():
    """
    Get all actors in db
    """
    return get_all_actors()


@app.route('/api/actor', methods=['GET'])
def actor_by_id():
    return get_actor_by_id()


@app.route('/api/actor', methods=['POST'])
def post_add_actor():
    return add_actor()

@app.route('/api/actor', methods=['PUT'])
def put_upd_actor():
    return upd_actor()

@app.route('/api/movie', methods=['PUT'])
def put_upd_movie():
    return upd_movie()


@app.route('/api/actor', methods=['DELETE'])
def delete_actor():
    return del_actor()


@app.route('/api/movie', methods=['DELETE'])
def delete_movie():
    return del_movie()

@app.route('/api/actor-relations', methods=['PUT'])
def act_add_rel():
    return actor_add_relation()

@app.route('/api/movie-relations', methods=['PUT'])
def mov_add_rel():
    return movie_add_relation()

@app.route('/api/actor-relations', methods=['DELETE'])
def act_del_rel():
    return actor_clear_relations()

@app.route('/api/movie-relations', methods=['DELETE'])
def mov_adel_rel():
    return movie_clear_relations()





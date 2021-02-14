from flask import jsonify, make_response

from datetime import datetime as dt
from ast import literal_eval

from models.actor import Actor
from models.movie import Movie
from settings.constants import MOVIE_FIELDS  # to make response pretty
from settings.constants import ACTOR_FIELDS
from controllers.parse_request import get_request_data


# from app.models.actor import Actor
# from app.models.movie import Movie
# from app.settings.constants import MOVIE_FIELDS  # to make response pretty
# from app.controllers.parse_request import get_request_data


def get_all_movies():
    """
    Get list of all records
    """
    all_movies = Movie.query.all()
    movies = []
    for movie in all_movies:
        mov = {k: v for k, v in movie.__dict__.items() if k in MOVIE_FIELDS}
        movies.append(mov)
    return make_response(jsonify(movies), 200)


def get_dict_of_movies():
    all_movies = Movie.query.all()
    movies = []
    for movie in all_movies:
        mov = {k: v for k, v in movie.__dict__.items() if k in MOVIE_FIELDS}
        movies.append(mov)
    return movies


def get_movie_by_id():
    """
    Get record by id
    """

    data = get_request_data()

    for dat in data:
        if dat not in set(MOVIE_FIELDS):
            err = 'Wrong key'
            return make_response(jsonify(error=err), 400)

    if 'id' in data.keys():
        try:
            row_id = int(data['id'])
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400)

        obj = Movie.query.filter_by(id=row_id).first()
        try:
            movie = {k: v for k, v in obj.__dict__.items() if k in MOVIE_FIELDS}
        except:
            err = 'Record with such id does not exist'
            return make_response(jsonify(error=err), 400)

        return make_response(jsonify(movie), 200)

    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)


def add_movie():
    """
    Add new movies
    """
    data = get_request_data()
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    print(data)
    for dat in data:
        if dat not in set(MOVIE_FIELDS):
            err = 'Wrong key'
            return make_response(jsonify(error=err), 400)

    if 'name' in data.keys():
        if data['name'].isdigit():
            err = 'Name must be string'
            return make_response(jsonify(error=err), 400)

        if (len(data['name']) >= 50):
            err = 'Name must be less than 50 characters'
            return make_response(jsonify(error=err), 400)

        if not data['name']:
            err = 'Name cannot be null'
            return make_response(jsonify(error=err), 400)

        mov_dict = get_dict_of_movies()
        for m in mov_dict:
            if (m['name'] == data['name']):
                err = 'movie with that name is already exist'
                return make_response(jsonify(error=err), 400)

    if 'year' in data.keys():
        try:
            year = int(data['year'])
        except:
            err = 'year must be integer'
            return make_response(jsonify(error=err), 400)
    if 'genre' in data.keys():
        if data['genre'].isdigit():
            err = 'Genre must be string'
            return make_response(jsonify(error=err), 400)

        if (len(data['genre']) > 50):
            err = 'Genre must be less than 50 characters'
            return make_response(jsonify(error=err), 400)
    new_record = data
    new_movie = Movie.create(**new_record)
    new_record['id'] = new_movie.id

    return make_response(jsonify(new_record), 200)


def upd_movie():
    data = get_request_data()
    new_record = data
    for dat in data:
        if dat not in set(MOVIE_FIELDS):
            err = 'Wrong key'
            return make_response(jsonify(error=err), 400)
    if data.get('id'):
        try:
            row_id = int(data['id'])
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400)

        obj = Movie.query.filter_by(id=row_id).first()
        try:
            try_movie = {k: v for k, v in obj.__dict__.items() if k in MOVIE_FIELDS}
        except:
            err = 'Record with such id does not exist'
            return make_response(jsonify(error=err), 400)

        if data.get('genre'):
            if data['genre'].isdigit():
                err = 'Genre must be string'
                return make_response(jsonify(error=err), 400)

            elif (len(data['genre']) > 50):
                err = 'Genre must be less than 50 characters'
                return make_response(jsonify(error=err), 400)
        else:
            new_record.pop('genre', None)

        if data.get('year'):
            try:
                year = int(data['year'])
            except:
                err = 'year must be integer'
                return make_response(jsonify(error=err), 400)
        else:
            new_record.pop('year', None)


        if data.get('name'):
            obj = Movie.query.filter_by(name=new_record['name']).first()
            if obj:
                err = 'Actor with that name already exist'
                return make_response(jsonify(error=err), 400)
            if data['name'].isdigit():
                err = 'Name must be string'
                return make_response(jsonify(error=err), 400)

            if (len(data['name']) > 50):
                err = 'Name must be less than 50 characters'
                return make_response(jsonify(error=err), 400)
        else:
            new_record.pop('data', None)
        Movie.update(data['id'], **new_record)

        movie = Movie.query.filter_by(id=data['id']).first()
        if movie:
            return_var = {k: v for k, v in movie.__dict__.copy().items() if not k.startswith('_')}
        else:
            err = f'Could not find an actor with ID {data.get("id")}'
            return make_response(jsonify(error=err), 400)

        return make_response(jsonify(return_var), 200)
    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)



def del_movie():
    data = get_request_data()

    if 'id' in data.keys():
        try:
            row_id = int(data['id'])
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400)

        obj = Movie.query.filter_by(id=data['id']).first()
        try:
            movie = {k: v for k, v in obj.__dict__.items() if k in MOVIE_FIELDS}
        except:
            err = 'Record with such id does not exist'
            return make_response(jsonify(error=err), 400)

        Movie.delete(data['id'])
        message = "row with id has been succsessfuly deleted"
        return make_response(jsonify(message), 200)
    else:
        err = 'Wrong key'
        return make_response(jsonify(error=err), 400)

def movie_add_relation():
    """
    Add a movie to actor's filmography
    """
    data = get_request_data()
    KEY_DICT = ['id','relation_id']
    for dat in data:
        if dat not in set(KEY_DICT):
            err = 'Wrong key'
            return make_response(jsonify(error=err), 400)


    ### YOUR CODE HERE ###
    if data.get('id'):
        try:
            row_id = int(data['id'])
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400)
        obj = Movie.query.filter_by(id=data['id']).first()
        try:
            try_movie = {k: v for k, v in obj.__dict__.items() if k in MOVIE_FIELDS}
        except:
            err = 'Movie with such id does not exist'
            return make_response(jsonify(error=err), 400)
        if data.get('relation_id'):
            try:
                row_id = int(data['relation_id'])
            except:
                err = 'Id must be integer'
                return make_response(jsonify(error=err), 400)
            obj = Actor.query.filter_by(id=data['relation_id']).first()
            try:
                try_actor = {k: v for k, v in obj.__dict__.items() if k in ACTOR_FIELDS}
            except:
                err = 'Actor with such id does not exist'
                return make_response(jsonify(error=err), 400)
        else:
            err = 'No related_id specified'
            return make_response(jsonify(error=err), 400)
        related_actor = Actor.query.filter_by(id=data['relation_id']).first()
        movie =  Movie.add_relation(data['id'], related_actor)# add relation here
        rel_movie = {k: v for k, v in movie.__dict__.items() if k in MOVIE_FIELDS}
        rel_movie['cast'] = str(movie.cast)
        return make_response(jsonify(rel_movie), 200)
    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)

def movie_clear_relations():
    """
    Clear all relations by id
    """
    data = get_request_data()

    if 'id' in data.keys():
        try:
            row_id = int(data['id'])
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400)
        movie = Movie.query.filter_by(id=row_id).first()

        try:
            movie.clear_relations(row_id)
            rel_movie = {k: v for k, v in movie.__dict__.items() if k in MOVIE_FIELDS}
            rel_movie['cast'] = str(movie.cast)
        except:
            err = 'Record with such id does not exist'
            return make_response(jsonify(error=err), 400)

        return make_response(jsonify(rel_movie), 200)
    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)

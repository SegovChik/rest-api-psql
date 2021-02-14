from flask import jsonify, make_response
from datetime import datetime as dt
from sqlalchemy import Date, cast
from settings.constants import *
from ast import literal_eval
from models.actor import Actor
from models.movie import Movie
from settings.constants import ACTOR_FIELDS  # to make response pretty
from controllers.parse_request import get_request_data

from models.actor import Actor
from models.movie import Movie
from settings.constants import ACTOR_FIELDS  # to make response pretty
from controllers.parse_request import get_request_data


def get_all_actors():
    """
    Get list of all records
    """
    all_actors = Actor.query.all()
    actors = []
    for actor in all_actors:
        act = {k: v for k, v in actor.__dict__.items() if k in ACTOR_FIELDS}
        actors.append(act)
    return make_response(jsonify(actors), 200)


def get_dict_of_actors():
    all_actors = Actor.query.all()
    actors = []
    for actor in all_actors:
        act = {k: v for k, v in actor.__dict__.items() if k in ACTOR_FIELDS}
        actors.append(act)
    return actors


def get_actor_by_id():
    data = get_request_data()
    if 'id' in data.keys():
        try:
            row_id = int(data['id'])
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400)

        obj = Actor.query.filter_by(id=row_id).first()
        try:
            actor = {k: v for k, v in obj.__dict__.items() if k in ACTOR_FIELDS}
        except:
            err = 'Record with such id does not exist'
            return make_response(jsonify(error=err), 400)

        return make_response(jsonify(actor), 200)

    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)


def add_actor():
    """
    Add new actor
    """
    data = get_request_data()

    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    for dat in data:
        if dat not in set(ACTOR_FIELDS):
            err = 'Wrong key'
            return make_response(jsonify(error=err), 400)

    if 'name' in data.keys():
        if data['name'].isdigit():
            err = 'Name must be string'
            return make_response(jsonify(error=err), 400)

        if (len(data['name']) > 50):
            err = 'Name must be less than 50 characters'
            return make_response(jsonify(error=err), 400)

        if not data['name']:
            err = 'Name cannot be null'
            return make_response(jsonify(error=err), 400)

    if 'gender' in data.keys():
        if (data['gender'] != "male") and (data['gender'] != "female"):  # !!!!!!!!!!!!!!!!!!!!!!!!
            err = 'There are only two genders'
            return make_response(jsonify(error=err), 400)

    if 'date_of_birth' in data.keys():
        try:
            dt.strptime(data['date_of_birth'], DATE_FORMAT).date()
        except:
            err = 'incorrect date format(d.m.y)'
            return make_response(jsonify(error=err), 400)
    act_dict = get_dict_of_actors()
    for a in act_dict:
        if (a['name'] == data['name']):
            err = 'actor with that name is already exist'
            return make_response(jsonify(error=err), 400)

    new_record = data
    new_record['date_of_birth'] = dt.strptime(data['date_of_birth'], '%d.%m.%Y').date()

    new_actor = Actor.create(**new_record)  # !!!!!!!!!!!!!!!!!!!!!!!!
    new_record['id'] = new_actor.id

    return make_response(jsonify(new_record), 200)


def upd_actor():
    data = get_request_data()
    new_record = data
    for dat in data:
        if dat not in set(ACTOR_FIELDS):
            err = 'Wrong key'
            return make_response(jsonify(error=err), 400)
    if data.get('id'):
        try:
            row_id = int(data['id'])
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400)

        obj = Actor.query.filter_by(id=row_id).first()

        try:
            try_actor = {k: v for k, v in obj.__dict__.items() if k in MOVIE_FIELDS}
        except:
            err = 'Record with such id does not exist'
            return make_response(jsonify(error=err), 400)
        if data.get('gender'):
            if (data['gender'] != "male") and (data['gender'] != "female") and (data['gender'] != "Female") and (
                    data['gender'] != "Male"):  # !!!!!!!!!!!!!!!!!!!!!!!!
                err = 'There are only two genders'
                return make_response(jsonify(error=err), 400)
        else:
            new_record.pop('date_of_birth', None)


        if data.get('date_of_birth'):
            try:
                dt.strptime(data['date_of_birth'], DATE_FORMAT).date()
                new_record['date_of_birth'] = dt.strptime(data['date_of_birth'], DATE_FORMAT).date()
            except:
                err = 'incorrect date format(d.m.y)'
                return make_response(jsonify(error=err), 400)
        else:
            new_record.pop('date_of_birth', None)

        if data.get('name'):
            obj = Actor.query.filter_by(name=new_record['name']).first()
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
        Actor.update(data['id'], **new_record)

        actor = Actor.query.filter_by(id=data['id']).first()
        print(actor)
        if actor:
            return_var = {k: v for k, v in actor.__dict__.copy().items() if not k.startswith('_')}
        else:
            err = f'Could not find an actor with ID {data.get("id")}'
            return make_response(jsonify(error=err), 400)

        return make_response(jsonify(return_var), 200)
    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)

def del_actor():
    data = get_request_data()
    id_del = data['id']

    if id_del and 'id' in data.keys():
        try:
            row_id = int(data['id'])
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400)

        obj = Actor.query.filter_by(id=row_id).first()
        try:
            actor = {k: v for k, v in obj.__dict__.items() if k in ACTOR_FIELDS}
        except:
            err = 'Record with such id does not exist'
            return make_response(jsonify(error=err), 400)

        Actor.delete(id_del)
        message = "row with id has been succsessfuly deleted"
        return make_response(jsonify(message), 200)
    else:
        err = 'Wrong key'
        return make_response(jsonify(error=err), 400)


def actor_add_relation():
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
        obj = Actor.query.filter_by(id=data['id']).first()
        try:
            try_actor = {k: v for k, v in obj.__dict__.items() if k in ACTOR_FIELDS}
        except:
            err = 'Actor with such id does not exist'
            return make_response(jsonify(error=err), 400)
        if data.get('relation_id'):
            try:
                row_id = int(data['relation_id'])
            except:
                err = 'Id must be integer'
                return make_response(jsonify(error=err), 400)
            obj = Movie.query.filter_by(id=data['relation_id']).first()
            try:
                try_movie = {k: v for k, v in obj.__dict__.items() if k in MOVIE_FIELDS}
            except:
                err = 'Movie with such id does not exist'
                return make_response(jsonify(error=err), 400)
        else:
            err = 'No related_id specified'
            return make_response(jsonify(error=err), 400)
        related_movie = Movie.query.filter_by(id=data['relation_id']).first()
        actor =  Actor.add_relation(data['id'], related_movie)# add relation here
        rel_actor = {k: v for k, v in actor.__dict__.items() if k in ACTOR_FIELDS}
        rel_actor['filmography'] = str(actor.filmography)
        return make_response(jsonify(rel_actor), 200)
    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)

def actor_clear_relations():
    """
    Clear all relations by id
    """
    data = get_request_data()
    ### YOUR CODE HERE ###
    if 'id' in data.keys():
        try:
            row_id = int(data['id'])
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400)
        actor = Actor.query.filter_by(id=row_id).first()
        try:
            actor.clear_relations(row_id)
            rel_actor = {k: v for k, v in actor.__dict__.items() if k in ACTOR_FIELDS}
            rel_actor['filmography'] = str(actor.filmography)
        except:
            err = 'Record with such id does not exist'
            return make_response(jsonify(error=err), 400)

        return make_response(jsonify(rel_actor), 200)

    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)

    # use this for 200 response code

    ### END CODE HERE ###






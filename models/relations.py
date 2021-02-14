from core import db
from models.base import Model

# Table name -> 'association'
# Columns: 'actor_id' -> db.Integer, db.ForeignKey -> 'actors.id', primary_key = True
#          'movie_id' -> db.Integer, db.ForeignKey -> 'movies.id', primary_key = True

association = db.Table('association', db.metadata,
    db.Column('actor_id', db.Integer, db.ForeignKey('actors.id', onupdate="CASCADE", ondelete="CASCADE"), primary_key=True),
    db.Column('movie_id', db.Integer, db.ForeignKey('movies.id', onupdate="CASCADE", ondelete="CASCADE"), primary_key=True))

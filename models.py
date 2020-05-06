import os
from peewee import *
import datetime

from flask_login import UserMixin

from playhouse.db_url import connect

if 'ON_HEROKU' in os.environ: # later we will manually add this env var 
                              # in heroku so we can write this code
  	DATABASE = connect(os.environ.get('DATABASE_URL')) # heroku will add this 
                                                     # env var for you 
                                                     # when you provision the
                                                     # Heroku Postgres Add-on
else:
	DATABASE = SqliteDatabase('project3.sqlite')




class User(UserMixin, Model):
	username=CharField(unique=True)
	email=CharField(unique=True)
	password=CharField()

	class Meta:
		database = DATABASE

class Client(Model):
	first_name = CharField()
	last_name = CharField()
	date_of_birth = DateField()
	location = CharField()
	photographer = ForeignKeyField(User, backref='clients')

	class Meta:
		database = DATABASE

class Session(Model):
	title = CharField()
	date = DateField()
	time = CharField()
	location = CharField()
	comments = TextField()
	photographer = ForeignKeyField(User, backref='sessions')
	client = ForeignKeyField(Client, backref='sessions')

	class Meta:
		database = DATABASE




def initialize():
	DATABASE.connect()

	DATABASE.create_tables([User, Client, Session], safe=True)
	print("Connected to DB and created tables if they didn't already exist.")
	DATABASE.close()
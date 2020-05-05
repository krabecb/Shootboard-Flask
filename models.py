from peewee import *
import datetime

from flask_login import UserMixin

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
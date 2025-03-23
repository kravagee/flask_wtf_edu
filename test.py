from data import db_session
from data.db_session import global_init
from data.users import User

global_init('db/mars_explorer.db')

us = User()
us.name = '1'
us.surname = '2'
us.email = 'qwe@mail.ru'
us.hashed_password = '123'

db_sess = db_session.create_session()
db_sess.add(us)
db_sess.commit()
db_sess.close()
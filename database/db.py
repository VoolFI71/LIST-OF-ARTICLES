from pony.orm import *

db = Database()


class User(db.Entity):
    user_id = Required(str)
    nick = Required(str)
    age = Required(int)
    wallets = Set('Wallet')


class Wallet(db.Entity):
    address = Required(str)
    private_key = Required(str)
    owner = Required(User)


try:
    db.bind(provider='sqlite', filename='database.sqlite', create_db=True)
except Exception as Ex:
    print(Ex)
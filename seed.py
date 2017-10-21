
"""Utility file to seed community score database from various sources"""

from sqlalchemy import func
from model import connect_to_db, db, Address, User, Category, User_saved_event, Source  #<import classes>
from datetime import datetime
from server import app
from json import loads
from random import randint

def load_sources():
    """Load real sources into database."""

    print "Sources"
    Source.query.delete()

    src_dict = {'mtup': 'Meetup.com',
                'evtb': 'Eventbrite.com',
                'sfpk': 'SF Parks and Recreation'
                }

    for k, v in src_dict.items():
        src_id = k
        name = v

        source = Source(src_id=src_id, name=name)
        db.session.add(source)

    db.session.commit()


def load_categories():
    """Load real categories into database."""

    print "Categories"
    Category.query.delete()

    # from eventbrite
    eb_file = open('seed_data/eb_categories.json')
    eb_dict = loads(eb_file.read())
    eb_cats = eb_dict['categories']
    print eb_cats

    for cat in eb_cats:
        print 'EB: ', cat
        cat_id = cat['id']
        name = cat['name']
        short_name = cat['short_name']
        src_id = 'evtb'

        eb_cat_row = Category(cat_id=cat_id, name=name, short_name=short_name, src_id=src_id)
        db.session.add(eb_cat_row)

    # from meetup 
    mu_file = open("seed_data/mu_categories.json")
    mu_dict = loads(mu_file.read())
    mu_cats = mu_dict['results']
    print mu_cats

    for cat in mu_cats: 
        print 'MU: ', cat
        cat_id = cat['id']
        name = cat['name']
        short_name = cat['shortname']
        src_id = 'mtup'

        mu_cat_row = Category(cat_id=cat_id, name=name, short_name=short_name, src_id=src_id)
        db.session.add(mu_cat_row)

    db.session.commit()


###### Mock Data ######
def load_addresses():
    """Load mock addresses into database."""

    print 'Addresses'
    Address.query.delete()

    filename = open("seed_data/addresses.json")
    address_list = loads(filename.read())

    for address in address_list:
        print address
        addy_id = address['addy_id'],
        lat = address['lat'],
        lng = address['lng'],

        address = Address(addy_id=addy_id, lat=lat, lng=lng)

        db.session.add(address)

    db.session.commit()
    filename.close()


def load_users():
    """Load mock users into database."""

    print "Users"
    User.query.delete()

    filename = open("seed_data/users.json")
    users_list = loads(filename.read())

    for user in users_list:
        print user
        user_id = user['user_id']
        name = user['name']
        email = user['email']
        password = user['password']

        user = User(user_id=user_id, name=name, email=email, password=password)

        db.session.add(user)

    db.session.commit()
    filename.close()


###### Helper function ######
def set_val_user_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(User.user_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('users_user_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_sources()
    load_categories()
    # load_addresses()
    # load_users()
    # set_val_user_id()

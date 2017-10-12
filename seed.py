
"""Utility file to seed community score database from various sources"""

from sqlalchemy import func
from model import connect_to_db, db, Address, User, Category #<import classes>
from datetime import datetime
from server import app
from json import loads
from random import randint

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
        # addy_id = randint(1, 100)
        # addy_id = 5

        user = User(user_id=user_id, name=name, email=email, password=password)

        db.session.add(user)

    db.session.commit()
    filename.close()


def load_categories():
    """Load mock categories into database."""

    print "Categories"
    Category.query.delete()

    cat_dict = {"meetup":"Events from the meetup.com", 
                "garden":"Community gardens in SF", 
                "volun":"Volunteer opportunities in SF",
                "evtbr":"Events from eventbrite.com", 
                "parksrec":"Public parks and recreation activities"}

    for category in cat_dict.keys():
        cat_row = Category(name=category, description=cat_dict[category])
        db.session.add(cat_row)

    db.session.commit()


# Helper function
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
    # load_addresses()
    load_users()
    load_categories()
    set_val_user_id()


"""Utility file to seed community score database from various sources"""

from sqlalchemy import func
from model import connect_to_db, db, #<import classes>
from datetime import datetime
from server import app


def load_neighborhood_boundaries():
    """Load GeoJSON file of neighborhood boundaries within San Francisco."""

    print "Users"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    User.query.delete()

    # Read u.user file and insert data
    for row in open("seed_data/u.user"):
        row = row.rstrip()
        user_id, age, gender, occupation, zipcode = row.split("|")

        user = User(user_id=user_id,
                    age=age,
                    zipcode=zipcode)

        # We need to add to the session or it won't ever be stored
        db.session.add(user)


    # Once we're done, we should commit our work
    db.session.commit()


def load_movies():
    """Load movies from u.item into database."""

    print 'Movies'
    Movie.query.delete()

    for row in open("seed_data/u.item"):
        row = row.rstrip()
        clean = row.split("|")
        if clean[1] == "unknown":
            next
        else:
            date = datetime.strptime(clean[2], '%d-%b-%Y').date()
            movie = Movie(movie_id=clean[0],
                          title=clean[1][:-7],
                          released_at=date,
                          imdb_url=clean[4])
            #how do we get rid of the HH:MM from the timestamp?
        db.session.add(movie)

    db.session.commit()

def load_ratings():
    """Load ratings from u.data into database."""

    print "Ratings"

    Rating.query.delete()

    for row in open("seed_data/u.data"):
        print row
        user_id, movie_id, score, timestamp = row.split()

        rating = Rating(user_id=user_id,
                        movie_id=movie_id,
                        score=score)

        db.session.add(rating)

    db.session.commit()

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
    load_users()
    load_movies()
    load_ratings()
    set_val_user_id()

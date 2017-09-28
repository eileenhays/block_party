""" Models and database functions for Community database. """

from flask_sqlalchemy import SQLAlchemy

# Connect to the PostgreSQL database

db = SQLAlchemy()

# Model definitions

class Address(db.Model):
    """Standard format for address information for user location and for events."""

    __tablename__ = 'addresses'

    addy_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    lat = db.Column(db.String(100), nullable=False)
    lng = db.Column(db.String(100), nullable=False)
    add_line1 = db.Column(db.String(100), nullable=False)
    add_line2 = db.Column(db.String(100), nullable=True)
    city =  db.Column(db.String(100), nullable=False)
    zipcode = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        """Prints address object in a more helpful way"""

        return "<Address: addy_id=%s lat=%s lng=%s>" % (self.addy_id,
                                                        self.lat,
                                                        self.lng)


class User(db.Model):
    """User information collected when user registers."""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(75), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    addy_id = db.Column(db.ForeignKey(Address.addy_id), nullable=True)

    def __repr__(self):
        """Prints user object in a more helpful way"""

        return "<User: user_id=%s name=%s email=%s>" % (self.user_id, self.name,
                                                        self.email)


class Category(db.Model):
    """Category of community event/activity."""

    __tablename__ = 'categories'

    cat_id = db.Column(db.String(5), primary_key=True, unique=True)
    description = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        """Prints category object in a more helpful way"""

        return "<Category: cat_id=%s description=%s>" % (self.cat_id,
                                                  self.description)
#
#
# class Neighborhood_geometry(db.Model):
#     """Neighborhood geometry information collected to use on the community score
#     site.
#     """
#
#     __tablename__ = 'nhood_geos'
#
#     geo_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     nhood_id = db.Column(db.Integer, db.ForeignKey('neighborhoods.nhood_id'),
#                          nullable=False)
#     latitude = db.Column(db.Float(50), nullable=False)
#     longitude = db.Column(db.Float(50), nullable=False)
#
#     def __repr__(self):
#         """Prints neighborhood geometry object in a more helpful way"""
#
#         return "<Neighborhood_geometry: geo_id=%s nhood_id=%s>" % (self.geo_id,
#                                                                    self.nhood_id)
#
#

#
#
# class Saved_location(db.Model):
#     """Location information saved by user to use on the community score site."""
#
#     __tablename__ = 'saved_locs'
#
#     saved_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
#     add_id = db.Column(db.Integer, db.ForeignKey('addresses.add_id'), nullable=False)
#     nhood_id = db.Column(db.Integer, db.ForeignKey('addresses.add_id'), nullable=False)
#
#     def __repr__(self):
#         """Prints saved_location object in a more helpful way"""
#
#         return "<Saved_location: saved_id=%s user_id=%s add_id=%s>" % (self.saved_id,
#                                                                        self.user_id,
#                                                                        self.add_id)




##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///community'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)

if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."

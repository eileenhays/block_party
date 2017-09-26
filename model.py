""" Models and database functions for Community Score database. """

from flask_sqlalchemy import SQLAlchemy

# Connect to the PostgreSQL database

db = SQLAlchemy()

# Model definitions

class User(db.Model):
    """User information collected to use on the community score site."""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, autoincrement=True, primary_key= True)
    name = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        """Prints object in more helpful way."""

        pass


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

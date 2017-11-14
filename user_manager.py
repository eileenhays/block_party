from flask import Flask, Response
from flask.ext.login import LoginManager, UserMixin, login_required


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)



class UserManager(object):


	def user_registration(self, name, email, regis_pw_input):
    """Register new user and save info in database"""

    # Check if user is already registered
    if User.query.filter_by(email=email).first() is not None:
        flash("There is already an account registered with this email.")
        return redirect("/registration")

    # Hash password to save in database
    hashed_pw = bcrypt.hash(self.regis_pw_input)
    del self.regis_pw_input    

    address = save_current_address()

    # Add user record in DB 
    if address.addy_id:
        user = User(name=self.name, email=self.email, password=self.hashed_pw, addy_id=self.address.addy_id)
    else:
        user = User(name=self.name, email=self.email, password=self.hashed_pw)

    db.session.add(user)
    db.session.commit() 

    flash("registration was successful")

    @classmethod():
    def save_current_address():

    # Add address record in DB 
    if session != None:
        address = Address(lat=session["lat"], lng=session["lng"], formatted_addy=session["address"])
        db.session.add(address)
        db.session.flush()

    return address


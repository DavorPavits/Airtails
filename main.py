from flask import Flask, render_template, abort, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from sqlalchemy import Integer, String, Text
from forms import CreatePostForm, RegisterForm, CommentForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_ckeditor import CKEditor
from flask_bootstrap import Bootstrap5

app = Flask(__name__)
app.config["SECRET_KEY"] = "secretkey"
ckeditor = CKEditor(app)
Bootstrap5(app)

# Configure Login Manager
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)


#Create the db
class Base(DeclarativeBase):
    pass


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///airtails.db"
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Create a User table for all your registered users
class User(UserMixin, db.Model):
    __tablename__= "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(100))

    #TODO : Create the binomial connections down the road


with app.app_context():
    db.create_all()


#TODO : Register new users into the db
@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # Check if user is already present in the database
        result = db.session.execute(db.select(User).where(User.email == form.email.data))
        user = result.scalar()
        if user:
            flash("You have already signed up with that email, log in instead!")
            return redirect(url_for("login"))

        hash_and_salted_password = generate_password_hash(
            form.password.data,
            method="pbkdf2:sha256",
            salt_length=8
        )

        new_user = User(
            email = form.email.data,
            name = form.name.data,
            password = hash_and_salted_password,
        )

        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        return redirect(url_for("home_page"))
    return render_template("register.html", form=form, current_user=current_user)

@app.route("/")
def home_page():
    return render_template("index.html")


#TODO: Figure the login method
@app.route("/home")
def login():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/flights")
def search_flights():
    return render_template("flights.html")

if __name__ == "__main__":
    app.run(debug=True, port=5001)

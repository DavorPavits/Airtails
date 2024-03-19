from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditorField


#Create a form to register new users
class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = StringField("password", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    submit = SubmitField("Sign me Up!")


#TODO: Create a form for creating a blogpost
class CreatePostForm(FlaskForm):
    pass


#TODO: Create a form to login existing users
class LoginForm(FlaskForm):
    pass


#TODO: Create a form to add comments
class CommentForm(FlaskForm):
    pass

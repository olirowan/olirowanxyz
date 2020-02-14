from app import app, db
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField, SelectMultipleField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, Regexp
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from app.models import User, BlogPostTags, BlogPost


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(message="Please don't leave this field blank.")])
    password = PasswordField('Password', validators=[DataRequired(message="Please don't leave this field blank.")])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(message="Please don't leave this field blank."), Length(min=4, max=32), Regexp(regex='^(?=.*[a-zA-Z])[A-Za-z0-9_]*$', message='Only letters, numbers, and underscores are accepted.')])
    email = StringField('Email', validators=[DataRequired(message="Please don't leave this field blank."), Email(message="Please enter a valid email.")])
    password = PasswordField('Password', validators=[DataRequired(message="Please don't leave this field blank."),
                                                     Length(min=10, max=128, message="Please make sure your password contains at least 10 characters."),
                                                     Regexp(regex="^.*[a-z].*$", message="Please make sure your password contains at least 1 lowercase character."),
                                                     Regexp(regex="^.*[A-Z].*$", message="Please make sure your password contains at least 1 uppercase character."),
                                                     Regexp(regex="^.*[0-9].*$", message="Please make sure your password contains at least 1 number.")
                                                     ])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(message="Please don't leave this field blank."), EqualTo('password', message="Please make sure both passwords are the same.")])
    if app.config['ENVIRONMENT_TYPE'] == 'production':
        recaptcha = RecaptchaField(validators=None)
    submit = SubmitField('Register')

    def validate_username(self, username):
        username_lower = str(username.data).lower()
        user = User.query.filter_by(username_lower=username_lower).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        email_lower = str(email.data).lower()
        user = User.query.filter_by(email=email_lower).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(message="Please don't leave this field blank."), Email(message="Please enter a valid email.")])
    submit = SubmitField('Request Password Reset')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(message="Please don't leave this field blank."), Length(min=10, max=128, message="Please make sure your password contains at least 10 characters.")])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(message="Please don't leave this field blank."), EqualTo('password', message="Please make sure both passwords are the same.")])
    submit = SubmitField('Confirm Reset')


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(message="Please don't leave this field blank."), Length(min=4, max=32)])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):

        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):

        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')


class CreateBlogPost(FlaskForm):
    blog_title = TextAreaField('Title:', validators=[DataRequired(message="Please enter a title.")])
    blog_icon = TextAreaField('Icon:', validators=[DataRequired(message="Please enter an icon.")])
    #blog_tags = SelectField('Tags:', choices=[(str(tag.id), str(tag.blogpost_tag)) for tag in BlogPostTags.tag_names()])
    blog_tags = SelectMultipleField('Tags:', choices=[(str(tag.id), str(tag.blogpost_tag)) for tag in BlogPostTags.tag_names()])
    blog_content = TextAreaField('Content:', validators=[DataRequired(message="Please enter blog content.")])
    submit = SubmitField('Post')

    def validate_blog_title(self, blog_title):
        title_used = BlogPost.query.filter_by(title=blog_title.data).first()
        if title_used is not None:
            raise ValidationError('This title has already been used.')

class PostForm(FlaskForm):
    post = TextAreaField('Create a note', validators=[DataRequired(message="Please don't leave this field blank.")])
    submit = SubmitField('Post')


class CreateTag(FlaskForm):
    tag = TextAreaField('Add tag:', validators=[DataRequired(message="Please don't leave this field blank.")])
    submit = SubmitField('Add')

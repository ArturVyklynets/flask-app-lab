from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, BooleanField, SelectField, DateTimeLocalField, SelectMultipleField
from datetime import datetime as dt
from wtforms.validators import DataRequired , Length

CATEGORIES = [('tech', 'Tech'), ('science', 'Science'), ('lifestyle', 'Lifestyle')]

class PostForm(FlaskForm):
  title = StringField('Title', validators=[DataRequired(), Length(min=2)])
  content = TextAreaField('Content', render_kw={"rows": 5, "cols": 40}, validators=[DataRequired()])
  is_active = BooleanField('Active Post')
  publish_date = DateTimeLocalField('Publish Date',
                           format="%Y-%m-%dT%H:%M", default=dt.now())
  category = SelectField('Category', choices=CATEGORIES, validators=[DataRequired()])
  author_id = SelectField('Author', coerce=int)
  tags = SelectMultipleField("Tags", coerce=int)
  submit = SubmitField('Add Post')
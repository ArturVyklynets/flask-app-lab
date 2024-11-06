from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired , Length

class PostForm(FlaskForm):
  title = StringField('Title', validators=[DataRequired(), Length(min=2)])
  content = TextAreaField('Content', render_kw={"rows": 5, "cols": 5}, validators=[DataRequired()])
  submit = SubmitField('Add Post')
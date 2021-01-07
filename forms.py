from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length


class EnContactForm(FlaskForm):
    title = SelectField("Title", choices=[
                        "Mr.", "Mrs.", "Miss.", "Ms.", "Mx.", "Rev", "Dr."], validators=[DataRequired()])

    first_name = StringField("First Name", validators=[
                             DataRequired(), Length(min=2, max=20)])

    last_name = StringField("Last Name", validators=[
                            DataRequired(), Length(min=2, max=20)])

    email = StringField("Email", validators=[DataRequired(), Email()])

    subject = SelectField("Subject", choices=[
                          "Product", "Website", "General Enquiry", "Other"], validators=[DataRequired()])

    message = TextAreaField("Message", validators=[
                            DataRequired(), Length(min=2, max=2000)])

    submit = SubmitField()

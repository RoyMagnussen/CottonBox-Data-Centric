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


class CheckoutForm(FlaskForm):
    title = SelectField("Title", choices=[
                        "Mr.", "Mrs.", "Miss.", "Ms.", "Mx.", "Rev", "Dr."], validators=[DataRequired()])

    first_name = StringField("First Name", validators=[
                             DataRequired(), Length(min=2, max=20)])

    last_name = StringField("Last Name", validators=[
                            DataRequired(), Length(min=2, max=20)])

    address_line_1 = StringField("Address Line 1", validators=[
                                 DataRequired(), Length(min=1, max=50)])

    address_line_2 = StringField("Address Line 2", validators=[
                                 DataRequired(), Length(min=1, max=50)])

    address_line_3 = StringField("Address Line 3", validators=[
                                 DataRequired(), Length(min=1, max=50)])

    address_line_4 = StringField("Address Line 4", validators=[
                                 DataRequired(), Length(min=1, max=50)])

    post_code = StringField(
        "Post Code/Zip", validators=[DataRequired(), Length(min=2)])

    country = StringField("Country", validators=[
                          DataRequired(), Length(min=2)])

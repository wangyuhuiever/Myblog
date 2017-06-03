#! -*- encoding:utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import Length

class EditProfileForm(FlaskForm):
    name = StringField("姓名", validators=[Length(0, 64)])
    location = StringField("地址", validators=[Length(0, 64)])
    about_me = TextAreaField("关于我")
    submit = SubmitField("确认")

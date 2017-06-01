#! -*- encoding:utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from ..models import User

class RegistrationForm(FlaskForm):
    email = StringField("邮箱",validators=[Required(), Length(1,64), Email()])
    username = StringField("用户名", validators=[Required(), Length(1,64),Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                                              '用户名只能包含字母， 数字，标点和下划线。')])
    password = PasswordField("密码", validators=[Required()])
    password2 = PasswordField("确认密码", validators=[Required(), EqualTo('password', message="两次密码必须一致")])
    submit = SubmitField("提交")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱已被注册')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已存在')

class LoginForm(FlaskForm):
    email = StringField("邮箱", validators=[Required(), Length(1, 64), Email()])
    password = PasswordField("密码", validators=[Required()])
    remember_me = BooleanField("记住我")
    submit = SubmitField("登录")
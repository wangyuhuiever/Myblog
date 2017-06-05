#! -*- encoding:utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, BooleanField, SelectField, ValidationError
from wtforms.validators import Length, Required, Regexp, Email
from ..models import Role, User
from flask_pagedown.fields import PageDownField

class EditProfileForm(FlaskForm):
    name = StringField("姓名", validators=[Length(0, 64)])
    location = StringField("地址", validators=[Length(0, 64)])
    about_me = TextAreaField("关于我")
    submit = SubmitField("确认")

class EditProfileAdminForm(FlaskForm):
    email = StringField("邮箱", validators=[Required(), Length(1, 64), Email()])
    username = StringField("用户名", validators=[Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,'用户名必须使用数字，字母，小数点和下划线。')])
    confirmed = BooleanField("验证")
    role = SelectField("角色", coerce=int)
    name = StringField("姓名", validators=[Length(0, 64)])
    location = StringField("地址", validators=[Length(0, 64)])
    about_me = TextAreaField("关于我")
    submit = SubmitField("确认")

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已被注册')

    def validate_username(self, field):
        if field.data != self.user.username and User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已存在')

class PostForm(FlaskForm):
    body = PageDownField('记录一下发生的事情吧', validators=[Required()])
    submit = SubmitField("提交")

class CommentForm(FlaskForm):
    body = StringField('输入评论', validators=[Required()])
    submit = SubmitField('提交')
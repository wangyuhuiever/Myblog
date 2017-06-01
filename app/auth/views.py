#! -*- encoding:utf-8 -*-
from . import auth
from .forms import RegistrationForm, LoginForm
from flask import render_template, redirect, url_for, request, flash
from .. import db
from ..models import User
from ..email import send_email
from flask_login import login_required, current_user, login_user, logout_user

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, '验证邮箱','auth/email/confirm',
                   user=user, token=token)
        flash('邮件已经发送至你的邮箱，请点击完成注册。')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('恭喜你，验证通过！')
    else:
        flash('对不起，链接错误！')
    return redirect(url_for('main.index'))

@auth.route('/confirm')
@login_required
def resend_confirm():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, "验证邮箱", 'auth/email/confirm',
               user=current_user, token=token)
    flash("一封新的邮件已经发送至你的邮箱，请注意查收。")
    return redirect(url_for('main.index'))

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('用户名或密码错误！')
    return render_template('auth/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('你已经退出了登录')
    return redirect(url_for('main.index'))
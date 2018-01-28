# !/usr/bin/env python
# coding:utf-8
# author bai
from wtforms import Form, BooleanField, TextField, PasswordField, validators, widgets
from wtforms.fields import simple, html5


class LoingForm(Form):
    username = TextField(label='Username',
                         validators=[
                             validators.DataRequired(message='用户名必填'),
                             validators.Length(min=4, max=16, message='用户名需最少4个字符，最大16个字符'),
                         ],
                         widget=widgets.TextInput(),
                         render_kw={'class': 'form-control'}
                         )
    password = simple.PasswordField(
        label='密码',
        validators=[
            validators.DataRequired(message='密码不能为空'),
            validators.Length(min=3, max=16, message='密码最少3个字符，最大16个字符')
        ],
        widget=widgets.PasswordInput(),
        render_kw={'class': 'form-control'}
    )

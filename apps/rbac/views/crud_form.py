
from wtforms import Form, BooleanField, TextField, PasswordField, validators, widgets
from wtforms.fields import simple, html5

# 菜单相关
# 根据每个model表中的字段，生成form类，然后再根据form类来
class Menu_form(Form):
    title = TextField(
        label='title',
        validators=[
            validators.DataRequired(message='菜单不能为空'),
            validators.Length(min=3,max=8,message='菜单最少3个字符，最大16个字符')
        ],
        widget=widgets.FileInput(),
        render_kw={'class':'form-control'}
    )
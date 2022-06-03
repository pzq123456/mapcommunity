from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,IntegerField,FloatField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User

from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length,NumberRange

#调用WTF库 创建登录表单
class LoginForm(FlaskForm): # 用户登录表单
    username = StringField('用 户 名：', validators=[DataRequired()])#DataRequired()验证内容是否为空
    password = PasswordField('密 码：', validators=[DataRequired()])
    remember_me = BooleanField('记 住 我')
    submit = SubmitField('登 录')


class RegistrationForm(FlaskForm): # 用户注册表单
    username = StringField('用 户 名：', validators=[DataRequired()])
    email = StringField('邮 箱：', validators=[DataRequired(), Email()])
    password = PasswordField('密 码：', validators=[DataRequired()])
    password2 = PasswordField('确 认 密 码：'
                                    , validators=[DataRequired()
                                                    , EqualTo('password')])
    submit = SubmitField('注 册')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('已存在该用户名！请换一个！')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('该邮箱地址已被注册！请换一个！')


class EditProfileForm(FlaskForm): # 用户编辑资料表单
    username = StringField('用 户 名：', validators=[DataRequired()])
    about_me = TextAreaField('个 性 签 名：', validators=[Length(min=0, max=140)])
    submit = SubmitField('提 交')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('该用户名已存在，请换一个。')

class PostForm(FlaskForm): # 用户发帖表单
    lon =FloatField('经 度',validators=[
        DataRequired(),NumberRange(-180,180)])#经度
    lat = FloatField('纬 度',validators=[
        DataRequired(),NumberRange(-90,90)]) #纬度
    post = TextAreaField('帖 子 内 容：', validators=[
        DataRequired(), Length(min=1, max=800)])
    
    submit = SubmitField('发布')



# 跟帖表单需要跟在某一个具体的帖子后面
class CommentForm(FlaskForm): # 用户跟帖表单
    post_num=IntegerField('帖子编号：',validators=[
        DataRequired()])
    comment = TextAreaField('评 论：', validators=[
        DataRequired(), Length(min=5, max=140)])
    submit = SubmitField('发布评论')
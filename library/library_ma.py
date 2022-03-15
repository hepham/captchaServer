from .extension import ma


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'password', 'merchant_key', 'count_captcha')

from .extension import ma


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id','fullname','username', 'password', 'merchant_key', 'count_captcha')

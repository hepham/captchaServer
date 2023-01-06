from .extension import ma


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id','created_by','last_modified_by', 'activation', 'first_name', 'image_url','lang_key','lastName','last_name','login','email','password_hash')
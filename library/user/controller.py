from flask import Blueprint
from flask_cors import cross_origin

from .services import (get_infor_by_id_service, sign_up_service, get_all_service, change_key, update_captcha_number,
                       sign_in)

users = Blueprint("users", __name__)


# get all users
@users.route("/users", methods=['GET'])
@cross_origin()
def get_all_user():
    return get_all_service()


# register
@users.route("/users/register", methods=['POST'])
@cross_origin()
def register():
    return sign_up_service()


# get user by id

@users.route("/users/<int:id>", methods=['GET'])
@cross_origin()
def get_user_by_id(id):
    return get_infor_by_id_service(id)


# change key
@users.route("/users/changekey/<int:id>", methods=['GET'])
def update_book_by_id(id):
    return change_key(id)


@users.route("/users/captcha/<int:id>", methods=['PUT'])
def update_capcha_by_id(id):
    return update_captcha_number(id)


@users.route("/users/signin", methods=['POST'])
@cross_origin()
def signin():
    return sign_in()

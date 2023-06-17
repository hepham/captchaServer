from flask import Blueprint
from flask_cors import cross_origin

from .services import (get_infor_by_id_service, sign_up_service, get_all_service, change_key, update_captcha_number,
                       sign_in,predict,predict2,solve,solve2,test)
from .services2 import (solvedetectApi,test,solveCaptchaApi)
import flask
print(flask.__version__)
users = Blueprint("users", __name__)


# get all users
# @users.route("/users", methods=['GET'])
# @cross_origin()
# def get_all_user():
#     return get_all_service()


# # register
# @users.route("/users/register", methods=['POST'])
# @cross_origin()
# def register():
#     return sign_up_service()


# # get user by id

# @users.route("/users/<int:id>", methods=['GET'])
# @cross_origin()
# def get_user_by_id(id):
#     return get_infor_by_id_service(id)


# # change key
# @users.route("/users/changekey", methods=['POST'])
# def update_captcha_by_merchant_key():
#     return change_key()


# @users.route("/users/captcha/updateNumber", methods=['POST'])
# def update_capcha_by_id():
#     return update_captcha_number()


# @users.route("/users/signin", methods=['POST'])
# @cross_origin()
# def signin():
#     return sign_in()
@users.route('/detect',methods=['POST'])
@cross_origin()
def encode():
    return solvedetectApi()

# @users.route('/captcha',methods=['POST'])
# @cross_origin()
# def encode2():
#     return solve()
@users.route('/captcha',methods=['POST'])
@cross_origin()
def encode3():
    return solveCaptchaApi()
    
@users.route('/test',methods=['POST'])
@cross_origin()
def encode4():
    return test()
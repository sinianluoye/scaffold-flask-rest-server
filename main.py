import config
from flask import Flask, Blueprint, jsonify
from utils.logger import logger
from flask import Flask
from controller import UserController
from service import UserService
from utils.security import generate_random_password, compute_md5
from model.basic import is_db_exist, init_databse, ModelBase
from flask_cors import CORS


app = Flask(__name__)

app.register_blueprint(UserController.blueprint)

CORS(app, supports_credentials=True)


@app.errorhandler(Exception)
def handle_exception(e):
    return jsonify({
        "code": -1,
        "message": f"unexpected error, {e}"
    })

def __init_admin():
    if UserService.get_user_count() == 0:
        password = generate_random_password(config.DEFAULT_ADMIN_PASSWORD_LENGTH)
        UserService.create_user(config.DEFAULT_ADMIN_USER_NAME, password)
        print(f"\033[1;31madmin user created:\n\tusername: {config.DEFAULT_ADMIN_USER_NAME}\n\tpassword: {password}\033[0m")

def __init_database():
    init_databse()

def __init_server():
    if not is_db_exist():
        __init_database()
    __init_admin()


@logger.log_aop(
        level=config.LOG_LEVEL_INFO, 
        project_name=config.RPOJECT_NAME,
        show_error_trace_stack=True,
        host=config.HOST, 
        port=config.PORT,
        debug_mode=config.DEBUG_MODE)
def main():
    __init_server()
    app.run(debug=config.DEBUG_MODE, host=config.HOST, port=config.PORT)
  
if __name__ == "__main__":
    main()
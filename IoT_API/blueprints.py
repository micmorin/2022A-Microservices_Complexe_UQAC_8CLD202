from flask import Blueprint
import controller as c

main = Blueprint('main',__name__, url_prefix="/")

main.route("/",                                 methods=['POST'])            (c.main_register)
main.route("/confirm",                          methods=['POST'])            (c.main_confirm)
main.route("/test",                             methods=['GET'])             (c.main_test)
main.route("/init_db",                          methods=['GET'])             (c.main_init)
main.route("/analytics",                        methods=['GET'])             (c.main_analytics)

data = Blueprint('data', __name__,url_prefix="/data")

data.route("/create",                          methods=['POST'])           (c.data_create)
data.route("/delete",                          methods=['DELETE'])         (c.data_delete)
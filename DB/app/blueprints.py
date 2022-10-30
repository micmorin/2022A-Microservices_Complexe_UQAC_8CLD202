from flask import Blueprint
import controller as c

main = Blueprint('main',__name__, url_prefix="/")

main.route("/",                                 methods=['GET'])            (c.main_index)
main.route("/login",                            methods=['POST'])           (c.main_login)

user = Blueprint('user', __name__,url_prefix="/users")

user.route("/",                                methods=['GET'])            (c.user_index)
user.route("/create",                          methods=['POST'])           (c.user_create)
user.route("/update",                          methods=['PUT'])            (c.user_update)
user.route("/delete",                          methods=['DELETE'])         (c.user_delete)

profil = Blueprint('profil', __name__,url_prefix="/profils")

profil.route("/",                              methods=['GET'])            (c.profil_index)
profil.route("/create",                        methods=['POST'])           (c.profil_create)
profil.route("/update",                        methods=['PUT'])            (c.profil_update)
profil.route("/delete",                        methods=['DELETE'])         (c.profil_delete)

calcul = Blueprint('calcul', __name__,url_prefix="/calculs")

calcul.route("/",                              methods=['POST'])           (c.calcul_index)
calcul.route("/delete",                        methods=['DELETE'])         (c.calcul_delete)

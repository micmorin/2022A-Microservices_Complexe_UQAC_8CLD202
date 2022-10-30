from flask import Blueprint
import controller as c

main = Blueprint('main',__name__, url_prefix="/")

main.route("/",                                 methods=['GET'])            (c.main_index)
main.route("/login",                            methods=['GET', 'POST'])    (c.main_login)
main.route("/logout",                           methods=['GET'])            (c.main_logout)

user = Blueprint('user', __name__,url_prefix="/users")

user.route('/',                                 methods=['GET'])            (c.user_index)
user.route('/create',                           methods=['GET','POST'])     (c.user_create)
user.route('/edit/<int:user_id>',               methods=['POST'])           (c.user_update)
user.route('/<int:user_id>',                    methods=['POST'])           (c.user_destroy)

profil = Blueprint('profil', __name__,url_prefix="/profils")

profil.route('/',                               methods=['GET'])            (c.profil_index)
profil.route('/create',                         methods=['POST'])           (c.profil_create)
profil.route('/edit/<int:profil_id>',           methods=['POST'])           (c.profil_update)
profil.route('/<int:profil_id>',                methods=['POST'])           (c.profil_destroy)

calcul = Blueprint('calcul', __name__,url_prefix="/calculs")

calcul.route('/',                               methods=['GET'])            (c.calcul_index)
calcul.route('/<int:calcul_id>',                methods=['POST'])           (c.calcul_destroy)
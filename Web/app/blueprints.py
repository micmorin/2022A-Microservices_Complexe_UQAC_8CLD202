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

object = Blueprint('object', __name__,url_prefix="/objects")

object.route('/edit/<int:object_id>',           methods=['POST'])           (c.object_update)

simulator = Blueprint('simulator', __name__,url_prefix="/simulator")

simulator.route('/',                            methods=['GET'])            (c.simulator_index)
from flask import request

from flask import (
    Blueprint
)

from . import services
import json

bp = Blueprint('airdrop', __name__, url_prefix='/airdrop')

@bp.route('/monster_holder', methods=["GET"])
def monster_holder():
    base = request.args.get('page', 200)
    # endblock = request.args.get('endblock', '')

    items = services.get_monster_holders()
    
    return json.dumps([{
        'index': i+1, 'address': e.holder_address, 'count': e.count, 
        'amount': services.cal_monster_holder_rewards(e.count, int(base))} for i, e in enumerate(items)])

@bp.route('/dungeons_interaction', methods=["GET"])
def dungeons_interaction():
    base = request.args.get('page', 50)

    items = services.get_dungeons_interactions()
    
    return json.dumps([{
        'index': i+1, 'address': e.called_from, 'count': e.count, 
        'amount': services.cal_dungeons_interaction_rewards(e.count, int(base))} for i, e in enumerate(items)])
from deta import Deta
import os

from flask import (
    Blueprint, jsonify
)

bp = Blueprint('dungeons', __name__, url_prefix='/dungeons')


@bp.route('/monster_coppers', methods=["GET"])
def monster_coppers():
    deta = Deta(os.getenv('DETA_SECRET'))
    monsterCoppers = deta.Base("monster_coppers")

    res = monsterCoppers.fetch().items
    res.sort(key=lambda x: x['count'], reverse=True)
    
    return jsonify(res[0:30])

@bp.route('/summoner_coppers', methods=["GET"])
def summoner_coppers():
    deta = Deta(os.getenv('DETA_SECRET'))
    db = deta.Base("summoner_coppers")

    res = db.fetch().items
    res.sort(key=lambda x: x['copper_count'], reverse=True)
    
    return jsonify(res[0:30])

@bp.route('/summoner_play_count', methods=["GET"])
def summoner_play_count():
    deta = Deta(os.getenv('DETA_SECRET'))
    db = deta.Base("summoner_coppers")

    res = db.fetch().items
    res.sort(key=lambda x: x['play_count'], reverse=True)
    
    return jsonify(res[0:30])
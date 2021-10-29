from flask import request

from flask import (
    Blueprint, jsonify
)

from .models import DungeonsSummonerStat, DungeonsFirstAdventure, DungeonsMonsterCoppers

bp = Blueprint('dungeons', __name__, url_prefix='/dungeons')


@bp.route('/monster_coppers', methods=["GET"])
def monster_coppers():
    items = DungeonsMonsterCoppers.query.order_by(DungeonsMonsterCoppers.copper_coins.desc()).limit(30).all()
    
    return jsonify([i.serialize for i in items])

@bp.route('/summoner_coppers', methods=["GET"])
def summoner_coppers():
    items = DungeonsSummonerStat.query.order_by(DungeonsSummonerStat.copper_coins.desc()).limit(30).all()
    
    return jsonify([i.serialize for i in items])

@bp.route('/summoner_play_count', methods=["GET"])
def summoner_play_count():
    items = DungeonsSummonerStat.query.order_by(DungeonsSummonerStat.plays_count.desc()).limit(30).all()
    
    return jsonify([i.serialize for i in items])

@bp.route('/adventure_history', methods=["GET"])
def adventure_history():
    page_size = request.args.get('page_size', 20)
    page = request.args.get('page', 0)

    lastid = request.args.get('lastid', 0)

    items = DungeonsFirstAdventure.query.filter(DungeonsFirstAdventure.id>int(lastid)).\
        order_by(DungeonsFirstAdventure.id.desc()).offset(int(page)*int(page_size)).limit(int(page_size)).all()
    
    return jsonify([i.serialize for i in items])
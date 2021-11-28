from flask import request

from flask import (
    Blueprint, jsonify
)

from .models import MonsterList, MonsterNFTHolder
from flaskr.dungeons.models import DungeonsMonsterCoppers
import json

bp = Blueprint('monsters', __name__, url_prefix='/monsters')


@bp.route('/monster_list', methods=["GET"])
def monster_list():
    page_size = request.args.get('page_size', 20)
    page = request.args.get('page', 0)

    items = MonsterList.query.\
        join(DungeonsMonsterCoppers, MonsterList.token_id==DungeonsMonsterCoppers.monster_tokenid, isouter=True).\
        order_by(MonsterList.id.desc()).offset(int(page)*int(page_size)).limit(int(page_size)).all()
    
    return jsonify([i.serialize for i in items])


@bp.route('/get_monster', methods=["GET"])
def get_monster():
    tokenid = request.args.get('tokenid', 0)

    obj = MonsterList.query.filter_by(token_id=tokenid).first()
    
    return jsonify(obj.serialize)


@bp.route('/get_mine_monster', methods=["GET"])
def get_mine_monster():
    address = request.args.get('address', '')

    items = MonsterNFTHolder.query.filter_by(holder_address=address.lower()).all()
    
    return jsonify([i.serialize for i in items])



@bp.route('/totalsupply', methods=["GET"])
def totalsupply():
    
    return '100,000,000'


@bp.route('/circulating', methods=["GET"])
def circulating():
    
    return '1,000,000'

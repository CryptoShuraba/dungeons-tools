from flask import request

from flask import (
    Blueprint, jsonify
)

from .models import MonsterList

bp = Blueprint('monsters', __name__, url_prefix='/monsters')


@bp.route('/monster_list', methods=["GET"])
def monster_list():
    page_size = request.args.get('page_size', 20)
    page = request.args.get('page', 0)

    items = MonsterList.query.\
        order_by(MonsterList.id.desc()).offset(int(page)*int(page_size)).limit(int(page_size)).all()
    
    return jsonify([i.serialize for i in items])


@bp.route('/get_monster', methods=["GET"])
def get_monster():
    tokenid = request.args.get('tokenid', 0)

    obj = MonsterList.query.filter_by(token_id=tokenid).first()
    
    return jsonify(obj.serialize)
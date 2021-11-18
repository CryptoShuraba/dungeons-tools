from .models import MonsterNFTHolder
from flaskr import db
from sqlalchemy import desc

def get_the_first_airdrop_array():

    return db.session.query(
        MonsterNFTHolder.holder_address, db.func.count().label('count')
    ).group_by(MonsterNFTHolder.holder_address).order_by(desc('count')).all()
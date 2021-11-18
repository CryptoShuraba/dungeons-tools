from .models import MonsterNFTHolder
from flaskr import db
from sqlalchemy import desc


def cal_rewards(num, base):
    rewards = 0
    if num < 1:
        return    
    if num > 20:
        rewards += (num - 20) * base * 0.5 
        num = 20
    if num > 10:
        rewards += (num - 10) * base * 0.6
        num = 10
    if num > 5:
        rewards += (num - 5) * base * 0.8
        num = 5
    rewards += num * base * 1
        
    return rewards


def get_the_first_airdrop_array():
    return db.session.query(
        MonsterNFTHolder.holder_address, db.func.count().label('count')
    ).group_by(MonsterNFTHolder.holder_address).order_by(desc('count')).all()
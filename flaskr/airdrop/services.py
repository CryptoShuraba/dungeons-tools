from flaskr.monster.models import MonsterNFTHolder
from flaskr.dungeons.models import DungeonsFirstAdventure
from flaskr.rarity.models import RarityNFTHolder
from flaskr import db
from sqlalchemy import desc


def cal_monster_holder_rewards(num, base):
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

def cal_dungeons_interaction_rewards(num, base):
    rewards = 0
    if num < 1:
        return    
    elif num > 5:
        rewards = base * 2
    else:
        rewards = base
        
    return rewards


def cal_rarity_holder_rewards(maxLevel, base):
    rewards = 0
    if maxLevel == 3:
        rewards = base    
    elif maxLevel > 3:
        rewards = base * 2 
        
    return rewards


def get_monster_holders(endblock):
    return db.session.query(
        MonsterNFTHolder.holder_address, db.func.count().label('count')
    ).filter(MonsterNFTHolder.block_number<=endblock).group_by(MonsterNFTHolder.holder_address).order_by(desc('count')).all()


def get_dungeons_interactions(endblock):
    return db.session.query(
        DungeonsFirstAdventure.called_from, db.func.count().label('count')
    ).filter(DungeonsFirstAdventure.blocknum<=endblock).group_by(DungeonsFirstAdventure.called_from).order_by(desc('count')).all()


def get_rarity_holders():
    return db.session.query(
        RarityNFTHolder.holder_address, db.func.max(RarityNFTHolder.summoner_level).label('max_level')
    ).filter(RarityNFTHolder.summoner_level>2).group_by(RarityNFTHolder.holder_address).order_by(desc('max_level')).all()

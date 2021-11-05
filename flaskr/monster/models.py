from enum import unique
from .. import db


class MonsterList(db.Model):
    __tablename__ = 'monster_list'

    id = db.Column(db.BigInteger, primary_key=True)
    token_id = db.Column(db.Integer, unique=True)

    suffix = db.Column(db.Integer)
    profession = db.Column(db.String(50), default='')
    monster = db.Column(db.String(50), default='')
    prefix = db.Column(db.String(50), default='')
    token_uri = db.Column(db.String(5000), default='')
    
    health_point = db.Column(db.Integer)
    physical_damage_point = db.Column(db.Integer)
    magical_damage_point = db.Column(db.Integer)
    physical_defence = db.Column(db.Integer)
    magical_defence = db.Column(db.Integer)
    dodge = db.Column(db.Integer)
    hit = db.Column(db.Integer)
    critical = db.Column(db.Integer)
    parry = db.Column(db.Integer)
    created = db.Column(db.DateTime)
    updated = db.Column(db.DateTime)
    
    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    @property
    def serialize(self):
        return {
            'token_id': self.token_id,
            'monster': self.monster,
            'prefix': self.prefix,
            'profession': self.profession,
            'token_uri': self.token_uri,
            'health_point': self.health_point,
            'physical_damage_point': self.physical_damage_point,
            'magical_damage_point': self.magical_damage_point,
            'physical_defence': self.physical_defence,
            'magical_defence': self.magical_defence,
            'dodge': self.dodge,
            'hit': self.hit,
            'critical': self.critical,
            'parry': self.parry
        }

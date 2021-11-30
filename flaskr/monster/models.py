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
    dungeonsMonsterCoppers = db.relationship('DungeonsMonsterCoppers', uselist=False, backref="monsterlist")
    
    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    @property
    def serialize(self):
        return {
            'token_id': self.token_id,
            'monster': self.monster,
            'prefix': self.prefix,
            'profession': self.profession,
            'health_point': self.health_point,
            'physical_damage_point': self.physical_damage_point,
            'magical_damage_point': self.magical_damage_point,
            'physical_defence': self.physical_defence,
            'magical_defence': self.magical_defence,
            'dodge': self.dodge,
            'hit': self.hit,
            'critical': self.critical,
            'parry': self.parry,
            'token_uri': self.token_uri,
            'copper_coins': self.dungeonsMonsterCoppers.copper_coins if self.dungeonsMonsterCoppers else 0
        }


class MonsterNFTTracker(db.Model):
    __tablename__ = 'monster_nft_tracker'

    id = db.Column(db.BigInteger, primary_key=True)

    block_number = db.Column(db.BigInteger, default=0)
    time_stamp = db.Column(db.String(50))
    txhash = db.Column(db.String(100), unique=True)
    nonce = db.Column(db.String(50))
    block_hash = db.Column(db.String(100))
    from_address = db.Column(db.String(100))
    contract_address = db.Column(db.String(100))
    to_address = db.Column(db.String(100))
    token_id = db.Column(db.Integer)
    token_name = db.Column(db.String(50))
    token_symbol = db.Column(db.String(50))
    transaction_index = db.Column(db.String(50))
    confirmations = db.Column(db.String(50))

    created = db.Column(db.DateTime)
    updated = db.Column(db.DateTime)

    def __repr__(self):
        return '<id {}>'.format(self.id)


class MonsterNFTHolder(db.Model):
    __tablename__ = 'monster_nft_holder'

    id = db.Column(db.BigInteger, primary_key=True)

    holder_address = db.Column(db.String(100))
    token_id = db.Column(db.Integer, db.ForeignKey('monster_list.token_id'), unique=True)
    block_number = db.Column(db.BigInteger, default=0)

    created = db.Column(db.DateTime)
    updated = db.Column(db.DateTime)

    def __repr__(self):
        return '<id {}>'.format(self.id)

    @property
    def serialize(self):
        return {
            'token_id': self.token_id,
        }
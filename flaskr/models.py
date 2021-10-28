from . import db


class DungeonsFirstAdventure(db.Model):
    __tablename__ = 'dungeons_first_adventure'

    id = db.Column(db.BigInteger, primary_key=True)
    txhash = db.Column(db.String(200), unique=True)
    blocknum = db.Column(db.String(200))
    summoner_tokenid = db.Column(db.BigInteger)
    monster_tokenid = db.Column(db.BigInteger)
    summoner_class = db.Column(db.Integer)
    copper_coins = db.Column(db.Integer)
    is_summoner_win = db.Column(db.String(1))
    created = db.Column(db.DateTime)
    updated = db.Column(db.DateTime)

    def __init__(self, txhash, blocknum, summoner_tokenid, monster_tokenid, summoner_class, copper_coins, is_summoner_win, created, updated):
        self.txhash = txhash
        self.blocknum = blocknum
        self.summoner_tokenid = summoner_tokenid
        self.monster_tokenid = monster_tokenid
        self.summoner_class = summoner_class
        self.copper_coins = copper_coins
        self.is_summoner_win = is_summoner_win
        self.created = created
        self.updated = updated

    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    @property
    def serialize(self):
        return {
            'id': self.id, 
            'txhash': self.txhash,
            'blocknum': self.blocknum,
            'summoner_tokenid':self.summoner_tokenid,
            'monster_tokenid': self.monster_tokenid,
            'summoner_class': self.summoner_class,
            'copper_coins': self.copper_coins,
            'is_summoner_win': self.is_summoner_win
        }


class DungeonsSummonerStat(db.Model):
    __tablename__ = 'dungeons_summoner_stat'

    id = db.Column(db.BigInteger, primary_key=True)
    summoner_tokenid = db.Column(db.BigInteger, unique=True)
    summoner_class = db.Column(db.Integer)
    copper_coins = db.Column(db.Integer)
    wins_count = db.Column(db.Integer)
    plays_count = db.Column(db.Integer)
    created = db.Column(db.DateTime)
    updated = db.Column(db.DateTime)

    def __init__(self, summoner_tokenid, summoner_class, copper_coins, wins_count, plays_count, created, updated):
        self.summoner_tokenid = summoner_tokenid
        self.summoner_class = summoner_class
        self.copper_coins = copper_coins
        self.wins_count = wins_count
        self.plays_count = plays_count
        self.created = created
        self.updated = updated

    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    @property
    def serialize(self):
        return {
            'id': self.id, 
            'summoner_tokenid': self.summoner_tokenid,
            'summoner_class': self.summoner_class,
            'copper_coins':self.copper_coins,
            'wins_count': self.wins_count,
            'plays_count': self.plays_count,
        }


class DungeonsTrack(db.Model):
    __tablename__ = 'dungeons_track'

    id = db.Column(db.BigInteger, primary_key=True)
    key = db.Column(db.String(50), unique=True)
    value = db.Column(db.String(200), default='0')
    created = db.Column(db.DateTime)
    updated = db.Column(db.DateTime)

    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    @property
    def serialize(self):
        return {
            'id': self.id, 
            'key': self.key,
            'value': self.value
        }


class DungeonsMonsterCoppers(db.Model):
    __tablename__ = 'dungeons_monster_coppers'

    id = db.Column(db.BigInteger, primary_key=True)
    monster_tokenid = db.Column(db.BigInteger, unique=True)
    monster = db.Column(db.String(50), default='')
    prefix = db.Column(db.String(50), default='')
    suffix = db.Column(db.String(50), default='')
    copper_coins = db.Column(db.BigInteger)
    profession = db.Column(db.String(50), default='')
    created = db.Column(db.DateTime)
    updated = db.Column(db.DateTime)

    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    @property
    def serialize(self):
        return {
            'id': self.id, 
            'monster_tokenid': self.monster_tokenid,
            'monster': self.monster,
            'prefix': self.prefix,
            'suffix': self.suffix,
            'copper_coins': self.copper_coins,
            'profession': self.profession
        }

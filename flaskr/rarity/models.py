from enum import unique
from .. import db


class RarityNFTTracker(db.Model):
    __tablename__ = 'rarity_nft_tracker'

    id = db.Column(db.BigInteger, primary_key=True)

    block_number = db.Column(db.String(50))
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


class RarityNFTHolder(db.Model):
    __tablename__ = 'rarity_nft_holder'

    id = db.Column(db.BigInteger, primary_key=True)

    holder_address = db.Column(db.String(100))
    token_id = db.Column(db.Integer, db.ForeignKey('monster_list.token_id'), unique=True)

    created = db.Column(db.DateTime)
    updated = db.Column(db.DateTime)

    def __repr__(self):
        return '<id {}>'.format(self.id)

    @property
    def serialize(self):
        return {
            'token_id': self.token_id,
        }
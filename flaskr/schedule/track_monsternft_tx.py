import traceback
from flaskr import scheduler
from web3 import Web3
import os
from flaskr import db
from datetime import datetime

from flaskr.monster.models import MonsterList, MonsterNFTTracker, MonsterNFTHolder
from flaskr.dungeons.models import DungeonsTrack
import requests
import json


module = 'account'
action = 'tokennfttx'
address = '0x2D2f7462197d4cfEB6491e254a16D3fb2d2030EE'
apikey = os.getenv('FTM_APIKEY')
ftmapi = 'https://api.ftmscan.com/api?module={}&action={}&contractaddress={}&startblock={}&sort=asc&apikey={}'
trackKey = '30EE-last-block'


def get_track_blocknum():
    obj = DungeonsTrack.query.filter_by(key=trackKey).first()
    if not obj:
        obj = DungeonsTrack(key=trackKey, value='0', created=datetime.now(), updated=datetime.now())
        db.session.add(obj)
        db.session.commit()
        return '0'
    return obj.value


def put_track_blocknum(blocknum):
    obj = DungeonsTrack.query.filter_by(key=trackKey).first()
    obj.value = blocknum
    obj.updated = datetime.now()
    db.session.commit()

def update_monster_nft_holder(tokenId, holder):
    obj = MonsterNFTHolder.query.filter_by(token_id=tokenId).first()
    now = datetime.now()
    if not obj:
        obj = MonsterNFTHolder(token_id=tokenId, holder_address=holder, created=now, updated=now)
        db.session.add(obj)
    elif obj.holder_address != holder:
        obj.holder_address = holder
        obj.updated = now


@scheduler.task('interval', id='do_job_3', seconds=5)
def track_monsternft_contract_tx():
    with scheduler.app.app_context():
        blockNumber = get_track_blocknum()
        print("track_monsternft_contract_tx Start Block: {}".format(blockNumber))

        url = ftmapi.format(module, action, address, blockNumber, apikey)
        res = requests.get(url)
        results = json.loads(res.content)['result']

        if len(results) == 0:
            return

        for r in results:
            try:
                mnt = MonsterNFTTracker()
                mnt.block_number = r['blockNumber']
                mnt.time_stamp = r['timeStamp']
                mnt.txhash = r['hash']
                mnt.nonce = r['nonce']
                mnt.block_hash = r['blockHash']
                mnt.from_address = r['from']
                mnt.contract_address = r['contractAddress']
                mnt.to_address = r['to']
                mnt.token_id = r['tokenID']
                mnt.token_name = r['tokenName']
                mnt.token_symbol = r['tokenSymbol']
                mnt.transaction_index = r['transactionIndex']
                mnt.confirmations = r['confirmations']
                now = datetime.now()
                mnt.updated = now
                mnt.created = now

                # insert to table MonsterNFTTracker
                obj = MonsterNFTTracker.query.filter_by(txhash=r['hash']).first()
                if obj:
                    continue

                db.session.add(mnt)
                # update table monster_nft_holder if transfer
                update_monster_nft_holder(mnt.token_id, mnt.to_address)
                db.session.commit()

                blockNumber = mnt.block_number
            except:
                put_track_blocknum(blockNumber)
                traceback.print_exc()
                break

        print("track_monsternft_contract_tx End Block: {}".format(blockNumber))
        put_track_blocknum(blockNumber)

        return 'ok'

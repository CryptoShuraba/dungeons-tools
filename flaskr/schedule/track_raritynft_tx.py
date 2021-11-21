import traceback
from flaskr import scheduler
import os
from flaskr import db
from datetime import datetime

from flaskr.rarity.models import RarityNFTTracker, RarityNFTHolder
from flaskr.dungeons.models import DungeonsTrack
import requests
import json


module = 'account'
action = 'tokennfttx'
address = '0xce761D788DF608BD21bdd59d6f4B54b2e27F25Bb'
apikey = os.getenv('FTM_APIKEY')
# track 1000 items per page
# avoid to use startblock and endblock as parmas to retrieve, will leads to timeout 
ftmapi = 'https://api.ftmscan.com/api?module={}&action={}&contractaddress={}&page={}&offset=1000&sort=asc&apikey={}'
trackKey = 'rarity-transfer-events-last-page'


def get_track_pagenum():
    obj = DungeonsTrack.query.filter_by(key=trackKey).first()
    if not obj:
        obj = DungeonsTrack(key=trackKey, value='1', created=datetime.now(), updated=datetime.now())
        db.session.add(obj)
        db.session.commit()
        return '1'
    return obj.value


def put_track_blocknum(pageNum):
    obj = DungeonsTrack.query.filter_by(key=trackKey).first()
    obj.value = pageNum
    obj.updated = datetime.now()

def update_nft_holder(tokenId, holder):
    obj = RarityNFTHolder.query.filter_by(token_id=tokenId).first()
    now = datetime.now()
    if not obj:
        obj = RarityNFTHolder(token_id=tokenId, holder_address=holder, created=now, updated=now)
        db.session.add(obj)
    elif obj.holder_address != holder:
        obj.holder_address = holder
        obj.updated = now


# ERC721 - Track Token Transfer Events
@scheduler.task('cron', id='do_job_4', hour=7, minute=16)
def track_raritynft_contract_tx():
    with scheduler.app.app_context():
        pageNumber = get_track_pagenum()
        print("track_raritynft_contract_tx Start page: {}".format(pageNumber))
        while True:
            url = ftmapi.format(module, action, address, pageNumber, apikey)
            res = requests.get(url)
            results = json.loads(res.content)['result']

            if not results or len(results) == 0:
                break

            for r in results:
                try:
                    mnt = RarityNFTTracker()
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

                    # insert to table RarityNFTTracker
                    obj = RarityNFTTracker.query.filter_by(txhash=r['hash']).first()
                    if obj:
                        continue

                    db.session.add(mnt)
                    # update table rarity_nft_holder if transfer
                    # print("the #{} belongs to {}".format(mnt.token_id, mnt.to_address))
                    update_nft_holder(mnt.token_id, mnt.to_address)

                    blockNumber = mnt.block_number
                except:
                    put_track_blocknum(blockNumber)
                    traceback.print_exc()
                    break

            print("track_raritynft_contract_tx End page: {}".format(pageNumber))
            put_track_blocknum(pageNumber)
            db.session.commit()
            pageNumber += 1

        return 'ok'

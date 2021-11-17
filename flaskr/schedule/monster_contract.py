from flaskr import scheduler
from web3 import Web3
import traceback
import os
from flaskr import db
from datetime import datetime

from flaskr.monster.models import MonsterList
from flaskr.dungeons import models
import requests
import json


module = 'account'
action = 'tokennfttx'
address = '0x2D2f7462197d4cfEB6491e254a16D3fb2d2030EE'
apikey = os.getenv('FTM_APIKEY')
ftmapi = 'https://api.ftmscan.com/api?module={}&action={}&address={}&startblock={}&sort=asc&apikey={}'
trackKey = '30EE-last-block'


def get_track_blocknum():
    obj = models.DungeonsTrack.query.filter_by(key=trackKey).first()
    if not obj:
        obj = models.DungeonsTrack(key=trackKey, value='0', created=datetime.now(), updated=datetime.now())
        db.session.add(obj)
        db.session.commit()
        return '0'
    return obj.value


def put_track_blocknum(blocknum):
    obj = models.DungeonsTrack.query.filter_by(key=trackKey).first()
    obj.value = blocknum
    obj.updated = datetime.now()
    db.session.commit()


def put_monster(tokenid, suffix, profession, monster, prefix, token_uri, 
        health_point, physical_damage_point, magical_damage_point, 
        physical_defence, magical_defence, dodge, hit, critical, parry):
    obj = MonsterList.query.filter_by(token_id=tokenid).first()
    if not obj:
        now = datetime.now()
        obj = MonsterList(token_id=tokenid, suffix=suffix, profession=profession, monster=monster,
            prefix=prefix, token_uri=token_uri, health_point=health_point, physical_damage_point=physical_damage_point,
            magical_damage_point=magical_damage_point, physical_defence=physical_defence, magical_defence=magical_defence,
            dodge=dodge, hit=hit, critical=critical, parry=parry, created=now, updated=now)
        db.session.add(obj)
    db.session.commit()


def track_monsternft_contract_tx():
    blockNumber = get_track_blocknum()
    print("Start Block: {}".format(blockNumber))
    newBlockNumeber = blockNumber

    res = requests.get(ftmapi.format(module, action, address, blockNumber, apikey))
    results = json.loads(res.content)['result']

    if len(results) == 0:
        return

    for r in results:
        newBlockNumeber = r['blockNumber']
        timeStamp = r['timeStamp']
        txhash = r['hash']
        nonce = r['nonce']
        blockHash = r['blockHash']
        fromAddress = r['from']
        contractAddress = r['contractAddress']
        toAddress = r['to']
        tokenID = r['tokenID']
        tokenName = r['tokenName']
        tokenSymbol = r['tokenSymbol']
        transactionIndex = r['transactionIndex']
        confirmations = r['confirmations']

        # insert to table
        # put_summoner_stat(summonerTokenID, copperCoins, winsCount, playCount)

    print("End Block: {}".format(newBlockNumeber))
    put_track_blocknum(newBlockNumeber)

    return 'ok'

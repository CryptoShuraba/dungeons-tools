from . import scheduler
from web3 import Web3
import traceback
import requests
import json
import os
from datetime import datetime

from flaskr import db
from flaskr.dungeons import models


monkFirstAdventure = None

copperBox = None

ftmapi = 'https://api.ftmscan.com/api?module=account&action=txlist&address=0xbcedCE1e91dDDA15acFD10D0E55febB21FC6Aa38&startblock={}&page={}&offset=100&sort=asc&apikey=' + os.getenv('FTM_APIKEY')

def count_copper(tokenid):
    copperCoins = copperBox.functions.balanceOfSummoner(tokenid).call()
    if copperCoins > 0:
        copperCoins = copperCoins/1e18
    return copperCoins

def count_wins(tokenid):
    playCount = monkFirstAdventure.functions.adventureCount(tokenid).call()
    winsCount = monkFirstAdventure.functions.winsCount(tokenid).call()
    return winsCount, playCount

def get_result(tokenid, num):
    result = monkFirstAdventure.functions.result(tokenid, num).call()
    isWin = '1' if result[1] else '0'
    return result[0], result[1], isWin

def put_summoner_stat(tokenid, copperCoins, winCount, playCount):
    obj = models.DungeonsSummonerStat.query.filter_by(summoner_tokenid=tokenid).first()
    if not obj:
        obj = models.DungeonsSummonerStat(tokenid, 6, copperCoins, winCount, playCount, datetime.now(), datetime.now())
        db.session.add(obj)
    elif obj.plays_count != playCount:
        obj.copper_coins = copperCoins
        obj.wins_count = winCount
        obj.plays_count = playCount
        obj.updated = datetime.now()
    else:
        return 
    db.session.commit()

def get_track_blocknum():
    obj = models.DungeonsTrack.query.filter_by(key='aa38-last-block').first()
    if not obj:
        obj = models.DungeonsTrack(key='aa38-last-block', value='0', created=datetime.now(), updated=datetime.now())
        db.session.add(obj)
        db.session.commit()
        return '0'
    return obj.value

def put_track_blocknum(blocknum):
    obj = models.DungeonsTrack.query.filter_by(key='aa38-last-block').first()
    obj.value = blocknum
    obj.updated = datetime.now()
    db.session.commit()

def insert_adventure(txhash, blocknum, summoner_tokenid, monster_tokenid, summoner_class, copper_coins, is_summoner_win):
    obj = models.DungeonsFirstAdventure.query.filter_by(txhash=txhash).first()
    if not obj:
        obj = models.DungeonsFirstAdventure(txhash, blocknum, summoner_tokenid, monster_tokenid, summoner_class, copper_coins, is_summoner_win, datetime.now(), datetime.now())
        db.session.add(obj)
        db.session.commit()

def put_monster_coppers(monsterTokenid):
    copperCoins = copperBox.functions.balanceOfMonster(monsterTokenid).call()
    suffix = monsterContract.functions.suffix(monsterTokenid).call()
    prefix = monsterContract.functions.prefix(monsterTokenid).call()
    profession = monsterContract.functions.profession(suffix).call()
    monster = monsterContract.functions.monster(monsterTokenid).call()
    
    print('Monster#{}'.format(monsterTokenid), copperCoins/1e18)
    obj = models.DungeonsMonsterCoppers.query.filter_by(monster_tokenid=monsterTokenid).first()
    if not obj:
        obj = models.DungeonsMonsterCoppers(
            monster_tokenid=monsterTokenid, monster=monster, 
            prefix=prefix, suffix=suffix, copper_coins=copperCoins/1e18,
            profession=profession, created=datetime.now(), updated=datetime.now())
        db.session.add(obj)
    elif copperCoins/1e18 != obj.copper_coins:
        obj.copperCoins = copperCoins/1e18
        obj.updated = datetime.now()
    else:
        return
        
    db.session.commit()

@scheduler.task('interval', id='do_job_1', hours=1)
def stat_summoner_adventure():
    with scheduler.app.app_context():
        w3 = Web3(Web3.HTTPProvider(os.getenv('ANKR_ENDPOINTS')))

        global monkFirstAdventure
        monkFirstAdventure = w3.eth.contract(
            address='0xbcedCE1e91dDDA15acFD10D0E55febB21FC6Aa38',
            abi='[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"summoner","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"monster","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"copper","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"count","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"len","type":"uint256"}],"name":"CombatResult","type":"event"},{"inputs":[{"internalType":"uint256","name":"_score","type":"uint256"}],"name":"ability_modifier","outputs":[{"internalType":"int256","name":"_m","type":"int256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"_summoner","type":"uint256"},{"internalType":"uint256","name":"_monster","type":"uint256"}],"name":"ac","outputs":[{"internalType":"int256","name":"_summonerAC","type":"int256"},{"internalType":"int256","name":"_monsterAC","type":"int256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_summoner","type":"uint256"}],"name":"adventure","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"adventureCount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_round","type":"uint256"},{"internalType":"uint256","name":"_summoner","type":"uint256"},{"internalType":"uint256","name":"_monster","type":"uint256"}],"name":"attack","outputs":[{"internalType":"int256","name":"_summonerAttack","type":"int256"},{"internalType":"int256","name":"_monsterAttack","type":"int256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"baseAttackBonus","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_round","type":"uint256"},{"internalType":"uint256","name":"_summoner","type":"uint256"},{"internalType":"uint256","name":"_monster","type":"uint256"}],"name":"damage","outputs":[{"internalType":"int256","name":"_summonerDamage","type":"int256"},{"internalType":"int256","name":"_monsterDamage","type":"int256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_summoner","type":"uint256"}],"name":"hit_die","outputs":[{"internalType":"int256","name":"_hp","type":"int256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_monster","type":"uint256"}],"name":"hit_die_of_monster","outputs":[{"internalType":"int256","name":"","type":"int256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_summoner","type":"uint256"},{"internalType":"uint256","name":"_monster","type":"uint256"}],"name":"initiative_check","outputs":[{"internalType":"uint8","name":"_order","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"lastAdventure","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"uint256","name":"","type":"uint256"}],"name":"processes","outputs":[{"internalType":"uint256","name":"round","type":"uint256"},{"internalType":"uint8","name":"offence","type":"uint8"},{"internalType":"uint8","name":"defence","type":"uint8"},{"internalType":"int256","name":"damage","type":"int256"},{"internalType":"int256","name":"HP","type":"int256"},{"internalType":"uint8","name":"isAttacked","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"uint256","name":"","type":"uint256"}],"name":"result","outputs":[{"internalType":"uint256","name":"monster","type":"uint256"},{"internalType":"uint256","name":"copper","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"rewards","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_a","type":"uint256"},{"internalType":"uint256","name":"_b","type":"uint256"},{"internalType":"uint256","name":"_dx","type":"uint256"}],"name":"roll","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"unarmedDamage","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"winsCount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]'
        )

        global copperBox
        copperBox = w3.eth.contract(
            address='0x253e55363F9440B532D13C228CB633Bac94F3b7C',
            abi='[{"anonymous":false,"inputs":[{"indexed":false,"internalType":"string","name":"subject","type":"string"},{"indexed":true,"internalType":"uint256","name":"from","type":"uint256"},{"indexed":true,"internalType":"uint256","name":"to","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"string","name":"symbol","type":"string"},{"indexed":false,"internalType":"uint256","name":"index","type":"uint256"},{"indexed":false,"internalType":"address","name":"operator","type":"address"},{"indexed":false,"internalType":"bool","name":"arg","type":"bool"}],"name":"Whitelist","type":"event"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"balanceOfMonster","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"balanceOfSummoner","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"isApproved","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_monster","type":"uint256"},{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"mint_to_monster","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_summnoer","type":"uint256"},{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"mint_to_summoner","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupplyOfMonster","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"totalSupplyOfOperator","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"totalSupplyOfOperatorOfMonster","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"totalSupplyOfOperatorOfSummoner","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupplyOfSummoner","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_from","type":"uint256"},{"internalType":"uint256","name":"_to","type":"uint256"},{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"transfer_to_monster","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_from","type":"uint256"},{"internalType":"uint256","name":"_to","type":"uint256"},{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"transfer_to_summoner","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_index","type":"uint256"}],"name":"whitelist","outputs":[],"stateMutability":"nonpayable","type":"function"}]'
        )

        global monsterContract
        monsterContract = w3.eth.contract(
            address='0x2D2f7462197d4cfEB6491e254a16D3fb2d2030EE',
            abi='[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"approved","type":"address"},{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"operator","type":"address"},{"indexed":false,"internalType":"bool","name":"approved","type":"bool"}],"name":"ApprovalForAll","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":false,"internalType":"uint256","name":"monster","type":"uint256"}],"name":"monstered","type":"event"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"approve","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"claim","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"critical","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_token_id","type":"uint256"}],"name":"divide","outputs":[{"internalType":"uint256[]","name":"","type":"uint256[]"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"dodge","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"getApproved","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_token_id","type":"uint256"}],"name":"getPrefix","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"health_Point","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"hit","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"operator","type":"address"}],"name":"isApprovedForAll","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"magical_damage_point","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"magical_defence","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"monster","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"next_monster","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address payable","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"ownerClaim","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"ownerOf","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"parry","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"physical_damage_point","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"physical_defence","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"prefix","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"profession","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"bytes","name":"_data","type":"bytes"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"operator","type":"address"},{"internalType":"bool","name":"approved","type":"bool"}],"name":"setApprovalForAll","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"suffix","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_token_id","type":"uint256"}],"name":"tokenURI","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"transferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"withdraw","outputs":[],"stateMutability":"nonpayable","type":"function"}]'
        )

        method = '0xb00b52f1'

        blockNumber = get_track_blocknum()
        print("Start Block: {}".format(blockNumber))
        newBlockNumeber = blockNumber

        page = 0
        while True:
            try:
                page += 1
                print("Current Page: {}".format(page))
                res = requests.get(ftmapi.format(blockNumber, page))
                results = json.loads(res.content)['result']
                if len(results) == 0:
                    break
                for r in results:
                    if r['isError'] == '0' and r['input'].startswith(method):
                        txinput = r['input'][10:]
                        summonerTokenID = int(txinput, 16)
                        # Count the copper coins obtained
                        copperCoins = count_copper(summonerTokenID)
                        # Count wins and plays
                        winsCount, playCount = count_wins(summonerTokenID)
                        # add to table
                        print(r['blockNumber'], summonerTokenID, copperCoins, winsCount, playCount)
                        put_summoner_stat(summonerTokenID, copperCoins, winsCount, playCount)

                        monsterTokenID, copper, isWin =  get_result(summonerTokenID, playCount)
                        copper = copper/1e18
                        insert_adventure(r['hash'], r['blockNumber'], summonerTokenID, monsterTokenID, 6, copper, isWin)

                        # get monster coppers
                        put_monster_coppers(monsterTokenID)

                        newBlockNumeber = r['blockNumber']
            except:
                put_track_blocknum(newBlockNumeber)
                traceback.print_exc()
                break

        print("End Block: {}".format(newBlockNumeber))
        put_track_blocknum(newBlockNumeber)
        return 'ok'

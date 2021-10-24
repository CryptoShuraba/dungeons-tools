from web3 import Web3
from deta import Deta
import traceback
import requests
import json
from web3.logs import STRICT, IGNORE, DISCARD, WARN
import os

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

def put_data(tokenid, copperCoins, winCount, playCount, summonerCoppers):
    item = summonerCoppers.get(str(tokenid))
    if not item or item['play_count'] != playCount:
        summonerCoppers.put({
            "tokenID": tokenid,
            "copper_count": copperCoins,
            "class": 'Monk',
            "play_count": playCount,
            "wins_count": winCount,
            "key": str(tokenid)
        })

def app():
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

    deta = Deta(os.getenv('DETA_SECRET'))
    summonerCoppers = deta.Base("summoner_coppers")
    track = deta.Base("track")

    method = '0xb00b52f1'
    summoner = []
    blockNumber = track.get('aa38-last-block')
    blockNumber = '0' if not blockNumber else blockNumber['value']
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
                    if summonerTokenID not in summoner:
                        copperCoins = count_copper(summonerTokenID)
                        # Count wins and plays
                        winsCount, playCount = count_wins(summonerTokenID)
                        # add to table
                        print(summonerTokenID, copperCoins, winsCount, playCount)
                        put_data(summonerTokenID, copperCoins, winsCount, playCount, summonerCoppers)
                        summoner.append(summonerTokenID)
                    newBlockNumeber = r['blockNumber']
        except:
            track.put(newBlockNumeber, 'aa38-last-block')
            traceback.print_exc()
            break

    print("End Block: {}".format(newBlockNumeber))
    track.put(newBlockNumeber, 'aa38-last-block')
    return 'ok'

if __name__ == '__main__':
    app()
from flaskr import scheduler
from web3 import Web3
import traceback
import os
from flaskr import db
from datetime import datetime

from flaskr.monster.models import MonsterList


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

@scheduler.task('interval', id='do_job_2', seconds=10)
def monsters():
    with scheduler.app.app_context():
        w3 = Web3(Web3.HTTPProvider(os.getenv('ANKR_ENDPOINTS')))

        monsterContract = w3.eth.contract(
            address='0x2D2f7462197d4cfEB6491e254a16D3fb2d2030EE',
            abi='[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"approved","type":"address"},{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"operator","type":"address"},{"indexed":false,"internalType":"bool","name":"approved","type":"bool"}],"name":"ApprovalForAll","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":false,"internalType":"uint256","name":"monster","type":"uint256"}],"name":"monstered","type":"event"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"approve","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"claim","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"critical","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_token_id","type":"uint256"}],"name":"divide","outputs":[{"internalType":"uint256[]","name":"","type":"uint256[]"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"dodge","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"getApproved","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_token_id","type":"uint256"}],"name":"getPrefix","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"health_Point","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"hit","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"operator","type":"address"}],"name":"isApprovedForAll","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"magical_damage_point","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"magical_defence","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"monster","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"next_monster","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address payable","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"ownerClaim","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"ownerOf","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"parry","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"physical_damage_point","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"physical_defence","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"prefix","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"profession","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"bytes","name":"_data","type":"bytes"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"operator","type":"address"},{"internalType":"bool","name":"approved","type":"bool"}],"name":"setApprovalForAll","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"suffix","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_token_id","type":"uint256"}],"name":"tokenURI","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"transferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"withdraw","outputs":[],"stateMutability":"nonpayable","type":"function"}]'
        )

        obj = MonsterList.query.order_by(MonsterList.token_id.desc()).limit(1).first()
        lastTokenId = monsterContract.functions.next_monster().call()
        
        tokenID = 0 if not obj else obj.token_id

        print("get_minted_monsters Start tokenID: {}".format(tokenID))

        while tokenID < lastTokenId:
            try:
                tokenID += 1
                suffix = monsterContract.functions.suffix(tokenID).call()
                profession = monsterContract.functions.profession(suffix).call()
                monster = monsterContract.functions.monster(tokenID).call()
                prefix = monsterContract.functions.prefix(tokenID).call()
                tokenURI = monsterContract.functions.tokenURI(tokenID).call()
                healthPoint = monsterContract.functions.health_Point(tokenID).call()
                physicalDamagePoint = monsterContract.functions.physical_damage_point(tokenID).call()
                magicalDamagePoint = monsterContract.functions.magical_damage_point(tokenID).call()
                physicalDefence = monsterContract.functions.physical_defence(tokenID).call()
                magicalDefence = monsterContract.functions.magical_defence(tokenID).call()
                dodge = monsterContract.functions.dodge(tokenID).call()
                hit = monsterContract.functions.hit(tokenID).call()
                critical = monsterContract.functions.critical(tokenID).call()
                parry = monsterContract.functions.parry(tokenID).call()

                print(tokenID, monster)

                put_monster(tokenID, suffix, profession, monster, prefix, tokenURI, 
                    healthPoint, physicalDamagePoint, magicalDamagePoint, 
                    physicalDefence, magicalDefence, dodge, hit, critical, parry)
            except:
                traceback.print_exc()
                break

        print("get_minted_monsters Last tokenID: {}".format(lastTokenId))
        return 'ok'

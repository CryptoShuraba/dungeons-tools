import traceback
from flaskr import scheduler
import os
from flaskr import db
from datetime import datetime

from flaskr.rarity.models import RarityNFTHolder
from flaskr.dungeons.models import DungeonsTrack
import requests
import json


url = 'url = "https://api.thegraph.com/subgraphs/name/rarity-adventure/rarity"'
payload = '''
            {
                summoners(first:1000, where:{id_gt: %s}) {
                    id
                    owner
                    _class
                    _level
                }
            }
        '''

trackKey = 'sync_rarity_subgraph-last-id'


def get_track_lastid():
    obj = DungeonsTrack.query.filter_by(key=trackKey).first()
    if not obj:
        obj = DungeonsTrack(key=trackKey, value='', created=datetime.now(), updated=datetime.now())
        db.session.add(obj)
        db.session.commit()
    return obj.value


def put_track_blocknum(LastID):
    obj = DungeonsTrack.query.filter_by(key=trackKey).first()
    obj.value = LastID
    obj.updated = datetime.now()


# @scheduler.task('cron', id='do_job_5', hour=7, minute=32)
def sync_rarity_subgraph():
    with scheduler.app.app_context():

        lastID = get_track_lastid()
        print("sync_rarity_subgraph Start ID: {}".format(lastID))

        while True:
            res = requests.post(url, json={"query": payload % lastID})

            results = json.loads(res.content)['data']['summoners']

            if not results or len(results) == 0:
                break

            for r in results:
                item = RarityNFTHolder()
                item.holder_address = r['owner']
                item.token_id = r['id']
                now = datetime.now()
                item.updated = now
                item.created = now
                item.summoner_class = r['_class']
                item.summoner_level = r['_level']
                lastID = r['id']
                db.session.add(item)
            
            print("sync_rarity_subgraph End ID: {}".format(lastID))
            put_track_blocknum(lastID)
            db.session.commit()

        return 'ok'

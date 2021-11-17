import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_apscheduler import APScheduler
from flask_cors import CORS


db = SQLAlchemy()
migrate = Migrate(compare_type=True)
scheduler = APScheduler()

def create_app(test_config=None):
    from .monster.models import MonsterList, MonsterNFTTracker, MonsterNFTHolder
    from .dungeons.models import DungeonsFirstAdventure, DungeonsSummonerStat, DungeonsMonsterCoppers

    def is_debug_mode():
        """Get app debug status."""
        debug = os.environ.get("FLASK_DEBUG")
        if not debug:
            return os.environ.get("FLASK_ENV") == "development"
        return debug.lower() not in ("0", "false", "no")

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_object(os.environ['APP_SETTINGS'])
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    db.init_app(app)
    migrate.init_app(app, db)
    scheduler.init_app(app)

    with app.app_context():
        from .schedule import dungeons, monster
        scheduler.start()

        from .dungeons import views as v1
        from .monster import views as v2
        app.register_blueprint(v1.bp)
        app.register_blueprint(v2.bp)
    
    CORS(app)
    return app
from datetime import datetime
from pony.orm import Database, PrimaryKey, Required

db = Database("sqlite", "../videobot.db", create_db=True)


class Video(db.Entity):
    id = PrimaryKey(str)
    title = Required(str)
    author = Required(str)
    publish_time = Required(datetime)
    processed = Required(bool, default=False)


db.generate_mapping(create_tables=True)

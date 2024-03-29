# cloudBox is copyright 2012 - 2014 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

from peewee import *

from cloudbox.common.models import BaseModel


class GlobalMetadata(BaseModel):
    class Meta:
        db_table = "cb_global_metadata"

    id = PrimaryKeyField()
    name = CharField()
    value = TextField()
    defaultValue = TextField()


class Server(BaseModel):
    class Meta:
        db_table = "cb_servers"
    id = PrimaryKeyField()
    name = CharField()


class WorldServer(Server):
    class Meta:
        db_table = "cb_worldservers"
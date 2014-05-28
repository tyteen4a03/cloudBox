# cloudBox is copyright 2012 - 2014 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

from peewee import *

from cloudbox.common.models import BaseModel
from cloudbox.common.models.servers import WorldServer


class World(BaseModel):
    class Meta:
        db_table = "cb_worlds"
    id = PrimaryKeyField()
    name = CharField()
    worldServerID = ForeignKeyField(WorldServer, db_column="worldServerID")
    filePath = CharField()
    isDefault = BooleanField()
    lastAccessed = IntegerField()
    lastModified = IntegerField()
    timeCreated = IntegerField()

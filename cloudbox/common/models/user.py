from peewee import *

from cloudbox.common.models import BaseModel


class User(BaseModel):
    class Meta():
        db_table = "cb_users"
        order_by = ("id", "username")

    id = PrimaryKeyField()
    username = CharField()
    firstseen = IntegerField()
    lastseen = IntegerField()
    primaryUserGroup = IntegerField()
    secondaryUserGroups = CharField()  # For easy lookup
    email = CharField()
    password = CharField()


class UserGroup(BaseModel):
    class Meta():
        db_table = "cb_user_groups"
        order_by = ("id",)

    id = PrimaryKeyField()
    title = CharField()
    displayStylePriority = IntegerField()


class UserGroupUserAssoc(BaseModel):
    class Meta():
        db_table = "cb_user_group_user_assoc"

    id = PrimaryKeyField()
    userID = ForeignKeyField(User)
    groupID = ForeignKeyField(UserGroup)


class UserIP(BaseModel):
    class Meta():
        db_table = "cb_user_ip"

    id = PrimaryKeyField()
    userID = ForeignKeyField(User)
    logDate = TimeField()
    ip = BlobField()
    action = IntegerField()
    subActionType = IntegerField()
    subActionID = IntegerField()


class Bans(BaseModel):
    class Meta():
        db_table = "cb_bans"
        order_by = ("userID",)

    id = PrimaryKeyField()
    userID = ForeignKeyField(User)
    bannerUserID = ForeignKeyField(User)
    type = IntegerField()
    recordID = IntegerField()
    startTime = IntegerField()
    endTime = IntegerField()
    reason = CharField()
from utils.db_api.schemas.user import CloudUsers
from utils.db_api.db_gino import db


async def add_user_and_token(user_id: int, username: str, adv: str, password: str, token: str):
    try:
        user = CloudUsers(user_id=user_id, username=username, adv=adv, password=password, token=token)
        await user.create()
    except Warning:
        print('ПОЛНЫЙ ПОДСЕБЯК')


async def select_all_users():
    users = await CloudUsers.query.gino.all()
    return users


async def select_user(user_id):
    user = await CloudUsers.query.where(CloudUsers.user_id == user_id).gino.first()
    print(user)
    return user


async def select_token(user_id):
    t = await CloudUsers.select('token').where(CloudUsers.user_id == user_id).gino.scalar()
    print(t)
    return t


async def delete_user(user_id):
    delete_user = await CloudUsers.query.where(CloudUsers.user_id == user_id).gino.first().delete()
    return delete_user

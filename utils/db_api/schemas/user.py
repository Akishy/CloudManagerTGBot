from sqlalchemy import Column, BigInteger, String
from utils.db_api.db_gino import BaseModel


class CloudUsers(BaseModel):
    __tablename__ = 'CloudUsers'
    user_id = Column(BigInteger, primary_key=True)
    username = Column(String(50))
    adv = Column(String(24))
    password = Column(String(25))
    token = Column(String(2200))

from sqlalchemy import Column, BigInteger, String, sql

from utils.db_api.db_gino import TimedBaseModel


class User(TimedBaseModel):
    __tablename__ = 'user'
    user_id = Column(BigInteger, primary_key=True)
    first_name = Column(String(200))
    last_name = Column(String(200))
    username = Column(String(50))
    referral_id = Column(BigInteger)
    status = Column(String(30))
    time_report = Column(String(1000))
    course_history = Column(String(10000))
    query: sql.select

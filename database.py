from typing import Dict
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session


class DbSessionHandler:
  def __init__(self, url:str='sqlite:///./huntil.db') -> None:
    self.db_url = url
    self.engine = self.init_engine()
    self.session = self.init_session()

  def init_engine(self,connect_args: Dict = {'check_same_thread':False})-> Engine:
    return create_engine(url=self.db_url,connect_args=connect_args)
  
  def init_session(self) -> Session:
    return sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
  
  def get_db(self):
    db = self.session()
    try:
      yield db
    finally:
      db.close()


  

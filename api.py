from typing import Annotated
from database import DbSessionHandler
from models import Site, Harvest, HuntableSpecies, Geography, Document
from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import FastAPI, Depends, Query, HTTPException

db_session_handler = DbSessionHandler()
SessionDependency = Annotated[Session, Depends(db_session_handler.get_db)]
app = FastAPI()

@app.get('/')
def root() -> str:
  return {'message':'Hello world'}

@app.get('/sites/')
def read_sites(
  session: SessionDependency,
  offset: int = 0,
  limit: Annotated[int, Query(le=100)] = 100
) -> list[Site]:
  stmt = select(Site).offset(offset).limit(limit)
  sites = session.execute(stmt).all()
  return sites

@app.get('/sites/{site_id}')
def read_site(
  session:SessionDependency,
  site_id:str
) -> Site:
  try:
    return session.execute(select(Site).where(Site.site_id==site_id))
  except:
    return HTTPException(status_code=404, detail=f"Site with site_id={site_id} not found")

@app.get('/huntable-species/}')
def read_huntable_species(
  session: SessionDependency,
  offset: int = 0,
  limit: Annotated[int, Query(le=100)] = 100
) -> list[HuntableSpecies]:
  stmt = select(HuntableSpecies).offset(offset).limit(limit)
  return session.execute(stmt).all()

@app.get('/huntable-species/}')
def read_huntable_species(
  session: SessionDependency,
  offset: int = 0,
  limit: Annotated[int, Query(le=100)] = 100
) -> list[HuntableSpecies]:
  stmt = select(HuntableSpecies).offset(offset).limit(limit)
  return session.execute(stmt).all()

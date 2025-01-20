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
  """Root endpoint for testing"""
  return {'message':'Hello world'}

@app.get('/sites/')
def read_sites(
  session: SessionDependency,
  offset: int = 0,
  limit: Annotated[int, Query(le=100)] = 100
) -> list[Site]:
  """Get all sites"""
  stmt = select(Site).offset(offset).limit(limit)
  sites = session.execute(stmt).all()
  return sites

@app.get('/sites/{site_id}/names')
def read_site(
  session:SessionDependency,
  site_id:str
) -> Site:
  """Get Site Naming info for a specific site"""
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
  """Get All Huntable Species available for all sites"""
  stmt = select(HuntableSpecies).offset(offset).limit(limit)
  return session.execute(stmt).all()

@app.get('/huntable-species/site/{site_id}}')
def read_huntable_species_by_site(
  session: SessionDependency,
  site_id:str
) -> list[HuntableSpecies]:
  """Get huntable specices for a specific site"""
  stmt = select(HuntableSpecies).where(HuntableSpecies.site_id == site_id)
  return session.execute(stmt).all()

@app.get('/huntable-species/species/{species}')
def read_huntable_species_by_site(
  session: SessionDependency,
  species:str
) -> list[HuntableSpecies]:
  """Gets all sites where a specific species is available"""
  stmt = select(HuntableSpecies).where(HuntableSpecies.species == species)
  return session.execute(stmt).all()

@app.get('/geography/{site_id}')
def read_geography(
  session:SessionDependency,
  site_id:str
) -> Geography:
  """Get Site geography info (address, huntable acres, coords, etc) for a specific site"""
  try:
    return session.execute(select(Geography).where(Geography.site_id==site_id))
  except:
    return HTTPException(status_code=404, detail=f"Site with site_id={site_id} not found")

@app.get('/documents/{site_id}')
def read_geography(
  session:SessionDependency,
  site_id:str
) -> Document:
  """Get Site document info (markdown conversion & url) for a specific site"""
  try:
    return session.execute(select(Document).where(Document.site_id==site_id))
  except:
    return HTTPException(status_code=404, detail=f"Site with site_id={site_id} not found")

@app.get('/harvest/')
def read_harvests(
  session: SessionDependency,
  offset: int = 0,
  limit: Annotated[int, Query(le=100)] = 100
) -> list[Harvest]:
  """Get all harvest data"""
  stmt = select(Harvest).offset(offset).limit(limit)
  harvest_records = session.execute(stmt).all()
  return harvest_records

@app.get('/harvest/counties')
def read_counties_harvests(
  session: SessionDependency
) -> list[Harvest]:
  """Get all county-wise harvest data"""
  stmt = select(Harvest).where(Harvest.is_county == 1)
  harvest_records = session.execute(stmt).all()
  return harvest_records

@app.get('/harvest/sites')
def read_counties_harvests(
  session: SessionDependency
) -> list[Harvest]:
  """Get all county-wise harvest data"""
  stmt = select(Harvest).where(Harvest.is_county == 0)
  harvest_records = session.execute(stmt).all()
  return harvest_records


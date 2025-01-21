from typing import Annotated, Union, Optional
from database import DbSessionHandler
from models import Site, Harvest, HuntableSpecies, Geography, Document
import response_models
from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import FastAPI, Depends, Query, HTTPException

db_session_handler = DbSessionHandler()
SessionDependency = Annotated[Session, Depends(db_session_handler.get_db)]
app = FastAPI()

@app.get('/')
def root() -> str:
  """Root endpoint for testing"""
  return "{'message':'Hello world'}"

@app.get('/sites/names', response_model=list[response_models.SiteName])
def read_sites(
  session: SessionDependency,
  offset: int = 0,
  limit: Annotated[int, Query(le=100)] = 100
) -> list[response_models.SiteName]:
  """Get all sites"""
  stmt = select(Site.site_id, Site.abbreviated_name, Site.full_name, Site.site_type).offset(offset).limit(limit)
  sites = session.execute(stmt).all()
  return [response_models.SiteName.model_validate(response_models.SiteName(site_id=site.site_id, full_name = site.full_name, abbreviated_name=site.abbreviated_name, site_type=site.site_type)) for site in sites]

@app.get('/sites/{site_id}/names', response_model = Optional[response_models.SiteName])
def read_site(
  session:SessionDependency,
  site_id:str
) -> Optional[response_models.SiteName]:
  """Get Site Naming info for a specific site"""
  stmt = select(Site).where(Site.site_id==site_id)
  site = session.execute(stmt).scalar_one_or_none()
  if site is None:
    raise HTTPException(status_code=404, detail=f"Site with site_id={site_id} not found")
  return response_models.SiteName(site_id=site.site_id, full_name = site.full_name, abbreviated_name=site.abbreviated_name,site_type = site.site_type)


@app.get('/huntable-species/}')
def read_huntable_species(
  session: SessionDependency,
  offset: int = 0,
  limit: Annotated[int, Query(le=100)] = 100
) -> list[response_models.HuntableSpecies]:
  """Get All Huntable Species available for all sites"""
  stmt = select(HuntableSpecies).offset(offset).limit(limit)
  return session.execute(stmt).all()

@app.get('/huntable-species/site/{site_id}}')
def read_huntable_species_by_site(
  session: SessionDependency,
  site_id:str
) -> list[response_models.HuntableSpecies]:
  """Get huntable specices for a specific site"""
  stmt = select(HuntableSpecies).where(HuntableSpecies.site_id == site_id)
  return session.execute(stmt).all()

@app.get('/huntable-species/species/{species}')
def read_huntable_species_by_site(
  session: SessionDependency,
  species:str
) -> list[response_models.HuntableSpecies]:
  """Gets all sites where a specific species is available"""
  stmt = select(HuntableSpecies).where(HuntableSpecies.species == species)
  return session.execute(stmt).all()

@app.get('/geography/{site_id}')
def read_geography(
  session:SessionDependency,
  site_id:str
) -> response_models.Geography:
  """Get Site geography info (address, huntable acres, coords, etc) for a specific site"""
  try:
    return session.execute(select(Geography).where(Geography.site_id==site_id))
  except:
    return HTTPException(status_code=404, detail=f"Site with site_id={site_id} not found")

@app.get('/documents/{site_id}')
def read_geography(
  session:SessionDependency,
  site_id:str
) -> response_models.Document:
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
) -> list[response_models.Harvest]:
  """Get all harvest data"""
  stmt = select(Harvest).offset(offset).limit(limit)
  harvest_records = session.execute(stmt).all()
  return harvest_records

@app.get('/harvest/counties')
def read_counties_harvests(
  session: SessionDependency
) -> list[response_models.Harvest]:
  """Get all county-wise harvest data"""
  stmt = select(Harvest).where(Harvest.is_county == 1)
  harvest_records = session.execute(stmt).all()
  return harvest_records

@app.get('/harvest/sites')
def read_counties_harvests(
  session: SessionDependency
) -> list[response_models.Harvest]:
  """Get all county-wise harvest data"""
  stmt = select(Harvest).where(Harvest.is_county == 0)
  harvest_records = session.execute(stmt).all()
  return harvest_records


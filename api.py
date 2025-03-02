from typing import Annotated, Union, Optional
from database import DbSessionHandler
from models import Site, Harvest, HuntableSpecies, Geography, Document
import response_models
from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import FastAPI, Depends, Query, HTTPException, APIRouter
from fastapi.middleware.cors import CORSMiddleware

db_session_handler = DbSessionHandler()
SessionDependency = Annotated[Session, Depends(db_session_handler.get_db)]
app = FastAPI()
api_router = APIRouter(prefix="/api")
origins = [
  'http://localhost.com',
  'http://localhost',
  'http://localhost:5134'
]

app.add_middleware(CORSMiddleware, 
                   allow_origins=origins,
                   allow_credentials=False, 
                   allow_methods=["GET"], 
                   allow_headers=["*"]
                   )

@api_router.get('/')
def root() -> str:
  """Root endpoint for testing"""
  return "{'message':'Hello world'}"

@api_router.get('/sites/names', response_model=list[response_models.SiteName])
def read_sites(
  session: SessionDependency,
  offset: int = 0,
  limit: Annotated[int, Query(le=100)] = 100
) -> list[response_models.SiteName]:
  """Get all sites"""
  stmt = select(Site.site_id, Site.abbreviated_name, Site.full_name, Site.site_type).offset(offset).limit(limit)
  sites = session.execute(stmt).all()
  return [response_models.SiteName.model_validate(response_models.SiteName(site_id=site.site_id, full_name = site.full_name, abbreviated_name=site.abbreviated_name, site_type=site.site_type)) for site in sites]

@api_router.get('/sites/{site_id}/names', response_model = Optional[response_models.SiteName])
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


@api_router.get('/huntable-species/')
def read_huntable_species(
  session: SessionDependency,
  offset: int = 0,
  limit: Annotated[int, Query(le=100)] = 100
) -> list[response_models.HuntableSpecies]:
  """Get All Huntable Species available for all sites"""
  stmt = select(HuntableSpecies).offset(offset).limit(limit)
  huntables = session.execute(stmt).scalars().all()
  return [
    response_models.HuntableSpecies(
      site_id=huntable.site.site_id, 
      species=huntable.species,
      season=huntable.season,
      stipulation=huntable.stipulation
      ) for huntable in huntables]

@api_router.get('/huntable-species/site/{site_id}')
def read_huntable_species_by_site(
  session: SessionDependency,
  site_id:str
) -> list[response_models.HuntableSpecies]:
  """Get huntable specices for a specific site"""
  stmt = select(HuntableSpecies).where(HuntableSpecies.site_id == site_id)
  huntables = session.execute(stmt).scalars().all()
  if len(huntables) == 0:
    raise HTTPException(status_code=404, detail=f"No huntable species for site with site_id={site_id}")
  return [
    response_models.HuntableSpecies(
      site_id=huntable.site.site_id, 
      species=huntable.species,
      season=huntable.season,
      stipulation=huntable.stipulation
      ) for huntable in huntables]



@api_router.get('/huntable-species/species/{species}')
def read_huntable_species_by_site(
  session: SessionDependency,
  species:str
) -> list[response_models.HuntableSpecies]:
  """Get huntable specices for a specific site"""
  stmt = select(HuntableSpecies).where(HuntableSpecies.species == species)
  huntables = session.execute(stmt).scalars().all()
  if len(huntables) == 0:
    raise HTTPException(status_code=404, detail=f"No sites for site with huntable_species={species}")
  return [
    response_models.HuntableSpecies(
      site_id=huntable.site.site_id, 
      species=huntable.species,
      season=huntable.season,
      stipulation=huntable.stipulation
      ) for huntable in huntables]

@api_router.get('/geography/')
def get_all_geography(
  session:SessionDependency
) -> list[response_models.Geography]:
  stmt = select(Geography)
  results = session.execute(stmt).scalars().all()
  return [response_models.Geography(site_id=result.site_id,
                                    region=result.region, 
                                    county=result.county, 
                                    huntable_acres=result.huntable_acres,
                                    address=result.address,
                                    latitude=result.latitude, 
                                    longitude=result.longitude)
          for result in results]

@api_router.get('/geography/{site_id}')
def read_geography(
  session:SessionDependency,
  site_id:str
) -> response_models.Geography:
  """Get Site geography info (address, huntable acres, coords, etc) for a specific site"""
  stmt = select(Geography).where(Geography.site_id==site_id)
  result = session.execute(stmt).scalar_one_or_none()
  if result is None:
    raise HTTPException(status_code=404, detail=f"Geography with site_id={site_id} not found")
  return response_models.Geography(site_id=result.site_id,
                                    region=result.region, 
                                    county=result.county, 
                                    huntable_acres=result.huntable_acres,
                                    address=result.address,
                                    latitude=result.latitude, 
                                    longitude=result.longitude)
@api_router.get('/documents/')
def read_all_documents(
  session:SessionDependency,
) -> list[response_models.Document]:
  """Get Site document info (markdown conversion & url) for a specific site"""
  stmt = select(Document)
  results = session.execute(stmt).scalars().all()
  return [response_models.Document(site_id=result.site_id, site_markdown=result.site_markdown, url=result.url) for result in results]

@api_router.get('/documents/{site_id}')
def read_document(
  session:SessionDependency,
  site_id:str
) -> response_models.Document:
  """Get Site document info (markdown conversion & url) for a specific site"""
  stmt = select(Document).where(Document.site_id==site_id)
  result = session.execute(stmt).scalar_one_or_none()
  if result is None:
    raise HTTPException(status_code=404, detail=f"Document with site_id={site_id} not found")
  return response_models.Document(site_id=result.site_id, site_markdown=result.site_markdown, url=result.url)

@api_router.get('/harvest/')
def read_harvests(
  session: SessionDependency,
  offset: int = 0,
  limit: Annotated[int, Query(le=100)] = 100
) -> list[response_models.Harvest]:
  """Get all harvest data"""
  stmt = select(Harvest).offset(offset).limit(limit)
  harvest_records = session.execute(stmt).scalars().all()
  return [response_models.Harvest(record_id = harvest_record.record_id,
                                  site_id=harvest_record.site_id, 
                                  site=harvest_record.site,
                                  year=harvest_record.year,
                                  species=harvest_record.species,
                                  season=harvest_record.season,
                                  subcategory=harvest_record.subcategory,
                                  harvest_count=harvest_record.harvest_count
                                  ) for harvest_record in harvest_records]

#There's not much harvest data so I'll just load it in as a dataframe, cache, and do filtering on the client
"""
@app.get('/harvest/species/{species}')
def read_harvests_by_specices(
  session: SessionDependency,
  offset: int = 0,
  limit: Annotated[int, Query(le=100)] = 100
) -> list[response_models.Harvest]:
  stmt = select(Harvest).offset(offset).limit(limit)
  harvest_records = session.execute(stmt).all()
  return [response_models.Harvest(record_id = harvest_records.record_id,
                                  site_id=harvest_records.site_id, 
                                  year=harvest_records.year,
                                  species=harvest_records.species,
                                  season=harvest_records.season,
                                  subcategory=harvest_records.subcategory,
                                  harvest_count=harvest_records.harvest_count
                                  )]
                                  """


app.include_router(api_router)
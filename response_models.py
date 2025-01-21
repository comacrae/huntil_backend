from pydantic import BaseModel
from typing import List

class HuntableSpecies(BaseModel):
  class Config:
    from_attributes = True
  record_id: int
  site_id: str
  species: str
  season: str
  stipulation: str


class Document(BaseModel):
  class Config:
    from_attributes = True
  site_id:str
  site_markdown:str
  url:str

class Geography(BaseModel):
  class Config:
    from_attributes = True
  site_id:str
  region:str
  county:str
  huntable_acres:int
  address:str
  latitude: float
  longitude: float

class Harvest(BaseModel):
  class Config:
    from_attributes = True
  record_id:int
  site_id: str
  site:str
  year: int
  species:str
  season:str
  subcategory:str
  harvest_count:int

class Site(BaseModel):
  class Config:
    from_attributes = True
  site_id: str
  full_name:str
  abbreviated_name:str
  site_type:str
  huntable: List[HuntableSpecies] = []
  document: Document
  geography: Geography
  harvest: List[Harvest] = []
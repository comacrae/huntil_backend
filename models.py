from __future__ import annotations
from typing import Optional,List
from sqlalchemy import ForeignKey, String, Text, Integer, Float, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
  pass

class Site(Base):
  __tablename__="sites"
  site_id : Mapped[str] = mapped_column(String(63),primary_key=True)
  full_name: Mapped[str] = mapped_column(String(127))
  abbreviated_name: Mapped[str] = mapped_column(String(127))
  site_type: Mapped[str] = mapped_column(String(63))
  huntable: Mapped[List["HuntableSpecies"]] = relationship("HuntableSpecies",back_populates="site")
  document: Mapped["Document"] = relationship("Document",back_populates="site")
  geography: Mapped["Geography"] = relationship("Geography",back_populates="site")
  harvest: Mapped[List["Harvest"]] = relationship("Harvest",back_populates="site_relationship")

  def __repr__(self) -> str:
    return f"site_id={self.site_id!r} full_name={self.full_name!r} abbreviated_name={self.abbreviated_name!r} site_type={self.site_type!r}"


class HuntableSpecies(Base):
  __tablename__="huntable_species"
  record_id: Mapped[int] = mapped_column(Integer, primary_key=True,autoincrement=True, index=True)
  site_id : Mapped[str] = mapped_column(ForeignKey("sites.site_id"))
  species : Mapped[str] = mapped_column(String(127))
  season : Mapped[str] = mapped_column(String(127), default='Statewide')
  stipulation: Mapped[str] = mapped_column(String(127))
  site: Mapped["Site"] = relationship("Site",back_populates="huntable")

  def __repr__(self) -> str:
    return f"record_id={self.record_id!r} site_id={self.site_id!r} species={self.species!r} season={self.season!r} stipulation={self.stipulation!r} site={self.site!r}"

class Document(Base):
  __tablename__="documents"
  site_id : Mapped[str] = mapped_column(ForeignKey("sites.site_id"), primary_key=True)
  site_markdown:Mapped[str] = mapped_column(Text)
  url: Mapped[str] = mapped_column(String(255))
  site: Mapped["Site"] = relationship("Site",back_populates="document")

  def __repr__(self) -> str:
    return f"site_id={self.site_id!r} site_markdown={self.site_markdown!r} url={self.url!r}"

class Geography(Base):
  __tablename__="geography"
  site_id : Mapped[str] = mapped_column(ForeignKey("sites.site_id"), primary_key=True)
  region: Mapped[int] = mapped_column(Integer)
  county: Mapped[str] = mapped_column(String(63))
  huntable_acres: Mapped[int] = mapped_column(Integer)
  address: Mapped[str] = mapped_column(String(255))
  latitude: Mapped[float] = mapped_column(Float)
  longitude: Mapped[float] = mapped_column(Float)
  site: Mapped["Site"] = relationship("Site",back_populates="geography")
  
  def __repr__(self) -> str: 
    return f"site_id={self.site_id!r} region={self.region!r} county={self.county!r} huntable_acres={self.huntable_acres!r} address={self.address!r} latitude={self.latitude!r} longitude={self.longitude!r}"

class Harvest(Base):
  __tablename__="harvest"
  record_id: Mapped[int] = mapped_column(Integer, primary_key=True,autoincrement=True, index=True)
  site_id : Mapped[str] = mapped_column(ForeignKey("sites.site_id"))
  site : Mapped[str] = mapped_column(String(63))
  year: Mapped[int] = mapped_column(Integer)
  species: Mapped[str]= mapped_column(String(127))
  season: Mapped[str] = mapped_column(String(127))
  subcategory: Mapped[str] = mapped_column(Text)
  harvest_count: Mapped[int] = mapped_column(Integer)
  site_relationship: Mapped["Site"] = relationship("Site",back_populates="harvest")

  def __repr__(self) -> str:
    return f"record_id={self.record_id!r} site={self.site!r} is_county={self.is_county!r} year={self.year!r} species={self.species!r} season={self.season!r} subcategory={self.subcategory!r} harvest={self.harvest!r}"
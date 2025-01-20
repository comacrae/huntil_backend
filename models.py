from typing import Optional,List
from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
  pass
class Site(Base):
  __tablename__="site"
  site_id : Mapped[str] = mapped_column(String(63),primary_key=True)
  full_name: Mapped[str] = mapped_column(String(127))
  abbreviated_name: Mapped[str] = mapped_column(String(127))
  site_type: Mapped[str] = mapped_column(String(63))
  huntable: Mapped[List["HuntableSpecies"]] = relationship(back_populates="site")

  def __repr__(self) -> str:
    return f"site_id={self.site_id!r} full_name={self.full_name!r} abbreviated_name={self.abbreviated_name!r} site_type={self.site_type!r}"

class HuntableSpecies(Base):
  __tablename__="huntable_species"
  record_id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
  site_id : Mapped[str] = mapped_column(String(63),ForeignKey("site.site_id"))
  species : Mapped[str] = mapped_column(String(127))
  season : Mapped[str] = mapped_column(String(127), default='Statewide')
  stipulation: Mapped[str] = mapped_column(String(127))
  site: Mapped["Site"] = relationship(back_populates="huntable")

  def __repr__(self) -> str:
    return f"record_id={self.record_id!r} site_id={self.site_id!r} species={self.species!r} season={self.season!r} stipulation={self.stipulation!r} site={self.site!r}"

class Document(Base):
  __tablename__="documents"
  site_id : Mapped[str] = mapped_column(String(63),ForeignKey("site.site_id"), primary_key=True)
  site_markdown:Mapped[str] = mapped_column(Text)
  url: Mapped[str] = mapped_column(String(255))

  def __repr__(self) -> str:
    return f"site_id={self.site_id!r} site_markdown={self.site_markdown!r} url={self.url!r}"
  
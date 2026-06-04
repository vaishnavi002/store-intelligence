from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, String, Float, Boolean


class Base(DeclarativeBase):
    pass


class EventModel(Base):
    __tablename__ = "events"

    event_id = Column(String, primary_key=True)
    store_id = Column(String)
    camera_id = Column(String)
    visitor_id = Column(String)
    event_type = Column(String)
    timestamp = Column(String)

    is_staff = Column(Boolean)
    confidence = Column(Float)
from sqlalchemy import Boolean, Column, Integer, String, DATETIME
from datetime import datetime
from config import Tashkent_tz
from database import Base


class AssignmentTable(Base):
    __tablename__ = "Assignment"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(64), index=True)
    description = Column(String, index=True)
    priority = Column(String(24))
    the_nadir = Column(String(64))
    is_complete = Column(Boolean,default=False)
    created_at  = Column(DATETIME,nullable=False,default=datetime.now(tz=Tashkent_tz))
    updated_at = Column(DATETIME, onupdate=datetime.now(tz=Tashkent_tz))

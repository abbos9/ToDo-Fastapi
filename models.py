from sqlalchemy import Boolean, Column, Integer, String, DATETIME, ForeignKey
from datetime import datetime
from config import Tashkent_tz
from database import Base
from sqlalchemy.orm import relationship


class Users(Base):
    __tablename__ = "User"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True)
    first_name = Column(String(36))
    last_name = Column(String(36))
    phone_num = Column(String(36))
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at  = Column(DATETIME,nullable=False,default=datetime.now(tz=Tashkent_tz))
    updated_at = Column(DATETIME, onupdate=datetime.now(tz=Tashkent_tz))

    assignments = relationship("AssignmentTable", back_populates="owner")


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

    owner_id = Column(Integer, ForeignKey("User.id"))
    owner = relationship("Users", back_populates="assignments")
from datetime import datetime
from uuid import uuid4

from app.database.db import Base
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID


class User(Base):
    __tablename__ = 'users'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(25), nullable=False)
    email = Column(String(75), nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, index=True, default=datetime.utcnow)
    updated_at = Column(DateTime, index=True, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}("
            f"id={self.id}, "
            f"name={self.name}, "
            f")>"
        )

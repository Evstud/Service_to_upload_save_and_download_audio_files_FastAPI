from uuid import uuid4
from sqlalchemy import Column, String, ForeignKey, LargeBinary
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from db import Base, engine


class UserTable(Base):
    __tablename__ = 'user_table'
    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    user_token = Column(UUID(as_uuid=True), default=uuid4)
    user_name = Column(String(200), unique=True)
    audio = relationship('Audio', back_populates='user', cascade="all, delete")


class Audio(Base):
    __tablename__ = 'audio'
    audio_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    audio_name = Column(String(200))
    audio_data = Column(LargeBinary)
    user_id = Column(UUID(as_uuid=True), ForeignKey('user_table.user_id'))
    user = relationship('UserTable', back_populates='audio')


Base.metadata.create_all(bind=engine)

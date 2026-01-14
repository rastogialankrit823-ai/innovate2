from collections.abc import AsyncGenerator
import uuid

from sqlalchemy import Column , String ,Integer,Text ,DateTime ,ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine ,async_sessionmaker
from sqlalchemy.orm import DeclarativeBase ,relationship
from datetime import datetime 

DATABASE_URL ="sqlite+aiosqlite:///./test.db"
DATABASE_URL2 ="sqlite+aiosqlite:///./test2.db"


class BASE(DeclarativeBase):
	pass

class Post(BASE):
	__tablename__="posts(transaction)" 

	id=Column(UUID(as_uuid=True),primary_key=True , default=uuid.uuid4)
	#caption=Column(Text)
	uid=Column(String, nullable=False)
	upw=Column(String, nullable=False)
	amount=Column(Integer , nullable=False)
	reg=Column(String , nullable=False)

	created_at=Column(DateTime,default=datetime.utcnow)

engine=create_async_engine(DATABASE_URL)
async_session_maker=async_sessionmaker(engine ,expire_on_commit=False)

async def create_db():
    async with engine.begin() as conn:
    	await conn.run_sync(BASE.metadata.create_all)

async def get_async_session()  :
	async with async_session_maker() as session:
		yield session 

class Postu(BASE):
	__tablename__="posts(user data)" 

	id=Column(UUID(as_uuid=True),primary_key=True , default=uuid.uuid4)
	#caption=Column(Text)
	uid=Column(String, nullable=False)
	upw=Column(String, nullable=False)

	created_at=Column(DateTime,default=datetime.utcnow)

engine2=create_async_engine(DATABASE_URL2)
async_session_maker2=async_sessionmaker(engine2 ,expire_on_commit=False)

async def create_db():
    async with engine.begin() as conn:
    	await conn.run_sync(BASE.metadata.create_all)

async def get_async_session()  :
	async with async_session_maker() as session:
		yield session 

async def create_db2():
    async with engine2.begin() as conn:
    	await conn.run_sync(BASE.metadata.create_all)

async def get_async_session2()  :
	async with async_session_maker2() as session:
		yield session 


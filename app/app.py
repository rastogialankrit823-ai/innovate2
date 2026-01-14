from fastapi import FastAPI,File,UploadFile, Form ,Depends
from fastapi import HTTPException
from app.schemas import userbase ,userb
from app.db import Post ,create_db, get_async_session , Postu ,create_db2 ,get_async_session2
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from sqlalchemy import select

@asynccontextmanager
async def life(app :FastAPI):
	await create_db()
	await create_db2()
	yield 



app=FastAPI(lifespan=life)


@app.get("/hello")
def hellow():
	return {"message":"hello"}


async def find(id :str ,pw :str ,session :AsyncSession =Depends(get_async_session2)):
	text=await session.execute(select(Postu).order_by(Postu.created_at.desc()))
	text2=[row[0] for row in text.all()]
	fl=False
	for j in text2:
		if(j.uid==id and j.upw==pw):fl=True
	if(fl==False):
		raise HTTPException(status_code=500,detail="user not found") 
	return fl


@app.post("/posts")
async def make_user(post : userb, session :AsyncSession =Depends(get_async_session2)):
	newp={"user_id":post.id,"user_password":post.pw}
	pt=Postu(
		uid=post.id,
		upw=post.pw
    )
	session.add(pt)
	await session.commit()
	await session.refresh(pt)
	return newp 

@app.post("/transictions")
async def tras (post :userbase ,session: AsyncSession =Depends(get_async_session)):
	postt=Post(
		 uid=post.uid,
		 upw=post.upw,
		 amount=post.amount,
		 reg=post.reg
		)
	find(post.uid,post.upw)
	session.add(postt)
	await session.commit()
	await session.refresh(postt)
	return postt

@app.get("/state")
async def get_status( session: AsyncSession=Depends(get_async_session)):
	res=await session.execute(select(Post).order_by(Post.created_at.desc()))
	posts=[row[0] for row in res.all()]
	trans_data=[]
	for post in posts:
		trans_data.append(
			{
			   "id":str(post.id),
			   "uid":post.uid,
			   "upw":post.upw,
			   "amount":post.amount,
			   "reg":post.reg,
			   "time":post.created_at.isoformat()

			}
		 )
	return {"transictions" : trans_data}

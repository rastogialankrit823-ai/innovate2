from fastapi import FastAPI,File,UploadFile, Form ,Depends
from fastapi import HTTPException
from app.schemas import userbase 
from app.db import Post ,create_db, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from sqlalchemy import select

@asynccontextmanager
async def life(app :FastAPI):
	await create_db()
	yield 



app=FastAPI(lifespan=life)

text={1:{ "title": "new post"}}

@app.get("/hellow")
def hellow():
	return {"message":"hellow"}

@app.get("/post/{id}")
def post(id :int):
	if id not in text:
		raise HTTPException(status_code=404,detail="not found")

	return text[id]
@app.post("/posts")
def make_user(post : userbase):
	newp={"user_id":post.uid,"user_password":post.upw}
	text[max(text.keys())+1]=newp
	return newp 

@app.post("/transictions")
async def tras (post :userbase ,session: AsyncSession =Depends(get_async_session)):
	postt=Post(
		 uid=post.uid,
		 upw=post.upw,
		 amount=post.amount,
		 reg=post.reg
		)
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

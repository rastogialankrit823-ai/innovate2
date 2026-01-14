from pydantic import BaseModel



class userbase(BaseModel):
    uid: str
    upw: str 
    amount: str
    reg : str

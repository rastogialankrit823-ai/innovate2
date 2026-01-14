from pydantic import BaseModel



class userbase(BaseModel):
    uid: str
    upw: str 
    amount: int
    reg : str
class userb(BaseModel):
    id: str
    pw :str

from fastapi import FastAPI,APIRouter,Depends,status,HTTPException
from sqlalchemy.orm import Session
from datetime import timedelta
from db import connect
from models.sqlmodels import User,Item
from secure import get_current_active_user,create_access_token,get_password_hash,authenticate_user,RoleChecker
from models.schemas import Token,TokenData,UserBase,UserList,ItemBase,ItemList
from fastapi.security import OAuth2PasswordRequestForm
from typing import List
user_router=APIRouter()

@user_router.post('/register')
async def create_user(user:UserBase,db:Session=Depends(connect)):
    user_db=db.query(User).filter(User.username==user.username).first()
    if user_db:
        raise HTTPException(detail='username already exixt',status_code=403)
    password=get_password_hash(user.password)
    user_db=User(**user.dict())
    user_db.password=password 
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db 

@user_router.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm=Depends(),db:Session=Depends(connect)
) -> Token:
    user = authenticate_user(form_data.username, form_data.password,db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username,'role':user.role}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@user_router.post('/item/new')
async def create_item(req:ItemBase,
    user_id:int,
    user:bool=Depends(RoleChecker(allowed_methods=['teacher','admin','student'])),
    db:Session=Depends(connect)):
    item=Item(**req.dict(),owner_id=user_id)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
    
    
@user_router.get('/all',response_model=List[UserList])
async def get_all_users(db:Session=Depends(connect),user:bool=Depends(RoleChecker(allowed_methods=['admin']))):
    return db.query(User).all()

@user_router.get('/{username}')
async def get_user(username:str,db:Session=Depends(connect)):
    return db.query(User).filter(User.username==username).first()

@user_router.get('/{id}',response_model=UserList)
async def get_user_items(id:int,db:Session=Depends(connect)):
    return db.query(User).filter(User.id==id).first()

@user_router.get("/users/me/")
async def read_users_me(
    current_user:User=Depends(get_current_active_user),
    user:bool=Depends(RoleChecker(allowed_methods=['teacher','student','admin'])),
):
    return current_user

@user_router.get("/users/me/items/")
async def read_own_items(
    current_user:User=Depends(get_current_active_user),
):
    return [{"item_id": "Foo", "owner": current_user.username}]
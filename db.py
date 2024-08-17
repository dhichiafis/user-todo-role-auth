from sqlalchemy.orm import Session,sessionmaker

from sqlalchemy import create_engine

DATABASE='sqlite:///./useroleaut.db'

engine=create_engine(DATABASE)

SessionFactory=sessionmaker(autocommit=False,autoflush=False,bind=engine)


def connect():
    db=SessionFactory() 
    try:
        yield db 
    finally:
        db.close()
        
        
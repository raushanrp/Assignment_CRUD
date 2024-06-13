'''
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


#SQLALCHEMY_DATABASE_URL='postgresql://<username>:<password>@<ip-adress/hostname>/<database_name>'


SQLALCHEMY_DATABASE_URL='postgresql://postgres:Raushan%4012@localhost/fastapi'


engine=create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal=sessionmaker(autocommit=False,autoflash=False,bind=engine)


Base = declarative_base()


def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close() 

        '''


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database URL
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:Raushan%4012@localhost/fastapi'

# Create engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create session local class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

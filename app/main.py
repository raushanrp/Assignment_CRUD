
'''
from fastapi import FastAPI,Response,status,HTTPException,Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models
from .database import engine,get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

   

class Post (BaseModel):
    title: str
    content: str
    published: bool=True
    #rating : Optional[int]=None
while True:
    try:
        conn=psycopg2.connect(host='localhost', database='fastapi',user='postgres',password='Raushan@12',cursor_factory=RealDictCursor)
        cursor=conn.cursor()
        print("database connection was successfull!")
        break

    except Exception as error:
        print("Connecting to database failed")
        print("Error: ",error)
        time.sleep(2)

my_posts= [{"title": "title of post 1", "content": "content of post 1","id": 1},
           {"title": "spicy foods", "content": "i like butter chicken", "id": 2}]


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/sqlalchemy")
def test_posts(db: Session= Depends(get_db)):

    posts=  db.query(models.Post).all()
    return {"data": posts}





@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts """)
    posts=cursor.fetchall()
    print(posts)
    return {"data": posts}
    

@app.get("/posts")
def get_posts(db: Session= Depends(get_db)):
    posts=db.query(models.Post).all()
    return {"data": posts}

#@app.post("/createposts")
#def create_posts(payload: dict=Body(...)):
   # print (payload)
    #return {"posts": f"title {payload['title']} content: {payload['content']}"}
def find_post(id):
    for p in my_posts:
        if p['id']==id:
            return p

def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p['id']==id:
            return i
        


@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(post:Post):
    #print (post)
    #print (post.dict())
    #post_dict=post.dict()
   # post_dict['id']=randrange(0,10000000)
   # my_posts.append(post_dict)
     cursor.execute("""INSERT INTO POSTS (title,content,published) VALUES (%s,%s,%s) RETURNING * """,(post.title,post.content,post.published))
     new_post=cursor.fetchone()
     conn.commit()
     return {"data": new_post}
    #return {"data":my_posts}

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(post:Post,db: Session= Depends(get_db)):
   # new_post=models.post(title=post.title,content=post.title,published=post.published)

    new_post=models.post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {"data":new_post}
    





@app.get("/posts/{id}")
def get_posts(id: int,response: Response):
   # print (id)
   cursor.execute("""SELECT * FROM posts WHERE id=%s""",(str(id)))
   post=cursor.fetchone()
  # x=find_post(int(id))
   if not post:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} was not found")
       #response.status_code=status.HTTP_404_NOT_FOUND
       #return {'message': f"post with this id: {id} was not found"}
   #print(x)
   return {"post_data": post}

@app.get("/posts/{id}")
def get_posts(id: int,response: Response,db: Session= Depends(get_db)):
   post=db.query(models.post).filter(models.Post.id==id).first()
   print(post)
   if not post:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} was not found")
       #response.status_code=status.HTTP_404_NOT_FOUND
       #return {'message': f"post with this id: {id} was not found"}
   #print(x)
   return {"post_data": post}






@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index= find_index_post(int(id))
    if index==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id :{id} does not exist")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)



@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db: Session= Depends(get_db)):
   # cursor.execute("""DELETE FROM posts WHERE id=%s returning *""",(str(id),))
   # deleted_pos=cursor.fetchone()
    #conn.commit()
    post= db.query(models.Post).filter(models.Post.id==id)
    if post.first()==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id :{id} does not exist")
    post.delete(synchronize_session=False)
    post.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)





@app.put("/posts/{id}")
def update_post(id: int,post= Post):
    index= find_index_post(id)

    if index==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id :{id} does not exist")
    
    post_dict=post.dict()
    post_dict['id']=id
    my_posts[index]=post_dict
    return {"data": post_dict}
    

@app.put("/posts/{id}")
def update_post(id: int,updated_post= Post,db: Session= Depends(get_db)):
   # cursor.execute("""UPDATE posts SET title=%s,content=%s,published=%s WHERE id=%s RETURNING *""",(post.title,post.content,post.published,str(id)))
   # updated_posts=cursor.fetchone()
   # conn.commit()

    post_query=db.query(models.Post).filter(models.post.id==id)
    post=post_query.first()

    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id :{id} does not exist")
    
    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    return {"data": post_query.first()}


    '''
'''
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import models, schemas
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from . import models, schemas
from .database import engine, get_db

# Create the database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/create_configuration", response_model=schemas.ConfigurationResponse, status_code=201)
def create_configuration(config: schemas.ConfigurationCreate, db: Session = Depends(get_db)):
    db_config = models.Configuration(country_code=config.country_code, requirements=config.requirements)
    db.add(db_config)
    db.commit()
    db.refresh(db_config)
    return db_config

@app.get("/get_configuration/{country_code}", response_model=schemas.ConfigurationResponse)
def get_configuration(country_code: str, db: Session = Depends(get_db)):
    config = db.query(models.Configuration).filter(models.Configuration.country_code == country_code).first()
    if not config:
        raise HTTPException(status_code=404, detail="Configuration not found")

    return config

@app.post("/update_configuration/{country_code}", response_model=schemas.ConfigurationResponse)
def update_configuration(country_code: str, config_update: schemas.ConfigurationUpdate, db: Session = Depends(get_db)):
    config = db.query(models.Configuration).filter(models.Configuration.country_code == country_code).first()
    if not config:
        raise HTTPException(status_code=404, detail="Configuration not found")
    for key, value in config_update.requirements.items():
        config.requirements[key] = value
    db.commit()
    db.refresh(config)
    return config

@app.delete("/delete_configuration/{country_code}", status_code=204)
def delete_configuration(country_code: str, db: Session = Depends(get_db)):
    config = db.query(models.Configuration).filter(models.Configuration.country_code == country_code).first()
    if not config:
        raise HTTPException(status_code=404, detail="Configuration not found")
    db.delete(config)
    db.commit()
    return {"message": "Configuration deleted successfully"}
'''



from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from . import models, schemas
from .database import engine, get_db

# Create the database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/create_configuration", response_model=schemas.ConfigurationResponse, status_code=201)
def create_configuration(config: schemas.ConfigurationCreate, db: Session = Depends(get_db)):
    db_config = models.Configuration(country_code=config.country_code, requirements=config.requirements)
    db.add(db_config)
    db.commit()
    db.refresh(db_config)
    return db_config

@app.get("/get_configuration/{country_code}", response_model=schemas.ConfigurationResponse)
def get_configuration(country_code: str, db: Session = Depends(get_db)):
    config = db.query(models.Configuration).filter(models.Configuration.country_code == country_code).first()
    if not config:
        raise HTTPException(status_code=404, detail="Configuration not found")
    return config

@app.post("/update_configuration/{country_code}", response_model=schemas.ConfigurationResponse)
def update_configuration(country_code: str, config_update: schemas.ConfigurationUpdate, db: Session = Depends(get_db)):
    config = db.query(models.Configuration).filter(models.Configuration.country_code == country_code).first()
    if not config:
        raise HTTPException(status_code=404, detail="Configuration not found")
    config.requirements.update(config_update.requirements)
    db.commit()
    db.refresh(config)
    return config

@app.delete("/delete_configuration/{country_code}", status_code=204)
def delete_configuration(country_code: str, db: Session = Depends(get_db)):
    config = db.query(models.Configuration).filter(models.Configuration.country_code == country_code).first()
    if not config:
        raise HTTPException(status_code=404, detail="Configuration not found")
    db.delete(config)
    db.commit()
    return {"message": "Configuration deleted successfully"}

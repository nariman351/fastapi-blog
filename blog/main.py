from typing import List
from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import schemas, models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.post('/blog', status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id, db: Session = Depends(get_db)):
    # first solution
    # db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    # second better solution
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f'Blog with id of {id} not found')
    
    blog.delete(synchronize_session=False)
    db.commit()
    return f'blog with the ID {id} has been removed'

@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id, request: schemas.Blog, db: Session = Depends(get_db)):
    # first solution
    # db.query(models.Blog).filter(models.Blog.id == id).update(request, synchronize_session=False)
    # second better solution
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f'Blog with id of {id} not found')
    
    blog.update(request)
    db.commit()
    return f'ID {id} updated successfully.'

@app.get('/blog', response_model=List[schemas.ShowBlog])
def all(db: Session = Depends(get_db)):
   blogs = db.query(models.Blog).all()
   return blogs

@app.get('/blog/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
def show(id, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        # first solution
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return{'detail': f'blog with the ID {id} is not available.'}
        # Second and better solution
        raise HTTPException(
                                status_code = status.HTTP_404_NOT_FOUND,
                                detail = f'blog with the ID {id} is not available.'
                            )

    return blog

@app.post('/user')
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(
                            name=request.name,
                            email=request.email,
                            password=request.password
                            )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

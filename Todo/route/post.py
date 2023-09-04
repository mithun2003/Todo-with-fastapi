from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
import schemas, crud, oauth2


router = APIRouter(
    prefix='/todos',
    tags=['Todo']
)

@router.post("/{user_id}/create", response_model=schemas.Item)
def create_todo(user_id: int, todo: schemas.ItemCreate, db: Session = Depends(get_db),get_current_user: int =
                Depends(oauth2.get_current_user)):
    return crud.create_todo(db=db, item=todo, user_id=user_id)


@router.get("/", response_model=List[schemas.Item])
def read_todos(db: Session = Depends(get_db)):
    items = crud.get_items(db=db)
    if items is None:
        raise HTTPException(status_code=404, detail="No todo found")
    return items


@router.get("/{user_id}", response_model=List[schemas.Item])
def read_todos(user_id: int, db: Session = Depends(get_db)):
    items = crud.get_items_user(db=db, user_id=user_id)
    if items is None:
        raise HTTPException(status_code=404, detail="No todo found")
    return items

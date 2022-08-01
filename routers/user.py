from sqlalchemy.orm.session import Session
from routers.schemas import UserBase, UserDisplay
from fastapi import APIRouter, Depends
from db.database import get_db
from db.db_user import create_new_user, delete_user, update_user
from auth.oauth2 import get_current_user

router = APIRouter(prefix="/user", tags=["user"])


@router.post("", response_model=UserDisplay)
def create_user_(request: UserBase, db: Session = Depends(get_db)):
    return create_new_user(db, request)


@router.post("/{id}/update")
def update_user_(
    id: int,
    request: UserBase,
    db: Session = Depends(get_db),
    current_user: UserBase = Depends(get_current_user),
):
    return update_user(db, id, request)


@router.get("/delete/{id}")
def delete_user_(
    id: int,
    db: Session = Depends(get_db),
    current_user: UserBase = Depends(get_current_user),
):
    return delete_user(db, id)

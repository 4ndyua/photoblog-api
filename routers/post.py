import shutil
from typing import List
from sqlalchemy.orm.session import Session
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from db.db_post import create_new_post, get_all, delete_post
from db.database import get_db
from routers.schemas import UserAuth, PostBase, PostDisplay
from auth.oauth2 import get_current_user

router = APIRouter(prefix="/post", tags=["post"])

image_url_types = ["absolute", "relative"]


@router.post("", response_model=PostDisplay)
def create(
    request: PostBase,
    db: Session = Depends(get_db),
    current_user: UserAuth = Depends(get_current_user),
):
    if request.image_url_type not in image_url_types:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Parameter image_url_type can only take values 'absolute' or 'relative'.",
        )
    return create_new_post(db, request)


@router.get("/all", response_model=List[PostDisplay])
def posts_all(db: Session = Depends(get_db)):
    return get_all(db)


@router.post("/image")
def upload_image(
    image: UploadFile = File(...), current_user: UserAuth = Depends(get_current_user)
):
    filename = image.filename
    path = f"images/{filename}"

    with open(path, "w+b") as buffer:
        shutil.copyfileobj(image.file, buffer)

    return {"filename": path}


@router.post("/delete/{id}")
def delete_post_(
    id: int,
    db: Session = Depends(get_db),
    current_user: UserAuth = Depends(get_current_user),
):
    return delete_post(db, id, current_user.id)

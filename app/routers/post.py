from typing import List, Optional

from fastapi import Response, Depends, HTTPException, status, APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session

from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
)


@router.get(
    "",
    response_model=List[schemas.PostOut]
)
def get_posts(
        db: Session = Depends(get_db),
        current_user=Depends(oauth2.get_current_user),
        limit: int = 10,
        skip: int = 0,
        search: Optional[str] = ""
):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    print(limit)
    posts = (db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
             .filter(models.Post.owner_id == current_user.id)
             .outerjoin(models.Vote, models.Vote.post_id == models.Post.id)
             .filter(models.Post.title.contains(search))
             .group_by(models.Post.id)
             .limit(limit)
             .offset(skip)
             .all())
    # posts = select(models.Post).where(models.Post.owner_id == current_user.id) => new version
    return posts


@router.get(
    "/{id}",
    response_model=schemas.PostOut
)
def get_post(
        id: int,
        db: Session = Depends(get_db),
        current_user=Depends(oauth2.get_current_user)
):
    # cursor.execute("""SELECT *
    #                   FROM posts
    #                   WHERE id = %s""", (str(id),))
    # post = cursor.fetchone()
    post = (db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
            .outerjoin(models.Vote, models.Vote.post_id == models.Post.id)
            .group_by(models.Post.id)
            .filter(models.Post.id == id)
            .first())
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {id} not found")
    inner_post, votes = post
    if inner_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    return post


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.Post
)
def create_post(
        post: schemas.PostCreate,
        db: Session = Depends(get_db),
        current_user=Depends(oauth2.get_current_user)
):
    # cursor.execute("""INSERT INTO posts (title, content, p
    # ublished)
    #                   VALUES (%s, %s, %s) RETURNING *""",
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    print(current_user.email)
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.put(
    "/{id}",
    response_model=schemas.Post
)
def update_post(
        id: int,
        updated_post: schemas.PostCreate,
        db: Session = Depends(get_db),
        current_user=Depends(oauth2.get_current_user)
):
    # cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s returning *",
    #                (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {id} not found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()

    return post_query.first()


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_post(
        id: int,
        db: Session = Depends(get_db),
        current_user=Depends(oauth2.get_current_user)
):
    # cursor.execute("""DELETE
    #                   FROM posts
    #                   WHERE id = %s returning *""", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    models.Post()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {id} not found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

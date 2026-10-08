from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/vote",
    tags=["Vote"],
)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED
)
def vote(
        vote: schemas.Vote,
        db: Session = Depends(get_db),
        current_user=Depends(oauth2.get_current_user)
):
    post = db.execute(select(models.Post).where(models.Post.id == vote.post_id)).scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")

    user_id = current_user.id
    found_vote = (db.execute(select(models.Vote)
                             .where(models.Vote.post_id == vote.post_id,
                                    models.Vote.user_id == user_id))
                  .scalar_one_or_none())
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"user {user_id} has already voted on post {vote.post_id}")
        new_vote = models.Vote(post_id=vote.post_id, user_id=user_id)
        db.add(new_vote)
        db.commit()

        return {"message": "successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")

        db.delete(found_vote)
        db.commit()

        return {"message": "successfully deleted vote"}

from typing import List, Optional
from sqlalchemy.orm import Session
from ..models import Idea
from ..schemas import IdeaCreate, IdeaUpdate

def get(db: Session, id: int) -> Optional[Idea]:
    return db.query(Idea).filter(Idea.id == id).first()

def get_multi_by_owner(
    db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
) -> List[Idea]:
    return (
        db.query(Idea)
        .filter(Idea.owner_id == owner_id)
        .offset(skip)
        .limit(limit)
        .all()
    )

def create_with_owner(
    db: Session, *, obj_in: IdeaCreate, owner_id: int
) -> Idea:
    db_obj = Idea(
        **obj_in.dict(),
        owner_id=owner_id
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update(
    db: Session, *, db_obj: Idea, obj_in: IdeaUpdate
) -> Idea:
    update_data = obj_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_obj, field, value)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def remove(db: Session, *, id: int) -> Idea:
    obj = db.query(Idea).filter(Idea.id == id).first()
    db.delete(obj)
    db.commit()
    return obj
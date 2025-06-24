from typing import List, Optional
from sqlalchemy.orm import Session
from ..models import HomeItem
from ..schemas import HomeItemCreate, HomeItemUpdate

def get(db: Session, id: int) -> Optional[HomeItem]:
    return db.query(HomeItem).filter(HomeItem.id == id).first()

def get_multi_by_owner(db: Session, *, owner_id: int) -> List[HomeItem]:
    return db.query(HomeItem).filter(HomeItem.user_id == owner_id).all()

def create_with_owner(
    db: Session, *, obj_in: HomeItemCreate, owner_id: int
) -> HomeItem:
    db_obj = HomeItem(
        **obj_in.dict(),
        user_id=owner_id
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update(
    db: Session, *, db_obj: HomeItem, obj_in: HomeItemUpdate
) -> HomeItem:
    update_data = obj_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_obj, field, value)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def remove(db: Session, *, id: int) -> HomeItem:
    obj = db.query(HomeItem).filter(HomeItem.id == id).first()
    db.delete(obj)
    db.commit()
    return obj
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ....api import deps
from ....models import User
from ....schemas import HomeItem, HomeItemCreate, HomeItemUpdate
from ....crud import crud_home

router = APIRouter()

@router.get("/items", response_model=List[HomeItem])
def read_home_items(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    ユーザーのホームアイテム一覧を取得
    """
    items = crud_home.get_multi_by_owner(db=db, owner_id=current_user.id)
    return items

@router.post("/items", response_model=HomeItem)
def create_home_item(
    *,
    db: Session = Depends(deps.get_db),
    item_in: HomeItemCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    新しいホームアイテムを作成
    """
    item = crud_home.create_with_owner(
        db=db, obj_in=item_in, owner_id=current_user.id
    )
    return item

@router.put("/items/{item_id}", response_model=HomeItem)
def update_home_item(
    *,
    db: Session = Depends(deps.get_db),
    item_id: int,
    item_in: HomeItemUpdate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    ホームアイテムを更新
    """
    item = crud_home.get(db=db, id=item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if item.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    item = crud_home.update(db=db, db_obj=item, obj_in=item_in)
    return item

@router.delete("/items/{item_id}")
def delete_home_item(
    *,
    db: Session = Depends(deps.get_db),
    item_id: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    ホームアイテムを削除
    """
    item = crud_home.get(db=db, id=item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if item.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    crud_home.remove(db=db, id=item_id)
    return {"detail": "Item deleted successfully"}
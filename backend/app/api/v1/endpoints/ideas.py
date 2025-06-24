from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ....api import deps
from ....crud import crud_idea
from ....models import User
from ....schemas import Idea, IdeaCreate, IdeaUpdate

router = APIRouter()

@router.get("/", response_model=List[Idea])
def read_ideas(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    ユーザーのアイデア一覧を取得
    """
    ideas = crud_idea.get_multi_by_owner(
        db=db, owner_id=current_user.id, skip=skip, limit=limit
    )
    return ideas

@router.post("/", response_model=Idea)
def create_idea(
    *,
    db: Session = Depends(deps.get_db),
    idea_in: IdeaCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    新しいアイデアを作成
    """
    idea = crud_idea.create_with_owner(
        db=db, obj_in=idea_in, owner_id=current_user.id
    )
    return idea

@router.get("/{idea_id}", response_model=Idea)
def read_idea(
    *,
    db: Session = Depends(deps.get_db),
    idea_id: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    特定のアイデアを取得
    """
    idea = crud_idea.get(db=db, id=idea_id)
    if not idea:
        raise HTTPException(status_code=404, detail="Idea not found")
    if idea.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return idea

@router.put("/{idea_id}", response_model=Idea)
def update_idea(
    *,
    db: Session = Depends(deps.get_db),
    idea_id: int,
    idea_in: IdeaUpdate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    アイデアを更新
    """
    idea = crud_idea.get(db=db, id=idea_id)
    if not idea:
        raise HTTPException(status_code=404, detail="Idea not found")
    if idea.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    idea = crud_idea.update(db=db, db_obj=idea, obj_in=idea_in)
    return idea

@router.delete("/{idea_id}")
def delete_idea(
    *,
    db: Session = Depends(deps.get_db),
    idea_id: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    アイデアを削除
    """
    idea = crud_idea.get(db=db, id=idea_id)
    if not idea:
        raise HTTPException(status_code=404, detail="Idea not found")
    if idea.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    crud_idea.remove(db=db, id=idea_id)
    return {"detail": "Idea deleted successfully"}
from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ....api import deps
from ....models import User
from ....schemas import Requirement, RequirementGenerate
from ....services import llm_service
from ....crud import crud_idea, crud_requirement

router = APIRouter()

@router.post("/generate", response_model=Requirement)
async def generate_requirement(
    *,
    db: Session = Depends(deps.get_db),
    requirement_in: RequirementGenerate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    アイデアから要件定義書を生成
    """
    # アイデアの存在確認と権限チェック
    idea = crud_idea.get(db=db, id=requirement_in.idea_id)
    if not idea:
        raise HTTPException(status_code=404, detail="Idea not found")
    if idea.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # LLMを使って要件定義書を生成
    try:
        requirement_content = await llm_service.generate_requirement(
            idea_content=idea.content,
            idea_title=idea.title,
            llm_model=requirement_in.llm_model
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate requirement: {str(e)}")
    
    # 要件定義書を保存
    requirement = crud_requirement.create(
        db=db,
        idea_id=requirement_in.idea_id,
        content=requirement_content,
        llm_model=requirement_in.llm_model
    )
    
    return requirement
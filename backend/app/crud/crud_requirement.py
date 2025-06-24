from sqlalchemy.orm import Session
from ..models import Requirement

def create(
    db: Session, *, idea_id: int, content: str, llm_model: str
) -> Requirement:
    db_obj = Requirement(
        idea_id=idea_id,
        content=content,
        llm_model=llm_model
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj
from sqlalchemy.orm import Session
from .interview_models import Interview
from .schemas import InterviewCreate, InterviewUpdate


def create_interview(db: Session, interview: InterviewCreate):
    db_interview = Interview(**interview.model_dump())
    db.add(db_interview)
    db.commit()
    db.refresh(db_interview)
    return db_interview


def get_interview(db: Session, interview_id: int):
    return db.query(Interview).filter(
        Interview.id == interview_id
    ).first()


def get_all_interviews(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Interview).offset(skip).limit(limit).all()


def get_interviews_by_application(db: Session, application_id: int):
    return db.query(Interview).filter(
        Interview.application_id == application_id
    ).all()


def update_interview(
    db: Session,
    interview_id: int,
    interview: InterviewUpdate
):
    db_interview = get_interview(db, interview_id)

    if db_interview is None:
        return None

    update_data = interview.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_interview, key, value)

    db.commit()
    db.refresh(db_interview)

    return db_interview


def delete_interview(db: Session, interview_id: int):
    db_interview = get_interview(db, interview_id)

    if db_interview is None:
        return None

    db.delete(db_interview)
    db.commit()

    return db_interview
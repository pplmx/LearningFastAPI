from sqlmodel import Session, select

from db.base import engine
from model.user import User


def create_user(user: User):
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user


def get_users():
    with Session(engine) as session:
        statement = select(User)
        results = session.exec(statement)
        return results.all()

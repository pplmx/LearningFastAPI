from db.base import engine
from fastapi import APIRouter, HTTPException
from model.user import User
from service import user_service
from sqlmodel import Session

router = APIRouter(
    prefix="/users",
)


@router.post("/", response_model=User)
async def create_user(user: User):
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user


@router.get("/{user_id}", response_model=User)
async def get_user(user_id: int):
    return _check_user_exists(user_id)


# get users
@router.get("/", response_model=list[User])
async def get_users():
    return user_service.get_users()


@router.put("/{user_id}", response_model=User)
async def update_user(user_id: int, user: User):
    with Session(engine) as session:
        db_user = _check_user_exists(user_id)
        user_data = user.dict(exclude_unset=True)
        for key, value in user_data.items():
            setattr(db_user, key, value)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user


@router.delete("/{user_id}")
async def delete_user(user_id: int):
    with Session(engine) as session:
        user = _check_user_exists(user_id)
        session.delete(user)
        session.commit()


def _check_user_exists(user_id: int):
    with Session(engine) as session:
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

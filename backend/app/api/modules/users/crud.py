from typing import Any

from sqlalchemy import text
from sqlmodel import Session, select

from app.api.modules.users.models import UserCreate, UserUpdate
from app.api.modules.users.models import Users
from app.core.security import get_password_hash, verify_password


def create_user(*, session: Session, user_create: UserCreate) -> Users:
    db_obj = Users.model_validate(
        user_create, update={"hashed_password": get_password_hash(user_create.password)}
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_user(*, session: Session, db_user: Users, user_in: UserUpdate) -> Any:
    user_data = user_in.model_dump(exclude_unset=True)
    extra_data = {}
    if "password" in user_data:
        password = user_data["password"]
        hashed_password = get_password_hash(password)
        extra_data["hashed_password"] = hashed_password
    db_user.sqlmodel_update(user_data, update=extra_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


#
# def get_user_by_email(*, session: Session, email: str) -> Users | None:
#     statement = select(Users).where(Users.email == email)
#     user = session.exec(statement).first()
#     print("get_user_by_email() → role:", user.role)  # 🔍 debug log
#     return user

def get_user_role_by_email(session: Session, email: str) -> str:
    result = session.exec(
        text("SELECT ROLE FROM USERS WHERE EMAIL = :email"), {"email": email}
    )
    row = result.first()
    return row[0] if row else None


# def authenticate(*, session: Session, email: str, password: str) -> Users | None:
#     db_user = get_user_by_email(session=session, email=email)
#     if not db_user:
#         return None
#     if not verify_password(password, db_user.hashed_password):
#         return None
#     return db_user


def authenticate(*, session: Session, email: str, password: str) -> Users | None:
    statement = select(Users).where(Users.email == email)
    db_user = session.exec(statement).first()

    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None

    if db_user.role is None:
        db_user.role = get_user_role_by_email(session, email)

    return db_user

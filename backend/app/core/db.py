from sqlmodel import Session, create_engine, select

from app.api.modules.users import crud
from app.api.modules.users.models import Users, UserCreate
from app.core.config import settings

# engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI), echo=True)

# engine = create_engine(str(settings.DATABASE_URL))

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, echo=True)


# Dependency injection için gerekli
def get_session():
    with Session(engine) as session:
        yield session


def init_db(session: Session) -> None:
    # Alembic ile migration yapıyorsak create_all() kullanmayacağız
    # from sqlmodel import SQLModel
    # SQLModel.metadata.create_all(engine)

    user = session.exec(
        select(Users).where(Users.email == settings.FIRST_SUPERUSER)
    ).first()
    if not user:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user = crud.create_user(session=session, user_create=user_in)

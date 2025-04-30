import logging

from sqlmodel import Session

# from app import utils
from app.api.modules.users import models
from app.core import security
from app.core.config import settings
from app.core.db import engine, init_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init() -> None:
    with Session(engine) as session:
        init_db(session)


def main() -> None:
    logger.info("Creating initial data")
    init()
    logger.info("Initial data created")


def init_db(db: Session) -> None:
    user = db.query(models.Users).filter(models.Users.email == settings.FIRST_SUPERUSER).first()
    if not user:
        new_user = models.Users(
            email=settings.FIRST_SUPERUSER,
            hashed_password=security.get_password_hash(settings.FIRST_SUPERUSER_PASSWORD),
            is_superuser=1,
            is_active=1,
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)


if __name__ == "__main__":
    main()

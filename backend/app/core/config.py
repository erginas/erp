import warnings
from typing import Annotated, Any, Literal

from pydantic import (
    AnyUrl,
    BeforeValidator,
    EmailStr,
    HttpUrl,
    computed_field,
    model_validator,
)
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing_extensions import Self


def parse_cors(v: Any) -> list[str] | str:
    """
    Parses CORS origins from a string or list.
    """
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, (list, str)):
        return v
    raise ValueError(v)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        # Use top level .env file (one level above ./backend/)
        env_file="../.env",
        env_ignore_empty=True,
        extra="ignore",
    )

    # Application settings
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "L8pp16HsuFwUyTq7DBBOQ8LxQDvLjEli9YX-bbOqOts"  # secrets.token_urlsafe(32)
    # print(SECRET_KEY)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    FRONTEND_HOST: str = "http://localhost:5173"
    # print(SECRET_KEY)
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"

    # CORS settings
    BACKEND_CORS_ORIGINS: Annotated[
        list[AnyUrl] | str, BeforeValidator(parse_cors)
    ] = []

    @computed_field  # type: ignore[prop-decorator]
    @property
    def all_cors_origins(self) -> list[str]:
        """
        Combines CORS origins with the frontend host.
        """
        return [str(origin).rstrip("/") for origin in self.BACKEND_CORS_ORIGINS] + [
            self.FRONTEND_HOST
        ]

    # Project settings
    PROJECT_NAME: str = "enginin projesi"
    SENTRY_DSN: HttpUrl | None = None

    # Oracle database settings
    # ORACLE_SERVER: str = "cloud.tipsan.com"
    ORACLE_SERVER: str = "192.168.0.253"
    # ORACLE_PORT: int = 3521
    ORACLE_PORT: int = 1521
    ORACLE_USER: str = "mgp"
    ORACLE_PASSWORD: str = "mgp"
    ORACLE_DB: str = "tpsn"  # SID veya Service Name
    ORACLE_USE_SERVICE_NAME: bool = False  # True ise Service Name, False ise SID
    ORACLE_DRIVER_MODE: Literal['thin', 'thick'] = 'thin'

    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        query_params = {}
        if self.ORACLE_DRIVER_MODE == "thick":
            query_params['mode'] = 'thick'

        if self.ORACLE_USE_SERVICE_NAME:
            query_params['service_name'] = self.ORACLE_DB
            path = ""
        else:
            # path = self.ORACLE_DB
            path = f"{self.ORACLE_DB}"
            # print(path)

        # Convert query_params dictionary to a query string
        from urllib.parse import urlencode
        query_string = urlencode(query_params) if query_params else None
        # print(query_string)

        dsn = MultiHostUrl.build(
            scheme="oracle+oracledb",
            username=self.ORACLE_USER,
            password=self.ORACLE_PASSWORD,
            host=self.ORACLE_SERVER,
            port=self.ORACLE_PORT,
            path=path,
            query=query_string  # Pass the query string here
        )
        # print("dsn yazdırıldı",dsn)
        return str(dsn)

    # Email settings
    SMTP_TLS: bool = True
    SMTP_SSL: bool = False
    SMTP_PORT: int = 587
    SMTP_HOST: str | None = None
    SMTP_USER: str | None = None
    SMTP_PASSWORD: str | None = None
    EMAILS_FROM_EMAIL: EmailStr | None = None
    EMAILS_FROM_NAME: EmailStr | None = None

    @model_validator(mode="after")
    def _set_default_emails_from(self) -> Self:
        """
        Sets default email sender name if not provided.
        """
        if not self.EMAILS_FROM_NAME:
            self.EMAILS_FROM_NAME = self.PROJECT_NAME
        return self

    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48

    @computed_field  # type: ignore[prop-decorator]
    @property
    def emails_enabled(self) -> bool:
        """
        Checks if email sending is enabled.
        """
        return bool(self.SMTP_HOST and self.EMAILS_FROM_EMAIL)

    EMAIL_TEST_USER: EmailStr = "test@example.com"
    FIRST_SUPERUSER: EmailStr = "engin@engin.com"
    FIRST_SUPERUSER_PASSWORD: str = "12345678"

    def _check_default_secret(self, var_name: str, value: str | None) -> None:
        """
        Validates that sensitive values are not using default secrets.
        """
        if value == "changethis":
            message = (
                f'The value of {var_name} is "changethis", '
                "for security, please change it, at least for deployments."
            )
            if self.ENVIRONMENT == "local":
                warnings.warn(message, stacklevel=1)
            else:
                raise ValueError(message)

    @model_validator(mode="after")
    def _enforce_non_default_secrets(self) -> Self:
        """
        Enforces non-default secrets for sensitive fields.
        """
        self._check_default_secret("SECRET_KEY", self.SECRET_KEY)
        self._check_default_secret("ORACLE_PASSWORD", self.ORACLE_PASSWORD)
        self._check_default_secret(
            "FIRST_SUPERUSER_PASSWORD", self.FIRST_SUPERUSER_PASSWORD
        )
        return self


settings = Settings()  # type: ignore

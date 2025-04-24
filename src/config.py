from pydantic_settings import BaseSettings


class Settings(BaseSettings):
	APP_NAME: str = "ShopNow Server"
	ACCESS_TOKEN_EXPIRE_MINUTES = 30
	REFRESH_TOKEN_EXPIRE_MINUTES = 10

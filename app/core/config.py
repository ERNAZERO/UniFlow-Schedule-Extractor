from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    APP_NAME: str = Field(default="Schedule Extractor API")
    APP_VERSION: str = Field(default="0.1.0")
    ENV: str = Field(default="dev")

    OLLAMA_BASE_URL: str = "http://127.0.0.1:11434"
    OLLAMA_MODEL: str = "llama3.2"
    OLLAMA_TEMPERATURE: float = 0.0
    OLLAMA_KEEP_ALIVE: str = "30m"
    OLLAMA_NUM_CTX: int = 2048
    OLLAMA_NUM_BATCH: int = 32
    OLLAMA_NUM_THREAD: int = 6

    BGE_MODEL_NAME: str = "BAAI/bge-base-en-v1.5"
    VECTORSTORE_DIR: str = "/tmp/vs_index"


settings = Settings()
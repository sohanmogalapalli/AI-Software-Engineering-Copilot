from typing import Optional
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    # LLM Provider & Model Configuration
    # Options: "auto", "gemini", "groq", "grok", "ollama"
    LLM_PROVIDER: str = Field(default="gemini")
    LLM_MODEL: str = Field(default="gemini-3-flash-preview")
    EMBEDDING_MODEL: str = Field(default="nomic-embed-text:latest")
    
    # Cloud API Keys
    GEMINI_API_KEY: Optional[str] = Field(default=None)
    GROK_API_KEY: Optional[str] = Field(default=None)
    GROQ_API_KEY: Optional[str] = Field(default=None)

    # Ollama Local Service Configuration
    OLLAMA_BASE_URL: str = Field(default="http://localhost:11434")
    
    # Storage Paths (relative to PROJECT_ROOT or absolute)
    VECTOR_STORE_PATH: str = Field(default="data/vector_store")
    REPOSITORY_PATH: str = Field(default="data/repositories")
    CHUNK_PATH: str = Field(default="data/chunks")
    INDEX_PATH: str = Field(default="data/indexes")
    
    # Retrieval Configuration
    TOP_K: int = Field(default=8)
    SIMILARITY_THRESHOLD: float = Field(default=0.25)
    RRF_K: int = Field(default=60)
    
    # Server Configuration
    HOST: str = Field(default="127.0.0.1")
    PORT: int = Field(default=8000)
    
    @property
    def vector_store_dir(self) -> Path:
        p = Path(self.VECTOR_STORE_PATH)
        return p if p.is_absolute() else PROJECT_ROOT / p

    @property
    def repository_dir(self) -> Path:
        p = Path(self.REPOSITORY_PATH)
        return p if p.is_absolute() else PROJECT_ROOT / p

    @property
    def chunk_dir(self) -> Path:
        p = Path(self.CHUNK_PATH)
        return p if p.is_absolute() else PROJECT_ROOT / p

    @property
    def index_dir(self) -> Path:
        p = Path(self.INDEX_PATH)
        return p if p.is_absolute() else PROJECT_ROOT / p

    model_config = SettingsConfigDict(
        env_file=str(PROJECT_ROOT / ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()

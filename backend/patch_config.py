with open("app/core/config.py", "r") as f:
    content = f.read()

new_imports = """import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import model_validator
from dotenv import load_dotenv"""

content = content.replace("import os\nfrom pathlib import Path\n\nfrom dotenv import load_dotenv", new_imports)

content = content.replace("class Settings:", "class Settings(BaseSettings):")

content = content.replace(
    'ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")',
    'ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")\n    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:3000")'
)

new_tail = """
    model_config = SettingsConfigDict(
        env_file=str(env_path),
        extra="ignore",
    )

    @model_validator(mode="after")
    def validate_secret_key(self) -> 'Settings':
        if self.ENVIRONMENT == "production" and self.SECRET_KEY == "default_secret_key_change_in_production":
            raise ValueError("SECRET_KEY must be set in production")
        return self

settings = Settings()
"""
content = content.replace("settings = Settings()", new_tail.strip())

with open("app/core/config.py", "w") as f:
    f.write(content)

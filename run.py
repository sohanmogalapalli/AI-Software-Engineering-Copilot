import sys
from pathlib import Path
import uvicorn
from backend.utils.config import settings
from backend.utils.logging import logger

def main():
    logger.info(f"Starting Copilot on http://{settings.HOST}:{settings.PORT}")
    uvicorn.run(
        "backend.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True
    )

if __name__ == "__main__":
    main()

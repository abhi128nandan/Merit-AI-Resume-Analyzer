import asyncio
from app.core.database import get_db
from sqlalchemy import text

async def main():
    try:
        # Get a session via the generator
        async for session in get_db():
            result = await session.execute(text("SELECT 1"))
            value = result.scalar()
            print(f"Database connection verified! SELECT 1 returned: {value}")
            break
    except Exception as e:
        print(f"Database connection failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())

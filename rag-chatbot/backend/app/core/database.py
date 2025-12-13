import asyncpg
import logging
from typing import Optional
from app.core.config import settings, DATABASE_URL

logger = logging.getLogger(__name__)

class DatabaseManager:
    """Manage database connections and operations"""

    _pool: Optional[asyncpg.Pool] = None

    @classmethod
    async def initialize(cls):
        """Initialize database connection pool"""
        try:
            cls._pool = await asyncpg.create_pool(
                DATABASE_URL,
                min_size=2,
                max_size=10,
                command_timeout=60
            )
            logger.info("Database connection pool created successfully")
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            raise

    @classmethod
    async def execute_query(cls, query: str, *args):
        """Execute a query and return results"""
        if not cls._pool:
            raise RuntimeError("Database not initialized")

        async with cls._pool.acquire() as connection:
            try:
                result = await connection.fetch(query, *args)
                return result
            except Exception as e:
                logger.error(f"Query execution failed: {e}")
                raise

    @classmethod
    async def execute_command(cls, command: str, *args):
        """Execute a command (INSERT, UPDATE, DELETE)"""
        if not cls._pool:
            raise RuntimeError("Database not initialized")

        async with cls._pool.acquire() as connection:
            try:
                await connection.execute(command, *args)
            except Exception as e:
                logger.error(f"Command execution failed: {e}")
                raise

    @classmethod
    async def close(cls):
        """Close database connection pool"""
        if cls._pool:
            await cls._pool.close()
            cls._pool = None
            logger.info("Database connection pool closed")

async def init_database():
    """Initialize database and create tables"""
    try:
        # Initialize database manager
        await DatabaseManager.initialize()

        # Create tables
        await create_tables()

        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise

async def create_tables():
    """Create necessary database tables"""

    # Create chat_sessions table
    create_sessions_table = """
    CREATE TABLE IF NOT EXISTS chat_sessions (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        user_id VARCHAR(255),
        session_metadata JSONB
    );
    """

    # Create chat_messages table
    create_messages_table = """
    CREATE TABLE IF NOT EXISTS chat_messages (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        session_id UUID REFERENCES chat_sessions(id) ON DELETE CASCADE,
        role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant')),
        content TEXT NOT NULL,
        context_sources JSONB,
        metadata JSONB,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );
    """

    # Create content_chunks table
    create_chunks_table = """
    CREATE TABLE IF NOT EXISTS content_chunks (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        file_path TEXT NOT NULL,
        chunk_index INTEGER NOT NULL,
        content TEXT NOT NULL,
        metadata JSONB,
        vector_id TEXT NOT NULL,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );
    """

    # Create indexes
    create_indexes = [
        "CREATE INDEX IF NOT EXISTS idx_chat_messages_session_id ON chat_messages(session_id);",
        "CREATE INDEX IF NOT EXISTS idx_chat_messages_created_at ON chat_messages(created_at);",
        "CREATE INDEX IF NOT EXISTS idx_content_chunks_file_path ON content_chunks(file_path);",
        "CREATE INDEX IF NOT EXISTS idx_content_chunks_vector_id ON content_chunks(vector_id);",
    ]

    # Execute table creation
    await DatabaseManager.execute_command(create_sessions_table)
    await DatabaseManager.execute_command(create_messages_table)
    await DatabaseManager.execute_command(create_chunks_table)

    # Execute index creation
    for index_query in create_indexes:
        await DatabaseManager.execute_command(index_query)

    logger.info("Database tables created successfully")

# Export database manager
db = DatabaseManager
import os
from asyncmy import create_pool, Pool

db_pool: Pool = None

async def init_db():
    global db_pool
    db_pool = await create_pool(
        host=os.getenv("DB_HOST", "asistencia-server.mysql.database.azure.com"),
        port=int(os.getenv("DB_PORT", 3306)),
        user=os.getenv("DB_USER", "qmvcqgjjvf"),
        password=os.getenv("DB_PASSWORD", ""),
        db=os.getenv("DB_NAME", "asistencia-database"),
        autocommit=True,  # Prevents explicit commits, good for web apps
        minsize=1,
        maxsize=10       # Keep it small for local testing
    )
    
    async with db_pool.acquire() as conn:
        async with conn.cursor() as cur:
            # Create tables (MySQL syntax)
            await cur.execute("""
                CREATE TABLE IF NOT EXISTS classes (
                    id INTEGER PRIMARY KEY AUTO_INCREMENT,
                    name VARCHAR(255) NOT NULL,
                    description TEXT
                )
            """)
            await cur.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTO_INCREMENT,
                    name VARCHAR(255) NOT NULL,
                    class_id INTEGER NOT NULL,
                    FOREIGN KEY (class_id) REFERENCES classes (id) ON DELETE CASCADE
                )
            """)
            await cur.execute("""
                CREATE TABLE IF NOT EXISTS attendance (
                    id INTEGER PRIMARY KEY AUTO_INCREMENT,
                    student_id INTEGER NOT NULL,
                    date DATE NOT NULL,
                    status ENUM('Present', 'Absent', 'Late') NOT NULL,
                    FOREIGN KEY (student_id) REFERENCES students (id) ON DELETE CASCADE,
                    UNIQUE KEY unique_attendance (student_id, date)
                )
            """)

async def get_db():
    async with db_pool.acquire() as conn:
        yield conn

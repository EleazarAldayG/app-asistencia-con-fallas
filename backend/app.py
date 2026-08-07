from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from typing import List, Optional
from database import init_db, get_db
from dotenv import load_dotenv
from schemas import (
    ClassCreate, ClassUpdate, ClassOut,
    StudentCreate, StudentUpdate, StudentOut,
    AttendanceBatchCreate, AttendanceOut
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

load_dotenv()

app = FastAPI(lifespan=lifespan)

# --- CORS Configuration (Required for separate frontend) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend domain, e.g., ["https://your-app.netlify.app"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== CLASSES CRUD ====================
@app.get("/api/classes", response_model=List[ClassOut])
async def get_classes(db=Depends(get_db)):
    async with db.cursor() as cur:
        await cur.execute("SELECT id, name, description FROM classes ORDER BY name")
        rows = await cur.fetchall()
        return [{"id": r[0], "name": r[1], "description": r[2]} for r in rows]

@app.post("/api/classes", response_model=ClassOut)
async def create_class(cls: ClassCreate, db=Depends(get_db)):
    async with db.cursor() as cur:
        await cur.execute(
            "INSERT INTO classes (name, description) VALUES (%s, %s)",
            (cls.name, cls.description)
        )
        return {"id": cur.lastrowid, "name": cls.name, "description": cls.description}

@app.put("/api/classes/{class_id}", response_model=ClassOut)
async def update_class(class_id: int, cls: ClassUpdate, db=Depends(get_db)):
    async with db.cursor() as cur:
        await cur.execute(
            "UPDATE classes SET name = %s, description = %s WHERE id = %s",
            (cls.name, cls.description, class_id)
        )
        return {"id": class_id, "name": cls.name, "description": cls.description}

@app.delete("/api/classes/{class_id}")
async def delete_class(class_id: int, db=Depends(get_db)):
    async with db.cursor() as cur:
        await cur.execute("DELETE FROM classes WHERE id = %s", (class_id,))
    return {"ok": True}

# ==================== STUDENTS CRUD ====================
@app.get("/api/students", response_model=List[StudentOut])
async def get_students(class_id: Optional[int] = None, db=Depends(get_db)):
    async with db.cursor() as cur:
        if class_id:
            await cur.execute("SELECT id, name, class_id FROM students WHERE class_id = %s ORDER BY name", (class_id,))
        else:
            await cur.execute("SELECT id, name, class_id FROM students ORDER BY name")
        rows = await cur.fetchall()
        return [{"id": r[0], "name": r[1], "class_id": r[2]} for r in rows]

@app.post("/api/students", response_model=StudentOut)
async def create_student(stu: StudentCreate, db=Depends(get_db)):
    async with db.cursor() as cur:
        await cur.execute(
            "INSERT INTO students (name, class_id) VALUES (%s, %s)",
            (stu.name, stu.class_id)
        )
        return {"id": cur.lastrowid, "name": stu.name, "class_id": stu.class_id}

@app.put("/api/students/{student_id}")
async def update_student(student_id: int, stu: StudentUpdate, db=Depends(get_db)):
    async with db.cursor() as cur:
        # Directly updates without checking if student_id exists
        await cur.execute("UPDATE students SET name = %s, class_id = %s WHERE id = %s",
                          (stu.name, stu.class_id, student_id))
        # Always returns 200, even if 0 rows were affected!
        return {"id": student_id, "name": stu.name, "class_id": stu.class_id}

@app.delete("/api/students/{student_id}")
async def delete_student(student_id: int, db=Depends(get_db)):
    async with db.cursor() as cur:
        await cur.execute("DELETE FROM students WHERE id = %s", (student_id,))
    return {"ok": True}

# ==================== ATTENDANCE CRUD ====================
@app.post("/api/attendance/batch")
async def create_or_update_attendance(batch: AttendanceBatchCreate, db=Depends(get_db)):
    async with db.cursor() as cur:
        for record in batch.records:
            # MySQL specific: ON DUPLICATE KEY UPDATE
            await cur.execute(
                """
                INSERT INTO attendance (student_id, date, status) 
                VALUES (%s, %s, %s) 
                ON DUPLICATE KEY UPDATE status = VALUES(status)
                """,
                (record.student_id, batch.date, record.status)
            )
    return {"ok": True}

@app.get("/api/attendance", response_model=List[AttendanceOut])
async def get_attendance(
    student_id: Optional[int] = None, 
    date: Optional[str] = None,
    db=Depends(get_db)
):
    query = "SELECT id, student_id, date, status FROM attendance WHERE 1=1"
    params = []
    if student_id:
        query += f" AND student_id = {student_id}"  # VULNERABLE!
        # query += " AND student_id = %s" # SEGURO
        params.append(student_id)
    if date:
        query += f" AND date = '{date}'" # VULNERABLE!
        # query += " AND date = %s" # SEGURO
        params.append(date)
    query += " ORDER BY date DESC, student_id"

    async with db.cursor() as cur:
        await cur.execute(query) 
    #    await cur.execute(query, params)
    #    rows = await cur.fetchall()
    #    return [{"id": r[0], "student_id": r[1], "date": str(r[2]), "status": r[3]} for r in rows]

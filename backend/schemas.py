from pydantic import BaseModel
# from pydantic import BaseModel, Field, constr
from typing import Optional, List

# --- Classes ---
class ClassBase(BaseModel):
    name: str
    description: Optional[str] = None

class ClassCreate(ClassBase):
    pass

class ClassUpdate(ClassBase):
    pass

class ClassOut(ClassBase):
    id: int

# --- Students ---
class StudentBase(BaseModel):
    name: str
    # name: str = Field(..., max_length=50, regex=r'^[A-Za-z\s\-]+$')
    class_id: int

class StudentCreate(StudentBase):
    pass

class StudentUpdate(StudentBase):
    pass

class StudentOut(StudentBase):
    id: int

# --- Attendance ---
class AttendanceRecord(BaseModel):
    student_id: int
    status: str  # "Present", "Absent", "Late"

class AttendanceBatchCreate(BaseModel):
    date: str  # Format: YYYY-MM-DD
    records: List[AttendanceRecord]

class AttendanceOut(BaseModel):
    id: int
    student_id: int
    date: str
    status: str
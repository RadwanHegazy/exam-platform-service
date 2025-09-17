from . import BaseModel, CassandraORM

class StudentAnswer (BaseModel) : 
    student_jwt = "TEXT"
    question_id = "INT"
    answer = "TEXT"
    created_at = "TIMESTAMP"
    exam_id = "INT"



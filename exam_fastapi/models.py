from pydantic import BaseModel
from datetime import datetime
from .cassandra_orm.models import CassandraORM, StudentAnswer as CasssandraStudentTable
import os

class StudentAnswer (BaseModel) : 
    question_id : int
    student_jwt : str
    answer : str
    exam_id : int

    def save_to_cassandra(self) : 
        "Transform the object into the correct cassandra dataset"
        data = {
            'question_id' : self.question_id,
            'student_jwt' : self.student_jwt,
            'answer' : self.answer,
            'created_at' : datetime.now(),
            'exam_id' : self.exam_id
        }

        CassandraORM.connect(
            hosts=[os.environ.get('CASSANDRA_HOST_1'), os.environ.get('CASSANDRA_HOST_2')],
            keyspace=os.environ.get('CASSANDRA_KEYSPACE')
        )

        CasssandraStudentTable.create_table()

        st_answer = CasssandraStudentTable()
        st_answer.create(**data)

        return True

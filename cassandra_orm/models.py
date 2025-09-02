import os
from . import BaseModel, CassandraORM

class StudentAnswer (BaseModel) : 
    student_id = "INT"
    question_id = "INT"
    answer = "TEXT"
    created_at = "TIMESTAMP"



if __name__ == "__main__" : 
    CassandraORM.connect(
        hosts=[os.environ.get('CASSANDRA_HOST_1'), os.environ.get('CASSANDRA_HOST_2')],
        keyspace=os.environ.get('CASSANDRA_KEYSPACE')
    )

    StudentAnswer.create_table()
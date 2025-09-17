from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import StudentDegrees, Student, Exam

class StudentDegreesResource(resources.ModelResource):
    # Use ForeignKeyWidget to handle foreign key relationships
    student = fields.Field(
        column_name='student',
        attribute='student',
        widget=ForeignKeyWidget(Student, 'id')  # Use 'id' field for import/export
    )
    
    exam = fields.Field(
        column_name='exam',
        attribute='exam',
        widget=ForeignKeyWidget(Exam, 'id')  # Use 'id' field for import/export
    )
    
    # Alternative: If you want to use other fields for lookup (e.g., name, email, etc.)
    student_name = fields.Field(
        column_name='student_name',
        attribute='student',
        widget=ForeignKeyWidget(Student, 'full_name')  # Assuming Student has full_name field
    )
    
    exam_name = fields.Field(
        column_name='exam_name',
        attribute='exam',
        widget=ForeignKeyWidget(Exam, 'name')  # Assuming Exam has name field
    )

    class Meta:
        model = StudentDegrees
        fields = ('id', 'student_name' , 'student' , 'exam_name', 'exam' , 'final_score', 'created_at')
        export_order = ('id', 'student_name' , 'student' , 'exam_name', 'exam' , 'final_score', 'created_at')
        import_id_fields = ('id',)  # Use ID as import identifier
        
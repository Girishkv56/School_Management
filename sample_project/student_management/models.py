from django.db import models


class TimeStampBaseModel(models.Model):
    """
    Abstract Model for saving created and modified times
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class StudentDetails(TimeStampBaseModel):
    """
    Model to save Student details
    """
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=False)
    email_id = models.EmailField(null=False)
    father_name = models.CharField(max_length=50, null=False)
    mother_name = models.CharField(max_length=50, null=False)
    city = models.CharField(max_length=50, null=False)
    contact = models.CharField(max_length=50, null=False, unique=True)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        db_table = "student_details"


class StudentActivities(TimeStampBaseModel):
    """
    Model to save student activities
    """
    student = models.ForeignKey(StudentDetails, on_delete=models.CASCADE, related_name="student_activities")
    activity = models.CharField(max_length=50, null=False)
    desc = models.CharField(max_length=50, null=False)

    class Meta:
        db_table = "student_activities"
        unique_together = ['student', 'activity']


class StudentGrades(TimeStampBaseModel):
    """
    Model to save grades of a student
    """
    student = models.ForeignKey(StudentDetails, on_delete=models.CASCADE, related_name="student_grades")
    maths = models.IntegerField(null=False)
    physics = models.IntegerField(null=False)
    chemistry = models.IntegerField(null=False)
    grade = models.IntegerField(null=False)
    semester = models.IntegerField(null=False)

    class Meta:
        db_table = "student_grades"
        unique_together = [['student', 'maths', 'semester'], ['student', 'physics', 'semester'], ['student', 'chemistry', 'semester']]


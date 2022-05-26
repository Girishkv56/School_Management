from rest_framework import serializers
from .models import *


class StudentActivitySerializer(serializers.ModelSerializer):
    """
    Serializer for StudentActivities queryset or instance to JSON
    """
    class Meta:
        model = StudentActivities
        fields = ("id", "activity", "desc")


class StudentGradeSerializer(serializers.ModelSerializer):
    """
    Serializer for StudentGrades queryset or instance to JSON
    """
    class Meta:
        model = StudentGrades
        fields = ("id", "maths", "physics", "chemistry", "grade", "semester")


class StudentDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for StudentDetail queryset or instance to JSON
    """
    student_activities = StudentActivitySerializer(many=True, read_only=True)
    student_grades = StudentGradeSerializer(many=True, read_only=True)

    class Meta:
        model = StudentDetails
        fields = ("id", "full_name", "first_name", "last_name", "email_id",
                  "father_name", "mother_name", "city", "contact",
                  "student_activities", "student_grades")

import json
from rest_framework import viewsets
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.decorators import method_decorator
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from student_management.models import *
from student_management.serializers import StudentDetailSerializer


class StudentView(viewsets.ModelViewSet):

    queryset = StudentDetails.objects.all()
    custom_filter_fields = ['first_name', "last_name", "city", "activity", "grade"]

    def get_serializer_class(self):
        """
        get the serializer class based on action
        """
        if self.action != "POST":
            return StudentDetailSerializer

    def get_queryset(self):
        return super(StudentView, self).get_queryset()

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_filtered_queryset(self, queryset, filters):
        """
        function to apply filters to the query set
        """
        if filters.get("activity"):
            queryset = queryset.filter(student_activities__activity=filters.pop("activity"))

        if filters.get("grade"):
            queryset = queryset.filter(student_grades__grade=filters.pop("grade"))

        return queryset.filter(**filters)

    def list(self, request, *args, **kwargs):
        """
        This function will be called when get API is called to fetch list of students
        returns list of students after applying filters
        """
        queryset = self.get_queryset()
        filters = request.GET.dict()

        # fetch queryset after applying filters
        queryset = self.get_filtered_queryset(queryset, filters)
        serializer = StudentDetailSerializer(queryset, many=True)
        return JsonResponse({
            "students": serializer.data
        })

    def create(self, request, *args, **kwargs):
        """
        This function is called when a student is being created
        Bulk creates students details
        """
        req_body = json.loads(request.body.decode())
        student_data = req_body['student_details']

        # saving multiple students to Data base along with activities
        for data in student_data:

            activities = data.pop("activities")
            student_obj = StudentDetails(**data)
            student_obj.save()

            # code to bulk insert student activities
            activity_list = [
                StudentActivities(**activity, student=student_obj) for activity in activities
            ]

            StudentActivities.objects.bulk_create(activity_list)

        return JsonResponse({
            "success": True,
        }, status=201)

    def retrieve(self, request, pk=None,  *args, **kwargs):
        """
        Fetches student with given roll number
        """

        # fetch single student data
        serializer = StudentDetailSerializer(self.get_object())
        return JsonResponse({
            "student": serializer.data
        })

    @action(detail=False, methods=["POST"])
    def add_grades(self, request, *args, **kwargs):
        """
        Function to bulk add multiple student grades
        """
        req_body = json.loads(request.body.decode())

        data = req_body['data']
        for student in data:
            student_id = student['student_id']
            student_grades = student['grades']

            # fetching student instance
            student_instance = StudentDetails.objects.get(pk=student_id)
            # saving student grades
            StudentGrades(**student_grades, student=student_instance).save()

        return JsonResponse({
            "success": True,
        }, status=201)

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from student_management.views import StudentView

router = DefaultRouter()
router.register("", StudentView)

app_name = "student_management"

urlpatterns = [
    path("", include(router.urls))
]

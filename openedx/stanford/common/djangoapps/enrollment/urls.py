"""
URL for enrollment API
"""
from django.conf import settings
from django.conf.urls import patterns, url

from .views import EnrollmentCourseRosterView
from .views import EnrollmentStatusView

urlpatterns = patterns(
    'enrollment.views',
    url(
        r'^roster/{course_key}$'.format(course_key=settings.COURSE_ID_PATTERN),
        EnrollmentCourseRosterView.as_view(),
        name='courseenrollmentroster',
    ),
    url(
        r"^status/?$",
        EnrollmentStatusView.as_view(),
        name='enrollment_status',
    ),
)

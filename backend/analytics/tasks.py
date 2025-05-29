from celery import shared_task
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from django.db.models import Avg, Count
from .models import SchoolAnalytics, SubjectPerformance, AttendanceTrend, DisciplineRecordSummary
from students.models import Student  # adjust as per your project structure
from teachers.models import Teacher
from attendance.models import AttendanceRecord
from academics.models import Grade, Subject
from discipline.models import DisciplineRecord

@shared_task
def update_school_analytics():
    """
    Periodic task to update analytics data for all schools.
    """

    schools = SchoolAnalytics.objects.all()
    today = datetime.today()
    first_day_of_month = make_aware(datetime(today.year, today.month, 1))

    for analytics in schools:
        school_user = analytics.school

        # Update totals
        analytics.total_students = Student.objects.filter(school=school_user).count()
        analytics.total_teachers = Teacher.objects.filter(school=school_user).count()

        # Calculate average attendance rate for current month
        attendance_records = AttendanceRecord.objects.filter(
            student__school=school_user,
            date__gte=first_day_of_month
        )
        if attendance_records.exists():
            avg_attendance = attendance_records.aggregate(
                avg_rate=Avg('attendance_rate')  # Adjust field name accordingly
            )['avg_rate'] or 0.0
            analytics.average_attendance_rate = avg_attendance

            # Save monthly attendance trend
            AttendanceTrend.objects.update_or_create(
                analytics=analytics,
                month=first_day_of_month,
                defaults={'attendance_rate': avg_attendance}
            )
        else:
            analytics.average_attendance_rate = 0.0

        # Calculate average performance across all subjects for current month
        grades = Grade.objects.filter(student__school=school_user)
        if grades.exists():
            avg_performance = grades.aggregate(avg_score=Avg('score'))['avg_score'] or 0.0
            analytics.average_performance = avg_performance

            # Update subject performances
            subjects = Subject.objects.all()
            for subject in subjects:
                avg_subj_score = grades.filter(subject=subject).aggregate(Avg('score'))['score__avg'] or 0.0
                SubjectPerformance.objects.update_or_create(
                    analytics=analytics,
                    subject_name=subject.name,
                    defaults={'average_score': avg_subj_score}
                )
        else:
            analytics.average_performance = 0.0

        # Calculate discipline incidents for current month
        incidents_count = DisciplineRecord.objects.filter(
            student__school=school_user,
            date_reported__gte=first_day_of_month
        ).count()

        DisciplineRecordSummary.objects.update_or_create(
            analytics=analytics,
            month=first_day_of_month,
            defaults={'incidents_reported': incidents_count}
        )

        analytics.save()


@shared_task
def test_celery_task():
    print("Celery task executed")
    return "It worked!"
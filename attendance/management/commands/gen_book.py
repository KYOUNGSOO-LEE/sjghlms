from django.core.management.base import BaseCommand
from datetime import datetime
from account.models import MyUser
from attendance.models import AttendanceBook, Grade, Class, Period, Place, Comments


class Command(BaseCommand):

    def handle(self, *args, **options):
        student_user = MyUser.objects.filter(is_student=1)
        grade_qs = Grade.objects.all()
        period_qs = Period.objects.all()
        place = Place.objects.get(place='교실')
        for user in student_user:
            for period in period_qs:
                book = AttendanceBook(user=user, date=datetime.today(), period=period, place=place)
                book.save()
        for grade in grade_qs:
            comments = Comments(date=datetime.today(), grade=grade, comments="")
            comments.save()

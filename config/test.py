from datetime import datetime
from account.models import MyUser
from attendance.models import AttendanceBook, Class, Period, Place


def gen_atdc_book():
    student_user = MyUser.objects.filter(is_student=1)
    period_qs = Period.objects.all()
    place = Place.objects.get(place='교실')
    for user in student_user:
        for period in period_qs:
            book = AttendanceBook(user=user, date=datetime.today(), period=period, place=place)
            book.save()
    return True


if __name__ == "__main__":
    gen_atdc_book()
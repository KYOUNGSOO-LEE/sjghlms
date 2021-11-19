import datetime
from django.shortcuts import render
from account.models import MyUser
from attendance.models import AttendanceBook, Class, Period, Place
from apscheduler.schedulers.background import BackgroundScheduler

from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa


sched = BackgroundScheduler()


def register(request):
    template = 'attendance/book_register.html'

    today = datetime.datetime.now()
    today_str = today.strftime('%F(%a)')

    user = request.user

    period_query = 7
    place_query = 6

    attendance_qs = AttendanceBook.objects\
        .filter(date=datetime.datetime.today())\
        .filter(user=user)\
        .filter(period__gte=7)\
        .filter(period__lte=11)
    period_qs = Period.objects.filter(period__gte=7).filter(period__lte=11)
    place_qs = Place.objects.filter(grade=int(request.user.user_code/1000))

    if request.method == 'POST':
        if request.POST.get('period') is not None:
            period_query = request.POST.get('period')
            place_query = request.POST.get('place')

    context = {
        'today': today_str,
        'user': user,
        'attendance_qs': attendance_qs,
        'period_qs': period_qs,
        'place_qs': place_qs,

        'current_period': int(period_query),
        'current_place': int(place_query),
    }

    return render(request, template, context)


def register_save(request):
    template = 'attendance/book_register.html'

    today = datetime.datetime.now()
    today_str = today.strftime('%F(%a)')

    user = request.user

    period_query = 7
    place_query = 6

    attendance_qs = AttendanceBook.objects\
        .filter(date=datetime.datetime.today())\
        .filter(user=user)\
        .filter(period__gte=7)\
        .filter(period__lte=11)
    period_qs = Period.objects.filter(period__gte=7).filter(period__lte=11)
    place_qs = Place.objects.filter(grade=int(request.user.user_code/1000))

    if request.method == 'POST':
        if request.POST.get('period') is not None:
            period_query = request.POST.get('period')
            place_query = request.POST.get('place')

    AttendanceBook.objects\
        .filter(date=datetime.datetime.today())\
        .filter(user=user)\
        .filter(period=period_query)\
        .update(place=place_query)

    context = {
        'today': today_str,
        'user': user,
        'attendance_qs': attendance_qs,
        'period_qs': period_qs,
        'place_qs': place_qs,

        'current_period': int(period_query),
        'current_place': int(place_query),
    }

    return render(request, template, context)


def book(request):
    template = 'attendance/book.html'

    today = datetime.datetime.now()
    today_str = today.strftime('%F(%a)')

    grade_query = 2
    cls_query = 1
    period_query = 7

    if request.method == 'POST':
        if request.POST.get('period') is not None:
            grade_query = request.POST.get('grade')
            cls_query = request.POST.get('cls')
            period_query = request.POST.get('period')

    cls_qs = Class.objects.all()
    period_qs = Period.objects.filter(period__gte=7).filter(period__lte=10)
    attendance_qs = AttendanceBook.objects.filter(date=datetime.datetime.today())\
        .filter(user__user_code__gte=int(grade_query)*1000+int(cls_query)*100)\
        .filter(user__user_code__lt=int(grade_query)*1000+(int(cls_query)+1)*100)
    attendance_qs = attendance_qs.order_by('user__user_code')

    context = {
        'today': today_str,

        'attendance_qs': attendance_qs,
        'period_qs': period_qs,
        'cls_qs': cls_qs,

        'current_grade': int(grade_query),
        'current_cls': int(cls_query),
        'current_period1': int(period_query),
        'current_period2': int(period_query) + 1,
    }
    return render(request, template, context)


def book_save(request):
    template = 'attendance/book.html'

    today = datetime.datetime.now()
    today_str = today.strftime('%F(%a)')

    grade_query = 2
    cls_query = 1
    period_query = 7

    cls_qs = Class.objects.all()
    period_qs = Period.objects.filter(period__gte=7).filter(period__lte=10)

    if request.method == 'POST':
        check1 = request.POST.getlist('check1')
        check2 = request.POST.getlist('check2')
        check = check1 + check2
        check.sort()
        check = [int(x) for x in check]

        grade_query = request.POST.get('hidden_grade')
        cls_query = request.POST.get('hidden_cls')
        period_query = request.POST.get('hidden_period')
        book_qs = AttendanceBook.objects\
            .filter(date=datetime.datetime.today())\
            .filter(period__gte=int(period_query))\
            .filter(period__lte=int(period_query) + 1)\
            .filter(user__user_code__gte=int(grade_query)*1000+int(cls_query)*100)\
            .filter(user__user_code__lt=int(grade_query)*1000+(int(cls_query)+1)*100)

        for el in book_qs:
            if el.id in check:
                AttendanceBook.objects.filter(id=el.id).update(check=True)
            else:
                AttendanceBook.objects.filter(id=el.id).update(check=False)

    attendance_qs = AttendanceBook.objects.filter(date=datetime.datetime.today())\
        .filter(user__user_code__gte=int(grade_query)*1000+int(cls_query)*100)\
        .filter(user__user_code__lt=int(grade_query)*1000+(int(cls_query)+1)*100)

    attendance_qs = attendance_qs.order_by('user__user_code')

    context = {
        'today': today_str,

        'attendance_qs': attendance_qs,
        'period_qs': period_qs,
        'cls_qs': cls_qs,

        'current_grade': int(grade_query),
        'current_cls': int(cls_query),
        'current_period1': int(period_query),
        'current_period2': int(period_query)+1,
    }
    return render(request, template, context)


def book_search(request):
    template = 'attendance/book_search.html'

    today = datetime.datetime.now()
    today_str = today.strftime('%F(%a)')

    grade_query = 2
    cls_query = 1

    month = datetime.date.today().month
    day = datetime.date.today().day
    year = datetime.date.today().year

    if request.method == 'POST':
        if request.POST.get('grade') is not None:
            grade_query = request.POST.get('grade')
            cls_query = request.POST.get('cls')
            date_query = request.POST.get('date')

            month = date_query[0:2]
            day = date_query[3:5]
            year = date_query[6:10]

    cls_qs = Class.objects.all()
    period_qs = Period.objects.filter(period__gte=7).filter(period__lte=11)
    attendance_qs = AttendanceBook.objects.filter(date=datetime.datetime(int(year), int(month), int(day))) \
        .filter(user__user_code__gte=int(grade_query) * 1000 + int(cls_query) * 100) \
        .filter(user__user_code__lt=int(grade_query) * 1000 + (int(cls_query) + 1) * 100)
    attendance_qs = attendance_qs.order_by('user__user_code')

    context = {
        'today': today_str,

        'attendance_qs': attendance_qs,
        'period_qs': period_qs,
        'cls_qs': cls_qs,

        'current_grade': int(grade_query),
        'current_cls': int(cls_query),
        'current_month': month,
        'current_day': day,
        'current_year': year,
    }
    return render(request, template, context)


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode('utf-8')), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type="application/pdf")
    return None


class ViewPDF(View):
    def post(self, request, *args, **kwargs):

        pdf = render_to_pdf('attendance/book_search.html', {})
        return HttpResponse(pdf, content='application/pdf')


@sched.scheduled_job('cron', hour='0', minute='0', second='1', id='gen_atdc_book')
def gen_atdc_book():
    student_user = MyUser.objects.filter(is_student=1)
    period_qs = Period.objects.all()
    place = Place.objects.get(place='교실')
    for user in student_user:
        for period in period_qs:
            book = AttendanceBook(user=user, date=datetime.datetime.today(), period=period, place=place)
            book.save()
    return True


sched.start()

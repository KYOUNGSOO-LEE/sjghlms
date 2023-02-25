import datetime
from django.shortcuts import render
from attendance.models import AttendanceBook, Grade, Class, Period, Place, Comments
from django.db.models import Q
from django.contrib.auth.decorators import user_passes_test


def register(request):
    template = 'attendance/book_register.html'

    today = datetime.datetime.now()
    today_str = today.strftime('%F(%a)')

    user = request.user

    period_query = 7
    place_query = 5

    attendance_qs = AttendanceBook.objects\
        .filter(date=datetime.datetime.today())\
        .filter(user=user)\
        .filter(period__gte=7)\
        .filter(period__lte=11)
    period_qs = Period.objects.filter(period__gte=7).filter(period__lte=11)
    place_qs = Place.objects.all()

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
    place_query = 5

    attendance_qs = AttendanceBook.objects\
        .filter(date=datetime.datetime.today())\
        .filter(user=user)\
        .filter(period__gte=7)\
        .filter(period__lte=11)
    period_qs = Period.objects.filter(period__gte=7).filter(period__lte=11)
    place_qs = Place.objects.all()

    if request.method == 'POST':
        if request.POST.get('period') is not None:
            period_query = request.POST.get('period')
            place_query = request.POST.get('place')

    try:
        check = attendance_qs.get(period=period_query).check
    except:
        check = 2

    if check == 0:
        if Place.objects.get(id=place_query) == Place.objects.get(place='외박'):
            AttendanceBook.objects \
                .filter(date=datetime.datetime.today()) \
                .filter(user=user) \
                .filter(period__gte=period_query) \
                .update(place=place_query)
        else:
            AttendanceBook.objects \
                .filter(date=datetime.datetime.today()) \
                .filter(user=user) \
                .filter(period=period_query) \
                .update(place=place_query)
    else:
        pass

    context = {
        'today': today_str,
        'user': user,
        'attendance_qs': attendance_qs,
        'period_qs': period_qs,
        'place_qs': place_qs,

        'current_period': int(period_query),
        'current_place': int(place_query),

        'check': check,
    }

    return render(request, template, context)

@user_passes_test(lambda u: u.is_staff)
def book(request):
    template = 'attendance/book.html'

    today = datetime.datetime.now()
    today_str = today.strftime('%F(%a)')

    user_code = request.user.user_code

    #조회 옵션 default
    if user_code == 77:
        grade_query = 3
    else:
        grade_query = user_code
    cls_query = 1
    place_query = '0'
    period_query = 7

    if request.method == 'POST':
        if request.POST.get('period') is not None:
            grade_query = request.POST.get('grade')
            cls_query = request.POST.get('cls')
            place_query = request.POST.get('place')
            period_query = request.POST.get('period')

    if user_code == 77:
        grade_qs = Grade.objects.all()
    else:
        grade_qs = Grade.objects.filter(grade=user_code)
    cls_qs = Class.objects.all()
    place_qs = Place.objects.all()
    period_qs = Period.objects.filter(period__gte=7).filter(period__lte=10)
    if cls_query == '0':
        if place_query == '0':
            attendance_qs = AttendanceBook.objects.filter(date=datetime.datetime.today()) \
                .filter(user__user_code__gte=int(grade_query) * 1000) \
                .filter(user__user_code__lt=(int(grade_query) + 1) * 1000)
        else:
            user_qs = AttendanceBook.objects.filter(date=datetime.datetime.today()) \
                .filter(user__user_code__gte=int(grade_query) * 1000) \
                .filter(user__user_code__lt=(int(grade_query) + 1) * 1000)\
                .filter(period=period_query)\
                .filter(place=place_query)

            user = [el.user for el in user_qs]

            attendance_qs = AttendanceBook.objects.filter(date=datetime.datetime.today()) \
                .filter(user__user_code__gte=int(grade_query) * 1000) \
                .filter(user__user_code__lt=(int(grade_query) + 1) * 1000)\
                .filter(user__in=user)
    else:
        if place_query == '0':
            attendance_qs = AttendanceBook.objects.filter(date=datetime.datetime.today()) \
                .filter(user__user_code__gte=int(grade_query) * 1000 + int(cls_query) * 100) \
                .filter(user__user_code__lt=int(grade_query) * 1000 + (int(cls_query) + 1) * 100)
        else:
            user_qs = AttendanceBook.objects.filter(date=datetime.datetime.today()) \
                .filter(user__user_code__gte=int(grade_query) * 1000) \
                .filter(user__user_code__lt=(int(grade_query) + 1) * 1000) \
                .filter(period=period_query) \
                .filter(place=place_query)

            user = [el.user for el in user_qs]

            attendance_qs = AttendanceBook.objects.filter(date=datetime.datetime.today()) \
                .filter(user__user_code__gte=int(grade_query) * 1000 + int(cls_query) * 100) \
                .filter(user__user_code__lt=int(grade_query) * 1000 + (int(cls_query) + 1) * 100)\
                .filter(user__in=user)
    attendance_qs = attendance_qs.order_by('user__user_code')

    comments_qs = Comments.objects.filter(date=datetime.datetime.today()).filter(grade=grade_query)
    try:
        comments = comments_qs.get().comments
    except:
        comments = ""

    context = {
        'today': today_str,

        'attendance_qs': attendance_qs,
        'grade_qs': grade_qs,
        'period_qs': period_qs,
        'place_qs': place_qs,
        'cls_qs': cls_qs,
        'comments': comments,

        'current_grade': int(grade_query),
        'current_cls': int(cls_query),
        'current_place': int(place_query),
        'current_period1': int(period_query),
        'current_period2': int(period_query) + 1,
    }
    return render(request, template, context)

@user_passes_test(lambda u: u.is_staff)
def book_save(request):
    template = 'attendance/book.html'

    today = datetime.datetime.now()
    today_str = today.strftime('%F(%a)')

    user_code = request.user.user_code

    #조회 옵션 default
    if user_code == 77:
        grade_query = 3
    else:
        grade_query = user_code
    cls_query = 1
    place_query = '0'
    period_query = 7

    if user_code == 77:
        grade_qs = Grade.objects.all()
    else:
        grade_qs = Grade.objects.filter(grade=user_code)
    cls_qs = Class.objects.all()
    place_qs = Place.objects.all()
    period_qs = Period.objects.filter(period__gte=7).filter(period__lte=10)

    if request.method == 'POST':
        check1 = request.POST.getlist('check1')
        check2 = request.POST.getlist('check2')
        check = check1 + check2
        check.sort()
        check = [int(x) for x in check]

        grade_query = request.POST.get('hidden_grade')
        cls_query = request.POST.get('hidden_cls')
        place_query = request.POST.get('hidden_place')
        period_query = request.POST.get('hidden_period')
        comments_query = request.POST.get('comments')

        if cls_query == '0':
            if place_query == '0':
                book_qs = AttendanceBook.objects\
                    .filter(date=datetime.datetime.today())\
                    .filter(period__gte=int(period_query))\
                    .filter(period__lte=int(period_query) + 1) \
                    .filter(user__user_code__gte=int(grade_query) * 1000) \
                    .filter(user__user_code__lt=(int(grade_query) + 1) * 1000)
            else:
                book_qs = AttendanceBook.objects \
                    .filter(date=datetime.datetime.today()) \
                    .filter(period__gte=int(period_query)) \
                    .filter(period__lte=int(period_query) + 1) \
                    .filter(user__user_code__gte=int(grade_query) * 1000) \
                    .filter(user__user_code__lt=(int(grade_query) + 1) * 1000) \
                    .filter(place=place_query)

        else:
            if place_query == '0':
                book_qs = AttendanceBook.objects \
                    .filter(date=datetime.datetime.today()) \
                    .filter(period__gte=int(period_query)) \
                    .filter(period__lte=int(period_query) + 1) \
                    .filter(user__user_code__gte=int(grade_query) * 1000 + int(cls_query) * 100) \
                    .filter(user__user_code__lt=int(grade_query) * 1000 + (int(cls_query) + 1) * 100)
            else:
                book_qs = AttendanceBook.objects \
                    .filter(date=datetime.datetime.today()) \
                    .filter(period__gte=int(period_query)) \
                    .filter(period__lte=int(period_query) + 1) \
                    .filter(user__user_code__gte=int(grade_query) * 1000 + int(cls_query) * 100) \
                    .filter(user__user_code__lt=int(grade_query) * 1000 + (int(cls_query) + 1) * 100)\
                    .filter(place=place_query)

        for el in book_qs:
            if el.id in check:
                AttendanceBook.objects.filter(id=el.id).update(check=True)
            else:
                AttendanceBook.objects.filter(id=el.id).update(check=False)

        Comments.objects.filter(date=datetime.datetime.today()).filter(grade=grade_query).update(comments=comments_query)

    if cls_query == '0':
        if place_query == '0':
            attendance_qs = AttendanceBook.objects.filter(date=datetime.datetime.today()) \
                .filter(user__user_code__gte=int(grade_query) * 1000) \
                .filter(user__user_code__lt=(int(grade_query) + 1) * 1000)
        else:
            user_qs = AttendanceBook.objects.filter(date=datetime.datetime.today()) \
                .filter(user__user_code__gte=int(grade_query) * 1000) \
                .filter(user__user_code__lt=(int(grade_query) + 1) * 1000) \
                .filter(period=period_query) \
                .filter(place=place_query)

            user = [el.user for el in user_qs]

            attendance_qs = AttendanceBook.objects.filter(date=datetime.datetime.today()) \
                .filter(user__user_code__gte=int(grade_query) * 1000) \
                .filter(user__user_code__lt=(int(grade_query) + 1) * 1000) \
                .filter(user__in=user)
    else:
        if place_query == '0':
            attendance_qs = AttendanceBook.objects.filter(date=datetime.datetime.today()) \
                .filter(user__user_code__gte=int(grade_query) * 1000 + int(cls_query) * 100) \
                .filter(user__user_code__lt=int(grade_query) * 1000 + (int(cls_query) + 1) * 100)
        else:
            user_qs = AttendanceBook.objects.filter(date=datetime.datetime.today()) \
                .filter(user__user_code__gte=int(grade_query) * 1000) \
                .filter(user__user_code__lt=(int(grade_query) + 1) * 1000) \
                .filter(period=period_query) \
                .filter(place=place_query)

            user = [el.user for el in user_qs]

            attendance_qs = AttendanceBook.objects.filter(date=datetime.datetime.today()) \
                .filter(user__user_code__gte=int(grade_query) * 1000 + int(cls_query) * 100) \
                .filter(user__user_code__lt=int(grade_query) * 1000 + (int(cls_query) + 1) * 100) \
                .filter(user__in=user)

    attendance_qs = attendance_qs.order_by('user__user_code')

    comments_qs = Comments.objects.filter(date=datetime.datetime.today()).filter(grade=grade_query)
    try:
        comments = comments_qs.get().comments
    except:
        comments = ""

    context = {
        'today': today_str,

        'attendance_qs': attendance_qs,
        'grade_qs': grade_qs,
        'period_qs': period_qs,
        'cls_qs': cls_qs,
        'place_qs': place_qs,
        'comments': comments,

        'current_grade': int(grade_query),
        'current_cls': int(cls_query),
        'current_place': int(place_query),
        'current_period1': int(period_query),
        'current_period2': int(period_query)+1,
    }
    return render(request, template, context)

@user_passes_test(lambda u: u.is_staff)
def book_search(request):
    template = 'attendance/book_search.html'

    today = datetime.datetime.now()
    today_str = today.strftime('%F(%a)')

    user_code = request.user.user_code

    if user_code == 77:
        grade_query = 3
    else:
        grade_query = user_code
    cls_query = 1

    month = datetime.date.today().month
    day = datetime.date.today().day
    year = datetime.date.today().year

    if month < 10:
        month = "0" + str(month)
    if day < 10:
        day = "0" + str(day)

    if request.method == 'POST':
        if request.POST.get('grade') is not None:
            grade_query = request.POST.get('grade')
            cls_query = request.POST.get('cls')
            date_query = request.POST.get('date')

            month = date_query[0:2]
            day = date_query[3:5]
            year = date_query[6:10]

    if user_code == 77:
        grade_qs = Grade.objects.all()
    elif user_code > 1000:
        grade_qs = Grade.objects.filter(grade=(user_code // 1000))
    else:
        grade_qs = Grade.objects.filter(grade=user_code)

    if user_code > 1000:
        cls_qs = Class.objects.filter(cls= ((user_code % 1000) // 100))
    else:
        cls_qs = Class.objects.all()

    period_qs = Period.objects.filter(period__gte=7).filter(period__lte=11)
    attendance_qs = AttendanceBook.objects.filter(date=datetime.datetime(int(year), int(month), int(day))) \
        .filter(user__user_code__gte=int(grade_query) * 1000 + int(cls_query) * 100) \
        .filter(user__user_code__lt=int(grade_query) * 1000 + (int(cls_query) + 1) * 100)
    attendance_qs = attendance_qs.order_by('user__user_code')

    comments_qs = Comments.objects.filter(date=datetime.datetime(int(year), int(month), int(day))).filter(grade=grade_query)
    try:
        comments = comments_qs.get().comments
    except:
        comments = ""

    context = {
        'today': today_str,

        'attendance_qs': attendance_qs,
        'grade_qs': grade_qs,
        'period_qs': period_qs,
        'cls_qs': cls_qs,
        'comments': comments,

        'current_grade': int(grade_query),
        'current_cls': int(cls_query),
        'current_month': month,
        'current_day': day,
        'current_year': year,
    }
    return render(request, template, context)
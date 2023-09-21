import json
import datetime
from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.utils.dateformat import DateFormat

from . import models
from django.forms import Form
from django.forms import fields
from django.forms import widgets
from django.db.models import Q
from django.db.utils import IntegrityError
import pytz

from .models import Booking

timezone = pytz.timezone('Asia/Shanghai')


class LoginForm(Form):
    id = fields.CharField(
        required=True,
        error_messages={'required': '学工号不能为空'},
        widget=widgets.TextInput(attrs={'class': 'form-control', 'placeholder': '学工号', 'id': 'id'})
    )
    password = fields.CharField(
        required=True,
        error_messages={'required': '密码不能为空'},
        widget=widgets.PasswordInput(attrs={'class': 'form-control', 'placeholder': '密码', 'id': 'password'})
    )
    rmb = fields.BooleanField(required=False, widget=widgets.CheckboxInput(attrs={'value': 1}))


def md5(val):
    import hashlib
    m = hashlib.md5()
    m.update(val.encode('utf-8'))
    return m.hexdigest()


def auth(func):
    def inner(request, *args, **kwargs):
        user_info = request.session.get('user_info')
        if not user_info:
            return redirect('/login/')
        return func(request, *args, **kwargs)

    return inner


def auth_json(func):
    def inner(request, *args, **kwargs):
        user_info = request.session.get('user_info')
        if not user_info:
            return JsonResponse({'status': False, 'msg': '用户未登录'})
        return func(request, *args, **kwargs)

    return inner


def login(request):
    """
    用户登录
    """
    if request.method == "GET":
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            rmb = form.cleaned_data.pop('rmb')
            # form.cleaned_data['password'] = md5(form.cleaned_data['password'])
            user = models.UserInfo.objects.filter(**form.cleaned_data).first()
            if user:
                request.session['user_info'] = {'id': user.id, 'name': user.name}
                if rmb:
                    request.session.set_expiry(60 * 60 * 24 * 30)
                return redirect('/index/')
            else:
                form.add_error('password', '密码错误')
                return render(request, 'login.html', {'form': form})
        else:
            return render(request, 'login.html', {'form': form})
def get_7days_date():
    tz = pytz.timezone('Asia/Shanghai')

    dates = []
    for i in range(7):
        date = datetime.datetime.now(tz) + datetime.timedelta(days=i)

        week_day = date.weekday()
        day_map = {0: '星期一', 1: '星期二', 2: '星期三', 3: '星期四', 4: '星期五', 5: '星期六', 6: '星期日'}
        week_str = day_map[week_day]

        date_str = date.strftime("%Y年%m月%d日")
        tup = (i + 1, date_str, week_str)
        dates.append(tup)

    return dates

@auth
def index(request):
    """
    会议室预定首页
    :param request: 
    :return: 
    """
    time_choices = get_7days_date()
    user_info = request.session['user_info']
    return render(request, 'index.html', {'time_choices': time_choices, 'user_info':user_info}, )


def get_days_diff(booking_date):

  booking_date = DateFormat(booking_date).format('Y-m-d')
  booking_date = datetime.datetime.strptime(booking_date, '%Y-%m-%d').date()

  today = datetime.datetime.now().date()

  delta = booking_date - today
  days = delta.days

  if days == 0:
    return 0
  elif days > 0:
    return days
  else:
    return -days


def get_booking_grid(request):
    ret = {'code': 1000, 'msg': None, 'data': None}
    current_date = datetime.datetime.now(timezone).date()
    try:
        # 计算结束日期，即当前日期 + 7天
        end_date = current_date + datetime.timedelta(days=7)
        # 构建查询条件
        query_condition = Q(booking_date__range=(current_date, end_date))
        # 查询预定数据 每次都会从数据库重新查询
        booking_list = models.Booking.objects.filter(query_condition).select_related('user', 'room').order_by(
            'booking_time').iterator()
        room_list = models.MeetingRoom.objects.all()
        booking_dict = {}
        for item in room_list:
            booking_dict[item.title] = {'1': [],
                                        '2': [],
                                        '3': []}
        #预约日期返回的是距离今天的天数 0 代表当天
        for booking in booking_list:
            bookinginfo = {'预约人': booking.username,
                           '开始时间': booking.booking_time,
                           '结束时间': booking.ending_time,
                           '用途': booking.useto,
                           '预约日期': get_days_diff(booking.booking_date)}
            booking_dict[booking.roomname][str(booking.mae_time)].append(bookinginfo)

        ret['data'] = booking_dict
    except Exception as e:
        ret['code'] = 1001
        ret['msg'] = str(e)
    return JsonResponse(ret)


@auth_json
def booking(request):
    """
    获取会议室预定情况以及预定会议室
    :param request: 
    :param date: 
    :return: 
    """
    ret = {'code': 1000, 'msg': None, 'data': None}
    current_date = datetime.datetime.now(timezone).date()
    if request.method == "GET":
        return get_booking_grid(request)
    else:
        json_data = json.loads(request.body.decode('utf-8'))
        current_date = datetime.datetime.now(timezone).date()
        useto = json_data['useto']
        booking_date = current_date + datetime.timedelta(json_data['booking_data']-1)
        booking_time = int(json_data['booking_time'])
        ending_time = int(json_data['ending_time'])
        roomname = json_data['roomname']
        room_id = models.MeetingRoom.objects.filter(title=roomname).first().id
        user_id =request.session['user_info']['id']
        maechoice = {'上午':1,'下午':2,'晚上':3}
        mae_time = maechoice[json_data['mae_time']]
        username = request.session['user_info']['name']
        user_id =request.session['user_info']['id']
        booking_instance = models.Booking()

        # 设置各个字段的值
        booking_instance.useto = useto
        booking_instance.booking_date = booking_date
        booking_instance.booking_time = booking_time
        booking_instance.ending_time = ending_time
        booking_instance.room_id = room_id
        booking_instance.user_id = user_id
        booking_instance.mae_time = mae_time
        booking_instance.username = username
        booking_instance.roomname = roomname
        all_booking = models.Booking.objects.filter(booking_date=booking_date,room_id=room_id,mae_time=mae_time)
        if len(all_booking)>0:
            for booking in all_booking:
                if (booking.booking_time <=booking_time<booking.ending_time) or (booking.booking_time<ending_time<=booking.ending_time):
                    return JsonResponse({'error': '与其他预定时间冲突，请重新选择预约时间段'}, status=400)

            # 调用 save() 方法来保存实例到数据库
            booking_instance.save()
            return JsonResponse({'data': '预定成功'})
        else:
            # 调用 save() 方法来保存实例到数据库
            booking_instance.save()
            return JsonResponse({'data': '预定成功'})


@auth
def personal(request):
    time_choices = models.Booking.booking_date_choices
    user_info = request.session['user_info']
    return render(request, 'personalbooking.html',{'time_choices': time_choices,'user_info':user_info},)

@auth_json
def bookingpersonal(request):
    """
    获取会议室预定情况以及预定会议室
    :param request:
    :param date:
    :return:
    """

    userid = request.session['user_info']['id']
    if request.method == "GET":
        return get_booking_grid_personal(request,userid)



def get_booking_grid_personal(request,userid):
    ret = {'code': 1000, 'msg': None, 'data': None}
    current_date = datetime.datetime.now(timezone).date()
    try:
        # 计算结束日期，即当前日期 + 7天
        end_date = current_date + datetime.timedelta(days=7)
        # 构建查询条件
        query_condition = Q(booking_date__range=(current_date, end_date),user_id=userid)
        # 查询预定数据 每次都会从数据库重新查询
        booking_list = models.Booking.objects.filter(query_condition).select_related('user', 'room').order_by(
            'booking_time').iterator()
        room_list = models.MeetingRoom.objects.all()
        booking_dict = {}
        for item in room_list:
            booking_dict[item.title] = {'1': [],
                                        '2': [],
                                        '3': []}
        #预约日期返回的是距离今天的天数 0 代表当天
        for booking in booking_list:
            bookinginfo = {'预约人': booking.username,
                           '开始时间': booking.booking_time,
                           '结束时间': booking.ending_time,
                           '用途': booking.useto,
                           '预约日期': get_days_diff(booking.booking_date)}
            booking_dict[booking.roomname][str(booking.mae_time)].append(bookinginfo)

        ret['data'] = booking_dict
    except Exception as e:
        ret['code'] = 1001
        ret['msg'] = str(e)
    return JsonResponse(ret)


def cancelbooking(request):
    json_data = json.loads(request.body.decode('utf-8'))
    current_date = datetime.datetime.now(timezone).date()
    booking_date = current_date + datetime.timedelta(json_data['booking_data'] - 1)
    roomname = json_data['roomname']
    booking_info= json_data['booking_info'].split('\n')
    time_choices = {
        '8:00': 1,
        '8:30': 2,
        '9:00': 3,
        '9:30': 4,
        '10:00': 5,
        '10:30': 6,
        '11:00': 7,
        '11:30': 8,
        '12:00': 9,
        '12:30': 10,
        '13:00': 11,
        '13:30': 12,
        '14:00': 13,
        '14:30': 14,
        '15:00': 15,
        '15:30': 16,
        '16:00': 17,
        '16:30': 18,
        '17:00': 19,
        '17:30': 20,
        '18:00': 21,
        '18:30': 22,
        '19:00': 23,
        '19:30': 24,
        '20:00': 25,
        '20:30': 26,
        '21:00': 27,
        '21:30': 28,
        '22:00': 29,
        '22:30': 30
    }
    time = booking_info[0].split('-')
    booking_time = time_choices[time[0]]
    ending_time = time_choices[time[1]]
    try:
        # 创建一个查询集，选择要删除的数据
        data_to_delete = Booking.objects.filter(booking_time=booking_time,ending_time=ending_time,booking_date=booking_date,roomname=roomname)  # 根据条件选择要删除的数据

        # 删除查询集中的所有数据对象
        data_to_delete.delete()
        return JsonResponse({'data': '删除成功'})

    except Exception as e:
        return JsonResponse({'error': e}, status=400)


def main(request):
    return render(request, 'main.html')

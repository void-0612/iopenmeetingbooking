from django.db import models
import datetime
import pytz

use_choices = ((1, '教学'),
               (2, '会议'),
               (3, '讲座'),
               (4, '答辩'))
mae_choices = ((1, '上午'),
               (2, '下午'),
               (3, '晚上'))

time_choices = (
    (1, '8:00'),
    (2, '8:30'),
    (3, '9:00'),
    (4, '9:30'),
    (5, '10:00'),
    (6, '10:30'),
    (7, '11:00'),
    (8, '11:30'),
    (9, '12:00'),
    (10, '12:30'),
    (11, '13:00'),
    (12, '13:30'),
    (13, '14:00'),
    (14, '14:30'),
    (15, '15:00'),
    (16, '15:30'),
    (17, '16:00'),
    (18, '16:30'),
    (19, '17:00'),
    (20, '17:30'),
    (21, '18:00'),
    (22, '18:30'),
    (23, '19:00'),
    (24, '19:30'),
    (25, '20:00'),
    (26, '20:30'),
    (27, '21:00'),
    (28, '21:30'),
    (29, '22:00'),
    (30, '22:30'),
)


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


class UserInfo(models.Model):
    name = models.CharField(verbose_name='用户姓名', max_length=32)
    id = models.CharField(verbose_name='学工号', max_length=32, primary_key=True)
    password = models.CharField(verbose_name='密码', max_length=32)


class MeetingRoom(models.Model):
    id = models.IntegerField(verbose_name='会议室id', max_length=32, primary_key=True)
    title = models.CharField(verbose_name='会议室', max_length=32)


class Booking(models.Model):
    user = models.ForeignKey(verbose_name='用户', to='UserInfo', on_delete=models.CASCADE)

    room = models.ForeignKey(verbose_name='会议室', to='MeetingRoom', on_delete=models.CASCADE)
    username = models.CharField(verbose_name='用户名称', max_length=32)
    roomname = models.CharField(verbose_name='会议室名称', max_length=32)

    useto = models.IntegerField(verbose_name='用途', choices=use_choices)

    booking_date = models.DateField(verbose_name='预定日期')
    booking_date_choices = get_7days_date()
    # morning afternoon evening choices

    booking_time = models.IntegerField(verbose_name='预定时间段', choices=time_choices)
    ending_time = models.IntegerField(verbose_name='结束时间段', choices=time_choices)
    mae_time = models.IntegerField(verbose_name='上下晚时间段', choices=mae_choices)
    class Meta:
        unique_together = (
            ('booking_date', 'booking_time', 'room')
        )

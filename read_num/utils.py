import datetime
from django.contrib.contenttypes.models import ContentType
from django.db.models import Sum
from django.utils import timezone
from .models import ReadNum,ReadDetail
# 阅读统计

def read_num_method(request,obj):
    ct = ContentType.objects.get_for_model(obj)
    key = ('%s_%s_read' % (ct.model,obj.pk))



    # 阅读计数对象
    if not request.COOKIES.get(key):
        # 每篇阅读数
        readnum, tuple = ReadNum.objects.get_or_create(content_type=ct, object_id=obj.pk,
                                                       defaults={'read_num': 0})
        readnum.read_num += 1
        readnum.save()
        # 有日期的阅读计数
        date=timezone.now().date()
        readDetail, tuple = ReadDetail.objects.get_or_create(content_type=ct, object_id=obj.pk,create_time=date,
                                                             defaults={'read_num':0} )
        readDetail.read_num += 1
        readDetail.save()

    return key

def get_seven_day_read_method(model):
    ct=ContentType.objects.get_for_model(model)
    today=timezone.now().date()
    week=[]
    read_nums=[]
    for i in range(6,-1,-1):
        date = today- datetime.timedelta(days=i)
        read_details = ReadDetail.objects.filter(content_type=ct,
                                                 create_time=date, )
        # 昨天
        week.append(date.strftime('%m/%d'))
        result=read_details.aggregate(read_num_sum=Sum('read_num'))
        read_nums.append(result['read_num_sum'] or 0)
    return week,read_nums


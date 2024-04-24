from datetime import timedelta

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F
from django.http import JsonResponse
from django.utils import timezone
from django.utils.translation import gettext as _
from django.views.decorators.csrf import csrf_exempt

import json
from .models import Icons
from .models import Queue, Services


def get_service_list(request):
    services = Services.objects.all().annotate(icon_icon=F('icon__icon'))
    data = {'services': list(services.values('id', 'name', 'icon_icon', 'code', 'created_at', 'updated_at'))}
    return JsonResponse(data)


def create_service(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        code = request.POST.get('code')

        try:
            # Bazada unikal bo'lgan xizmatni izlash
            service = Services.objects.get(code=code)
            # Agar topilsa, xizmatni o'zgartirish
            service.name = name
            service.save()
        except ObjectDoesNotExist:
            # Agar topilmasa, yangi xizmat yaratish
            service = Services.objects.create(name=name, code=code)

        # Auth group obyektini yaratish yoki topish
        try:
            group = Group.objects.create(name=name)
        except ObjectDoesNotExist:
            pass

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'Request method is not POST'})


@csrf_exempt
def receive_data(request):
    if request.method == 'POST':
        # JSON formatidagi ma'lumotlarni olish
        data = json.loads(request.body)

        # Ma'lumotlarni qabul qilish
        first_name = data.get('first_name', '')
        last_name = data.get('last_name', '')
        service_id = data.get('service_id', '')

        # Xizmatni bazadan olish
        try:
            service = Services.objects.get(pk=service_id)
        except Services.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Service not found'}, status=400)

        try:
            # Yangi Queue obyektini yaratish va saqlash
            new_queue_item = Queue.objects.create(
                first_name=first_name,
                last_name=last_name,
                services=service,
                done='waiting'
            )
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    else:
        return JsonResponse({'success': False, 'error': 'Only POST requests are allowed'}, status=405)


@csrf_exempt
def get_latest_queue(request, service_id):
    if request.method == 'GET':
        try:
            # Service_id ga tegishli eng so'nggi obyektni olish
            latest_queue_item = Queue.objects.filter(services_id=service_id).latest('order_number')
            data = {
                'first_name': latest_queue_item.first_name,
                'last_name': latest_queue_item.last_name,
                'order_number': latest_queue_item.order_number,
                'service_name': latest_queue_item.services.name,
                'done': latest_queue_item.get_done_display(),
            }
            return JsonResponse({'success': True, 'data': data})
        except Queue.DoesNotExist:
            return JsonResponse({'success': False, 'error': _('Ma\'lumot topilmadi')}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    else:
        return JsonResponse({'success': False, 'error': _('Faqat GET so\'rovlarni qo\'llab-quvvatlaymiz')}, status=405)


def get_waiting_queue(request):
    services_name = request.user.now_role

    # Bugungi sanani olamiz
    today = timezone.now()

    # Bugungi sanani avvalgi sanaga qarab hisoblash
    yesterday = today - timedelta(days=1)

    # "waiting" holatidagi barcha obyektlarni topish
    waiting_queue = Queue.objects.filter(done='waiting', services__name=services_name, created_at__gte=yesterday,
                                         created_at__lt=today)

    # JSON obyektini tayyorlash
    data = {
        'waiting_queue': [
            {
                'first_name': item.first_name,
                'last_name': item.last_name,
                'id': item.id,
                'created_at': item.created_at,
                'updated_at': item.updated_at,
                'services': item.services.name if item.services else '',
                'done': 'Kutilmoqda',
                'order_number': item.order_number,
                'user': item.user.username if item.user else ''
            }
            for item in waiting_queue
        ]
    }

    # JSON javobini qaytarish
    return JsonResponse(data)


def get_accepted_queue(request):
    services_name = request.user.now_role

    # Bugungi sanani olamiz
    today = timezone.now()

    # Bugungi sanani avvalgi sanaga qarab hisoblash
    yesterday = today - timedelta(days=1)

    # "waiting" holatidagi barcha obyektlarni topish
    waiting_queue = Queue.objects.filter(done='accept', services__name=services_name, created_at__gte=yesterday,
                                         created_at__lt=today)

    # JSON obyektini tayyorlash
    data = {
        'waiting_queue': [
            {
                'first_name': item.first_name,
                'last_name': item.last_name,
                'id': item.id,
                'created_at': item.created_at,
                'updated_at': item.updated_at,
                'services': item.services.name if item.services else '',
                'done': 'Qabul qilingan',
                'order_number': item.order_number,
                'user': item.user.first_name + item.user.second_name if item.user else ''
            }
            for item in waiting_queue
        ]
    }

    # JSON javobini qaytarish
    return JsonResponse(data)


def get_reject_queue(request):
    services_name = request.user.now_role

    # Bugungi sanani olamiz
    today = timezone.now()

    # Bugungi sanani avvalgi sanaga qarab hisoblash
    yesterday = today - timedelta(days=1)

    # "waiting" holatidagi barcha obyektlarni topish
    waiting_queue = Queue.objects.filter(done='reject', services__name=services_name, created_at__gte=yesterday,
                                         created_at__lt=today)

    # JSON obyektini tayyorlash
    data = {
        'waiting_queue': [
            {
                'first_name': item.first_name,
                'last_name': item.last_name,
                'id': item.id,
                'created_at': item.created_at,
                'updated_at': item.updated_at,
                'services': item.services.name if item.services else '',
                'done': 'Qaytarilgan',
                'order_number': item.order_number,
                'user': item.user.username if item.user else ''
            }
            for item in waiting_queue
        ]
    }

    # JSON javobini qaytarish
    return JsonResponse(data)


def get_delay_queue(request):
    services_name = request.user.now_role

    # Bugungi sanani olamiz
    today = timezone.now()

    # Bugungi sanani avvalgi sanaga qarab hisoblash
    yesterday = today - timedelta(days=1)

    # "waiting" holatidagi barcha obyektlarni topish
    waiting_queue = Queue.objects.filter(done='delay', services__name=services_name, created_at__gte=yesterday,
                                         created_at__lt=today)

    # JSON obyektini tayyorlash
    data = {
        'waiting_queue': [
            {
                'first_name': item.first_name,
                'last_name': item.last_name,
                'id': item.id,
                'created_at': item.created_at,
                'updated_at': item.updated_at,
                'services': item.services.name if item.services else '',
                'done': 'Kechiktirilgan',
                'order_number': item.order_number,
                'user': item.user.username if item.user else ''
            }
            for item in waiting_queue
        ]
    }

    # JSON javobini qaytarish
    return JsonResponse(data)


def save_icon(request):
    if request.method == 'POST':
        # HTML-dan ajax orqali olingan ikon nomi
        icon_name_server = request.POST.get('icon_name')
        icon_name = f'<i class="fa fa-{icon_name_server} fa-2x" aria-hidden="true"></i>'

        # Ikonlarni Icons modeliga saqlash
        icon, created = Icons.objects.get_or_create(name=icon_name_server, icon=icon_name)

        if created:
            return JsonResponse({'success': True, 'message': 'Icon saved successfully.'})
        else:
            return JsonResponse({'success': False, 'message': 'Icon already exists.'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method.'})


def get_icons(request):
    if request.method == 'GET':
        try:
            # Barcha iconlarni olish
            icons = Icons.objects.all()

            # Iconlarni JSON formatiga o'zgartirish
            icon_list = [{'id': icon.id, 'name': icon.name, 'icon': icon.icon, 'created_at': icon.created_at,
                          'updated_at': icon.updated_at} for icon in icons]

            # JSON javobini qaytarish
            return JsonResponse({'success': True, 'icons': icon_list})
        except Exception as e:
            return JsonResponse({'success': False, 'message': 'Iconlarni olishda xatolik yuz berdi: {}'.format(str(e))})
    else:
        return JsonResponse({'success': False, 'message': 'Istek usuli GET emas.'})


def save_service_with_icon(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            service_id = data.get('service_id')
            icon_id = data.get('icon_id')
            service = Services.objects.get(id=service_id)
            icon = Icons.objects.get(id=icon_id)
            service.icon = icon
            service.save()
            return JsonResponse({'success': True, 'message': 'Xizmat muvaffaqiyatli saqlandi.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    else:
        return JsonResponse({'success': False, 'message': 'Istek usuli POST emas.'})


def change_queue_status(request):
    if request.method == 'POST':
        user = request.user
        idcode = request.POST.get('id')
        name = request.POST.get('name')

        # Qabul, rad etish yoki kechiktirilgan holatiga mos ravishda done maydonini yangilash
        queue = Queue.objects.get(id=idcode)
        queue.done = name
        queue.user = user
        queue.save()

        return JsonResponse({'success': True, 'message': 'Holat muvaffaqiyatli o\'zgartirildi.'})

    return JsonResponse({'success': False, 'message': 'Noto\'g\'ri so\'rov usuli.'})


def get_user_count_by_status(status):
    """
    Foydalanuvchilarni belgilangan holat bo'yicha sanash funksiyasi
    """
    if status == 'accept':
        count = Queue.objects.filter(done='accept').count()
    elif status == 'reject':
        count = Queue.objects.filter(done='reject').count()
    elif status == 'delay':
        count = Queue.objects.filter(done='delay').count()
    elif status == 'waiting':
        count = Queue.objects.filter(done='waiting').count()
    else:
        count = 0  # Agar belgilangan holat yo'q bo'lsa, 0 qaytariladi
    return count


def get_service_count():
    """
    Xizmatlar sonini hisoblash funksiyasi
    """
    count = Services.objects.count()
    return count


def get_superuser_count():
    """
    Superuser foydalanuvchilarni hisoblash funksiyasi
    """
    User = get_user_model()
    count = User.objects.filter(is_superuser=True).count()
    return count


def get_non_superuser_users():
    """
    Superuser bo'lmagan foydalanuvchilarni JSON javobi sifatida qaytarish funksiyasi
    """
    User = get_user_model()
    non_superuser_users = User.objects.filter(is_superuser=False).values('id', 'username', 'email')
    return JsonResponse({'non_superuser_users': list(non_superuser_users)})


def statistics(request):
    """
    Asosiy statistikani JSON javobi sifatida qaytarish funksiyasi
    """
    accept_count = get_user_count_by_status('accept')
    reject_count = get_user_count_by_status('reject')
    delay_count = get_user_count_by_status('delay')
    waiting_count = get_user_count_by_status('waiting')
    queue_count = Queue.objects.count()
    service_count = get_service_count()
    superuser_count = get_superuser_count()

    statistics = {
        'accept_count': accept_count,
        'reject_count': reject_count,
        'delay_count': delay_count,
        'waiting_count': waiting_count,
        'queue_count': queue_count,
        'service_count': service_count,
        'superuser_count': superuser_count,
    }

    return JsonResponse(statistics)


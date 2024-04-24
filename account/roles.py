import json
from django.contrib.auth.models import Group
from django.http import JsonResponse


def create_group(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            group = Group.objects.create(name=name)
            return JsonResponse({'success': 'Group created successfully', 'id': group.id})
        else:
            return JsonResponse({'error': 'Name field is required'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST method is allowed'}, status=405)
def create_default_groups(request):
    # Grouplarni nomlari
    group_names = ['Administrator', 'Credit', 'Payment', 'Head', 'insurance']

    try:
        # Har bir group nomi uchun
        for group_name in group_names:
            # Agar bu nomda guruh mavjud bo'lmasa uni yaratamiz
            if not Group.objects.filter(name=group_name).exists():
                Group.objects.create(name=group_name)
        return JsonResponse({'message': 'Grouplar muvaffaqiyatli yaratildi'}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
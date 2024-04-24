# Serializer orqali ma'lumotlarni JSON ko'rinishida qaytarish
from django.contrib.auth import update_session_auth_hash, authenticate
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import Group
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from account.models import CustomUser
from account.serializers import CustomUserSerializer


def get_user_list(request):
    superadmins = CustomUser.objects.filter(is_superuser=True)
    normal_users = CustomUser.objects.filter(is_superuser=False)

    superadmin_serializer = CustomUserSerializer(superadmins, many=True)
    normal_user_serializer = CustomUserSerializer(normal_users, many=True)

    return JsonResponse({'superadmins': superadmin_serializer.data, 'normal_users': normal_user_serializer.data})


def create_employee(request):
    if request.method == 'POST':
        # Formdan ma'lumotlarni olish
        username = request.POST.get('val-username')
        email = request.POST.get('val-email')
        first_name = request.POST.get('val-first-name')
        last_name = request.POST.get('val-second-name')
        password = request.POST.get('val-password')

        # Yangi foydalanuvchi yaratish
        user = CustomUser.objects.create_user(username=username, email=email, first_name=first_name, is_staff=True,
                                              second_name=last_name,
                                              password=password)

        return JsonResponse({'success': True})  # Muvaffaqiyatli kirish

    return JsonResponse({'success': False})


def get_user_list_json(request, user_id):
    # Foydalanuvchini olish
    user = get_object_or_404(CustomUser, id=user_id)

    # Foydalanuvchining guruhlarini olish
    user_groups = list(user.groups.values_list('id', 'name'))

    # Barcha guruhlarni olish
    all_groups = list(Group.objects.values_list('id', 'name'))

    # Foydalanuvchi ma'lumotlarini JSON korinishida tayyorlash
    user_data = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'is_superuser': user.is_superuser,
        'full_name': user.full_name,
        'user_groups': user_groups,
        'all_groups': all_groups
    }

    # JsonResponse orqali ma'lumotlarni brauzerga jo'natish
    return JsonResponse({'user_data': user_data})


def update_user_groups(request):
    if request.method == 'POST':
        # Extract data from the POST request
        user_id = request.POST.get('user_id')
        mega_status = request.POST.get('mega-status')
        group_ids = request.POST.getlist('groups[]')  # 'groups[]' dan kelgan Group IDs

        # Retrieve the user object
        user = get_object_or_404(CustomUser, pk=user_id)

        # Remove the user from all groups first
        user.groups.clear()

        # Retrieve the groups based on the received group IDs
        selected_groups = Group.objects.filter(pk__in=group_ids)

        # Add the user to the selected groups
        user.groups.add(*selected_groups)

        # Update now_role field of the user with the name of the last saved group
        last_group_name = selected_groups.last().name
        user.now_role = last_group_name

        # Update superstatus based on mega-status
        if mega_status == 'true':
            user.is_superuser = True
        else:
            user.is_superuser = False

        # Save the changes
        user.save()

        # Return a JSON response to indicate success
        return JsonResponse({'success': True, 'message': "Muvaffaqiyatli yangilandi"})

    # If the request method is not POST, return an error response
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


def update_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        user_id = request.POST.get('user_id')

        # Foydalanuvchi obyektini olish
        user = get_object_or_404(CustomUser, pk=user_id)

        # Avvalgi parolni tekshirish
        if not authenticate(username=user.username, password=current_password):
            error_message = 'Avvalgi parol noto\'g\'ri. Iltimos, tekshirib qayta kiriting.'
            return JsonResponse({'success': False, 'message': error_message})

        # Parolni o'zgartirish
        form = PasswordChangeForm(user, data={'old_password': current_password, 'new_password1': new_password,
                                              'new_password2': confirm_password})
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Sessionni yangilash
            return JsonResponse({'success': True, 'message': 'Parol muvaffaqiyatli yangilandi.'})
        else:
            # Xatolik haqida xabar chiqarish
            error_message = 'Parolni yangilash muvaffaqiyatsiz tugadi. Iltimos, xatolarni to\'g\'rilang.'
            return JsonResponse({'success': False, 'message': error_message})

    # Agar so'rov POST emas bo'lsa, xato qaytariladi
    return JsonResponse({'success': False, 'message': 'Invalid request method'})


def user_groups_list(request):
    try:
        user = request.user
    except CustomUser.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'User not found'})

    user_groups = user.groups.all()
    group_list = [{'id': group.id, 'name': group.name} for group in user_groups]

    return JsonResponse({'success': True, 'user_groups': group_list})

def change_now_role(request):
    if request.method == 'POST':
        group_name = request.POST.get('name')  # JavaScript orqali yuborilgan guruh nomini olish
        user = request.user

        # Foydalanuvchi obyektini yangilash
        user.now_role = group_name
        user.save()

        return JsonResponse({'success': True, 'message': 'Foydalanuvchi roli muvaffaqiyatli o\'zgartirildi.'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404

from account.models import CustomUser


@login_required
def createEmployee(request):
    return render(request, 'admin/pages/create_employee.html')

@login_required
def userProfile(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    print(user)
    return render(request, 'admin/pages/user_profile.html', {'user': user})
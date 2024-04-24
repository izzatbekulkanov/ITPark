from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

from .models import Services


def index(request):
    return render(request, 'main/index.html')

@login_required
def adminPanel(request):
    return render(request, 'admin/main/index.html')

@login_required
def serviceView(request):
    return render(request, 'admin/pages/service.html')

@login_required
def acceptClientVIew(request):
    return render(request, 'admin/services/accept_client.html')

@login_required
def acceptedClientVIew(request):
    return render(request, 'admin/services/accepted_client.html')

@login_required
def rejectedClientVIew(request):
    return render(request, 'admin/services/rejected_client.html')

@login_required
def waitingClientVIew(request):
    return render(request, 'admin/services/waiting_client.html')

@login_required
def addRoleVIew(request):
    return render(request, 'admin/pages/add_role.html')

@login_required
def administratorListView(request):
    return render(request, 'admin/pages/administrator_list.html')

@login_required
def employeeListView(request):
    return render(request, 'admin/pages/employee_list.html')

@login_required
def roleListView(request):
    return render(request, 'admin/pages/role_list.html')

@login_required
def serviceView(request):
    return render(request, 'admin/pages/service.html')


@login_required
def iconListView(request):
    return render(request, 'admin/pages/icon_list.html')



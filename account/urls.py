from django.urls import path

from account.authentication import login_view, logout_view
from account.jsonView import get_user_list, create_employee, get_user_list_json, update_user_groups, update_password, \
    user_groups_list, change_now_role
from account.roles import create_default_groups, create_group
from account.views import createEmployee, userProfile

login_patterns = [
    path('login', login_view, name='login'),
    path('logout', logout_view, name='logout'),
]

groups_patterns = [
    path('create_default_groups', create_default_groups, name='create_default_groups'),
    path('create_group', create_group, name='create_group'),
    path('createEmployee', createEmployee, name='create_employee_views'),
    path('user-profile/<int:user_id>/', userProfile, name='user_profile'),
]

json_patterns = [
    path('json/get_user_list', get_user_list, name='get_user_list'),
    path('json/create_employee', create_employee, name='create_employee'),
    path('json/get_user_list_json/<int:user_id>', get_user_list_json, name='get_user_list_json'),
    path('json/update_user_groups', update_user_groups, name='update_user_groups'),
    path('json/update_password', update_password, name='update_user_groups'),
    path('json/user_groups_list', user_groups_list, name='user_groups_list'),
    path('json/change_now_role', change_now_role, name='change_now_role'),
]

urlpatterns = login_patterns + groups_patterns + json_patterns
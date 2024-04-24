from django.urls import path

from .serviceJson import create_service, get_service_list, receive_data, get_latest_queue, get_waiting_queue, save_icon, \
    get_icons, save_service_with_icon, get_accepted_queue, get_reject_queue, get_delay_queue, change_queue_status, \
    statistics
from .views import index, adminPanel, serviceView, acceptClientVIew, acceptedClientVIew, rejectedClientVIew, \
    administratorListView, addRoleVIew, employeeListView, roleListView, iconListView, waitingClientVIew

main_patterns = [
    path('', index, name='index'),
]
admin_patterns = [
    path('pages/admin_view', adminPanel, name='admin_view'),
    path('service/serviceView', serviceView, name='serviceView'),
    path('pages/acceptClientVIew', acceptClientVIew, name='acceptClientVIew'),
    path('pages/acceptedClientVIew', acceptedClientVIew, name='acceptedClientVIew'),
    path('pages/rejectedClientVIew', rejectedClientVIew, name='rejectedClientVIew'),
    path('pages/waitingClientVIew', waitingClientVIew, name='waitingClientVIew'),
    path('role/add_role', addRoleVIew, name='add_role'),
    path('user/administrator_list', administratorListView, name='administrator_list'),
    path('user/employee_list', employeeListView, name='employee_list'),
    path('role/role_list', roleListView, name='role_list'),
    path('pages/service', serviceView, name='service'),
    path('pages/iconListView', iconListView, name='icon_list'),
]
json_patterns = [
    path('json/create_service', create_service, name='create_service'),
    path('json/get_service_list', get_service_list, name='get_service_list'),
    path('json/receive_data', receive_data, name='receive_data'),
    path('json/latest_queue/<int:service_id>/', get_latest_queue, name='get_latest_queue'),
    path('json/get_waiting_queue', get_waiting_queue, name='get_waiting_queue'),
    path('json/get_accepted_queue', get_accepted_queue, name='get_waiting_queue'),
    path('json/get_reject_queue', get_reject_queue, name='get_waiting_queue'),
    path('json/get_delay_queue', get_delay_queue, name='get_waiting_queue'),
    path('json/save_icon', save_icon, name='save_icon'),
    path('json/get_icons', get_icons, name='get_icons'),
    path('json/save_service_with_icon', save_service_with_icon, name='save_service_with_icon'),
    path('json/change_queue_status', change_queue_status, name='change_queue_status'),
    path('json/statistics', statistics, name='statistics'),
]

urlpatterns = main_patterns + admin_patterns + json_patterns
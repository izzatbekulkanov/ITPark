from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')), # bosh sahifa
    path('user/', include('account.urls')), # bosh sahifa
]

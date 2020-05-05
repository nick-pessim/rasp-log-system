"""rasp_log_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from login.views import login, logging, logout
from home.views import menu
from add.views import add, add_device
from tcp_dump.views import dump, download_dump_file
from connection.views import add_device_gateway, add_connection, reset_connection


urlpatterns = [
    path('admin/', admin.site.urls),
    path('logging/', logging),
    path('logout/', logout),
    path('home/', menu),
    path('add/', add),
    path('add/device/', add_device),
    path('tcp-dump/', dump),
    path('tcp-dump/<str:dev_name>/', dump),
    path('tcp-dump/download/<str:dump_file>/', download_dump_file),
    path('connection/', add_device_gateway),
    path('connection/<str:dev_name>/', add_device_gateway),
    path('connection/<str:dev_name>/device/', add_connection),
    path('connection/<str:dev_name>/reset/', reset_connection),
    path('', login),
]

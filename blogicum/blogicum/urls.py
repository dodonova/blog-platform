"""blogicum URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.shortcuts import render

urlpatterns = [
    path('', include('blog.urls', namespace='blog')),
    path('category/', include('blog.urls', namespace='category_posts')),
    path('posts/', include('blog.urls', namespace='post_detail')),
    path('pages/', include('pages.urls', namespace='pages')),

    path('admin/', admin.site.urls)
]

# Если проект запущен в режиме разработки...
if settings.DEBUG:
    import debug_toolbar
# Добавить к списку urlpatterns список адресов из приложения debug_toolbar:
    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)

def handler404(request, *args, **argv):
    response = render(request, 'pages/404.html', status=404)
    return response


def handler500(request, *args, **argv):
    response = render(request, 'pages/500.html', status=500)
    return response
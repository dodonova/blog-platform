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
from django.urls import path, include, reverse_lazy
from django.conf import settings
from django.shortcuts import render

from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView

from django.conf.urls.static import static

urlpatterns = [
    path('', include('blog.urls', namespace='blog')),
    path('category/', include('blog.urls', namespace='category_posts')),
    path('posts/', include('blog.urls', namespace='post_detail')),
    path('pages/', include('pages.urls', namespace='pages')),
    path('auth/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path(
        'auth/registration/',
        CreateView.as_view(
            template_name='registration/registration_form.html',
            form_class=UserCreationForm,
            success_url=reverse_lazy('login'),
        ),
        name='registration'
    ),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'pages.views.page_not_found'
handler500 = 'pages.views.page_forbidden'

# def handler404(request, *args, **argv):
#     response = render(request, 'pages/404.html', status=404)
#     return response


# def handler500(request, *args, **argv):
#     response = render(request, 'pages/500.html', status=500)
#     return response

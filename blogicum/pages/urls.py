from django.urls import path

from .views import HomePage, Rules


app_name = 'pages'
urlpatterns = [
    path('about/', HomePage.as_view(), name='about'),
    path('rules/', Rules.as_view(), name='rules')
]

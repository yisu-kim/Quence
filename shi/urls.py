from django.urls import path

from . import views

app_name = 'shi'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('new/', views.new, name='new'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:input_id>/select/', views.select, name='select'),
    path('<int:input_id>/make/', views.make, name='make'),
    path('draft/', views.draft, name='draft'),
    path('<int:input_id>/publish/', views.publish, name='publish'),
]
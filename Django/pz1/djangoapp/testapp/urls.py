from django.urls import path
from . import views

app_name = 'testapp'

urlpatterns = [
    path('', views.home_view, name='home'),                          # главная страница
    path('news/<int:news_id>/', views.detail_view, name='detail'),   # страница новости
    path('news/add/', views.add_view, name='add'),                   # добавление новости
    path('news/success/', views.success_view, name='success'),
    path('news/<int:news_id>/delete/', views.delete_view, name='delete'),  # удаление
    path('search/', views.search_view, name='search'),               # поиск
]
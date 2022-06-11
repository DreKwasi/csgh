from django.urls import path
from csgh import views


urlpatterns = [
    path('', views.home, name='home'),
    path('delnote/', views.delnote, name='delnote'),
    path('salesquote/', views.salesquote, name='salesquote'),
    path('upload/<str:pk>', views.uploadfile, name='upload'),

]
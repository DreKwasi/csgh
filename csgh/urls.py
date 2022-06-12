from django.urls import path
from csgh import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.home, name='home'),
    path('delnote/', views.delnote, name='delnote'),
    path('salesquote/', views.SalesQuoteListView.as_view(), name='salesquote'),
    path('upload/<str:pk>', views.uploadfile, name='upload'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
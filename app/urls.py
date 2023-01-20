from . import views
from django.urls import path


urlpatterns = [
    path('', views.home , name= 'home'),
    path('login/', views.login , name= 'login'),
    path('dashboard/', views.dashboard , name= 'dashboard'),
    path('cancel_order/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('register/', views.register , name= 'register'),
    path('confirmed/', views.registration_confirmed , name= 'confirmed'),
]
from django.urls import path

from inventory import views

urlpatterns = [
    path('store/checkout/<int:pk>/', views.check_out, name="check-out"),
    path('store/checkin/<int:pk>/', views.check_in, name="check-in"),
]

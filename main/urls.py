from django.urls import path
from . import views

urlpatterns = [
    path('', views.home,name='home'),
    path('staff-list/', views.staff_list, name='staff_list'),
    path('staff-create/', views.staff_create, name='staff_create'),
    path('staff-delete/<int:id>/', views.staff_delete, name='staff_delete'),
    path('staff-update/<int:id>/', views.staff_update, name='staff_update' ),
    path('login/',views.log_in,name='login'),
    path('logout/',views.log_out,name='logout'),
    path('attendance/create/', views.attendance_create, name='attendance_create'),
    path('attendance/list/',views.attendance_list, name="attendance_list"),
    path('user/edit', views.edit_user, name='user_edit'),
]
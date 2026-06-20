from django.urls import path
from . import views

urlpatterns = [ 
    path('login/',views.login,name='login'),
    path('signup/',views.signup,name="signup"),
    path('status/',views.status,name='status'),
    path('teacher/',views.teacher,name='teacher'),
    path('profile/',views.profile,name='profile'),
    path('leave/',views.leave,name='leave'),
    path('',views.home,name='home'),
    path('logout/', views.logout_view, name='logout'),
    path('download_od/<str:leave_id>/', views.download_od, name='download_od'),
    path('download_medical/<str:leave_id>/', views.download_medical, name='download_medical'),
    path("status/delete/<str:leave_id>/", views.delete_leave, name="delete_leave"),
    path('calendar/', views.calendar_page, name='calendar_page'),
    
    path('teacher/analytics/', views.leave_analytics, name='leave_analytics'),
]
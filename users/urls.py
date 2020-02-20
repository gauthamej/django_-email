from django.urls import path

from users import views

urlpatterns = [
    path('api/v1/designers/login/', views.LoginView.as_view(), name='designers-login'),
    path('api/v1/designers/profile/', views.DesignerProfileView.as_view(), name='designers-profile'),
    path('login',views.login_user, name='login_user'),
    path('userlist', views.userlist, name='userlist'),
    path('register', views.register, name='register'),
    path('delete/<int:id>', views.delete, name='delete'),
     path('edit/<int:id>',views.edit, name='edit'),
     path('login',views.login_user, name='login_user'),
     path('logout_user',views.logout_user, name='logout_user'),
     path('login_form',views.login_form, name='login_form'),
]

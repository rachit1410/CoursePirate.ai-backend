from django.urls import path
from accounts import views

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('signin/', views.SignInView.as_view(), name='signin'),
    path('get-user/', views.GetUserView.as_view(), name='get-user'),
    path('refresh/', views.RefreshTokenView.as_view(), name='refresh-token'),
    path('signout/', views.SignOutView.as_view(), name='signout'),
]

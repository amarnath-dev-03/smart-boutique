from django.urls import path
from . import views

urlpatterns = [
    # Login
    path('', views.login_view, name='login'),

    # Logout
    path('logout/', views.logout_view, name='logout'),

    # Forgot Password
    path('forgot-password/', views.forgot_password, name='forgot_password'),

    # OTP Verification
    path('verify-otp/', views.verify_otp, name='verify_otp'),

    # Reset Password
    path('reset-password/', views.reset_password, name='reset_password'),
]

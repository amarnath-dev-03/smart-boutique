
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.hashers import make_password

import random
from datetime import datetime, timedelta
import os
import requests


# ==============================
# BREVO EMAIL
# ==============================

def send_brevo_email(to_email, otp):

    api_key = os.environ.get('BREVO_API_KEY')

    sender_email = os.environ.get(
        'SMART_BOUTIQUE_GMAIL',
        settings.DEFAULT_FROM_EMAIL
    )

    url = 'https://api.brevo.com/v3/smtp/email'

    headers = {
        'accept': 'application/json',
        'api-key': api_key,
        'content-type': 'application/json',
    }

    data = {
        'sender': {
            'name': 'Smart Boutique',
            'email': sender_email,
        },
        'to': [
            {
                'email': to_email,
            }
        ],
        'subject': 'Smart Boutique - Password Reset OTP',
        'textContent': (
            f'Your Smart Boutique password reset OTP is: {otp}\n\n'
            'This OTP is valid for 5 minutes.\n'
            'Do not share this OTP with anyone.'
        ),
        'htmlContent': f'''
            <div style="font-family: Arial, sans-serif; padding: 20px;">
                <h2 style="color:#5b3a29;">
                    Smart Boutique
                </h2>

                <p>Your password reset OTP is:</p>

                <div style="
                    font-size: 30px;
                    font-weight: bold;
                    letter-spacing: 6px;
                    color: #5b3a29;
                    margin: 20px 0;
                ">
                    {otp}
                </div>

                <p>
                    This OTP is valid for <strong>5 minutes</strong>.
                </p>

                <p>
                    Do not share this OTP with anyone.
                </p>

                <hr>

                <p style="color:#777;">
                    Smart Tailoring & Boutique
                </p>
            </div>
        ''',
    }

    response = requests.post(
        url,
        headers=headers,
        json=data,
        timeout=20,
    )

    response.raise_for_status()


# ==============================
# LOGOUT
# ==============================

def logout_view(request):
    logout(request)
    return redirect('login')


# ==============================
# LOGIN
# ==============================

def login_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('home')

        return render(request, 'userlogin/login.html', {
            'error': 'Invalid username or password.'
        })

    return render(request, 'userlogin/login.html')


# ==============================
# FORGOT PASSWORD
# ==============================

def forgot_password(request):

    if request.method == 'POST':

        username = request.POST.get('username')

        try:
            user = User.objects.get(username=username)

        except User.DoesNotExist:

            return render(request, 'userlogin/forgot_password.html', {
                'error': 'User not found.'
            })

        # Check registered email
        if not user.email:

            return render(request, 'userlogin/forgot_password.html', {
                'error': 'No email address is registered for this account.'
            })

        # Generate 6 digit OTP
        otp = str(random.randint(100000, 999999))

        # Store OTP in session
        request.session['reset_user_id'] = user.id
        request.session['reset_otp'] = otp
        request.session['otp_created_at'] = datetime.now().isoformat()

        # ==============================
        # SEND OTP
        # ==============================

        try:

            # If Brevo API key exists,
            # use Brevo API.
            if os.environ.get('BREVO_API_KEY'):

                send_brevo_email(
                    user.email,
                    otp
                )

            # Otherwise use existing Gmail SMTP.
            else:

                send_mail(
                    'Smart Boutique - Password Reset OTP',

                    f'Your Smart Boutique password reset OTP is: {otp}\n\n'
                    'This OTP is valid for 5 minutes.\n'
                    'Do not share this OTP with anyone.',

                    settings.DEFAULT_FROM_EMAIL,

                    [user.email],

                    fail_silently=False,
                )

        except Exception:

            return render(
                request,
                'userlogin/forgot_password.html',
                {
                    'error':
                    'Unable to send OTP email. Please try again later.'
                }
            )

        return redirect('verify_otp')

    return render(
        request,
        'userlogin/forgot_password.html'
    )


# ==============================
# VERIFY OTP
# ==============================

def verify_otp(request):

    if 'reset_user_id' not in request.session:
        return redirect('forgot_password')

    if request.method == 'POST':

        entered_otp = request.POST.get('otp')

        saved_otp = request.session.get('reset_otp')
        created_at = request.session.get('otp_created_at')

        # Check OTP expiry
        if created_at:

            created_time = datetime.fromisoformat(
                created_at
            )

            if datetime.now() - created_time > timedelta(minutes=5):

                request.session.flush()

                return render(
                    request,
                    'userlogin/verify_otp.html',
                    {
                        'error':
                        'OTP expired. Please request a new OTP.'
                    }
                )

        # Check OTP
        if entered_otp == saved_otp:

            request.session['otp_verified'] = True

            return redirect('reset_password')

        return render(
            request,
            'userlogin/verify_otp.html',
            {
                'error':
                'Invalid OTP. Please try again.'
            }
        )

    return render(
        request,
        'userlogin/verify_otp.html'
    )


# ==============================
# RESET PASSWORD
# ==============================

def reset_password(request):

    # OTP must be verified
    if not request.session.get('otp_verified'):
        return redirect('forgot_password')

    user_id = request.session.get('reset_user_id')

    try:

        user = User.objects.get(
            id=user_id
        )

    except User.DoesNotExist:

        request.session.flush()

        return redirect('forgot_password')

    if request.method == 'POST':

        password = request.POST.get('password')
        confirm_password = request.POST.get(
            'confirm_password'
        )

        # Password match
        if password != confirm_password:

            return render(
                request,
                'userlogin/reset_password.html',
                {
                    'error':
                    'Passwords do not match.'
                }
            )

        # Minimum password length
        if len(password) < 8:

            return render(
                request,
                'userlogin/reset_password.html',
                {
                    'error':
                    'Password must contain at least 8 characters.'
                }
            )

        # Change password
        user.password = make_password(
            password
        )

        user.save()

        # Clear reset session
        request.session.flush()

        return redirect('login')

    return render(
        request,
        'userlogin/reset_password.html'
    )


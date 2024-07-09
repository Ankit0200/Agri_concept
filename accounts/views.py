import time

from .serializers import DistrictSerializer, LocalSerializer
from django.shortcuts import render, redirect, HttpResponseRedirect, reverse
from rest_framework.throttling import AnonRateThrottle
from django.contrib import messages

from django.shortcuts import HttpResponse
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password, make_password

from .models import CustomUser, official_requests, District, Province, LocalBody
import random
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from news_publishing.models import notice_submission
from django.contrib.auth.decorators import login_required


# Create your views here.
def home_page(request):
    return render(request, 'Accounts/Signup_selection.html')


def farmer_signup(request):
    if request.method == 'POST':
        Name = request.POST['Name']
        Phone = request.POST['Contact']
        Province_selected = request.POST['Province']
        District = request.POST['District']
        local_body = request.POST['Local_body']
        email = request.POST['Email']
        password = request.POST['password']
        to_save_pass = make_password(password, salt=None, hasher='default')

        CustomUser.objects.create_user(Name=Name, Contact_no=Phone, Province=Province_selected, District=District,
                                       email=email,
                                       Local_government=local_body, password=to_save_pass)

        return HttpResponse("User created successfully")
    provinces = Province.objects.all()
    return render(request, 'Accounts/farmer_signup.html', {'provinces': provinces})


def officer_signup(request):
    if request.method == 'POST':
        Name = request.POST['Name']
        Phone = request.POST['Contact']
        Province_selected = request.POST['Province']
        District_selected = request.POST['District']
        local_body_selected = request.POST['Local_body']
        identity_proof = request.FILES['identity_proof']
        password = request.POST['password']
        email = request.POST['Email']

        to_save_pass = make_password(password, salt=None, hasher='default')

        my_province = Province.objects.filter(id=Province_selected).first()
        my_district = District.objects.filter(id=District_selected).first()
        my_local = LocalBody.objects.filter(id=local_body_selected).first()

        official_requests.objects.create(
            Name=Name, Contact_no=Phone, Province=my_province, District=my_district,
            Local_government=my_local, identity_proof=identity_proof, password=to_save_pass,
            email=email
        )
        return HttpResponse("Request sent successfully")

    provinces = Province.objects.all()
    return render(request, 'Accounts/officer_signup.html', {'provinces': provinces})


@login_required(login_url='login')
def check_requests(request):
    if request.user.is_superuser:
        official_request = official_requests.objects.filter(Q(status='waiting') | Q(status='rejected'))

        return render(request, 'Accounts/view_requests.html', {'official_requests': official_request})
    else:
        return HttpResponse("You are not authorized to view this page")


@login_required(login_url='login')
def qualify_requests(request, id):
    if request.user.is_superuser:
        official_request = official_requests.objects.get(id=id)
        official_request.status = 'accepted'
        official_request.save()

        Name = official_request.Name

        Phone = official_request.Contact_no
        Province = official_request.Province
        District = official_request.District
        local_body = official_request.Local_government
        identity_proof = official_request.identity_proof
        password = official_request.password
        email = official_request.email

        CustomUser.objects.create_user(Name=Name, Contact_no=Phone, Province=Province, District=District,
                                       Local_government=local_body, user_type='Official', identity_proof=identity_proof,
                                       email=email, password=password)
        return redirect('check-requests')
    else:
        return HttpResponse("You are not authorized for this action")


@login_required(login_url='login')
def reject_request(request, id):
    if request.user.is_superuser:
        official_request = official_requests.objects.get(id=id)
        official_request.status = 'rejected'
        official_request.save()
        return redirect('check-requests')
    else:
        return HttpResponse("You are not authorized for this action")


@login_required(login_url='login')
def approved_officials(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            try:
                suspend_reason = request.POST['suspend_reason']
                user_id = request.POST['char_id']
                request.session['char_id'] = user_id
                request.session['suspend_reason'] = suspend_reason
                return redirect('suspend')
            except:
                resticate_reason = request.POST['resticate_reason']
                request.session['resticate_reason'] = resticate_reason
                request.session['char_id'] = request.POST['char_id']
                return redirect('remove')

        approved = CustomUser.objects.filter(user_type='Official')
        return render(request, 'accounts/approved_officials.html', {'approved_officials': approved})
    else:
        return redirect('you are not authorized to view this page')


def suspend_officials(request):
    id = request.session['char_id']
    req_user = CustomUser.objects.get(id=id)
    req_user_contact = req_user.Contact_no
    suspend_reason = request.session['suspend_reason']

    email = EmailMessage(
        subject='YOU HAVE BEEN SUSPENDED FROM KRISHI JANKARI',
        body=f'Dear {req_user.Name},\n\n you have been suspended temporarily due to misconduct. The reasons of this action is mentioned below . Please read carefully and message us if there is any miscommunication between us.\n\n {suspend_reason}',
        from_email=f'{settings.EMAIL_HOST_USER}',
        to=[req_user.email]
    )
    email.send()
    req_user.delete()
    ##CHANGING THE STATUS INTO REJECTED IN REQUESTS

    request_to_modify = official_requests.objects.get(Contact_no=req_user_contact)
    request_to_modify.status = 'rejected'
    request_to_modify.save()

    return redirect('check-requests')


def remove_officials(request):
    id = request.session['char_id']
    req_user = CustomUser.objects.get(id=id)
    req_user_contact = req_user.Contact_no
    suspend_reason = request.session['resticate_reason']

    email = EmailMessage(
        subject='YOU HAVE BEEN Resticated FROM KRISHI JANKARI',
        body=f'Dear {req_user.Name},\n\n you have been resticated due to misconduct. The reasons of this action is mentioned below . Please read carefully and message us if there is any miscommunication between us.\n\n {suspend_reason}',
        from_email=f'{settings.EMAIL_HOST_USER}',
        to=[req_user.email]
    )
    email.send()
    req_user = CustomUser.objects.get(id=id)
    req_user_contact = req_user.Contact_no
    req_user.delete()

    # NOW DELETING THE REQUEST AS WELL
    request_to_delete = official_requests.objects.get(Contact_no=req_user_contact)
    request_to_delete.delete()
    return redirect('approved')


@login_required(login_url='login')
def after_official_login(request):
    if request.user.is_superuser:
        return redirect('admin_page')
    elif request.user.is_authenticated and request.user.user_type == 'Official':
        Recent_works = notice_submission.objects.filter(Uploader=request.user).order_by('-date_submitted')[:3]
        return render(request, 'accounts/home_page_after_official_login.html', {'recent_works': Recent_works})
    elif request.user.is_authenticated and request.user.user_type == 'Farmer':
        request.session['user_id'] = request.user.id
        return redirect('recent_news')


def login_view(request):
    if request.method == 'POST':
        contact = request.POST['contact']
        password = request.POST['password']
        user = authenticate(request, Contact_no=contact, password=password)
        if user is not None:
            login(request, user)
            return redirect('homepage_after_official_login')
        else:
            messages.error(request, "Invalid credentials")
            return redirect('login')
    return render(request, 'Accounts/login_page.html')


def forgot_password(request):
    if request.method == 'POST':
        try:
            variable = request.POST['email']
            recov_user = CustomUser.objects.filter(email=variable).first()
            if recov_user is not None:
                code = random.randint(100000, 999999)
                email_ready = EmailMessage(
                    f'Recovery Code from Krishi Jankari',
                    f'Hello {recov_user}\n\n Your OTP  for password reset is {code}.\n\n ',
                    f'{settings.EMAIL_HOST_USER}',
                    [variable],

                )
                email_ready.send()
                print(code)
                current_time = time.time()
                request.session['otp_code'] = code
                request.session['otp_time'] = current_time
                request.session['user'] = recov_user.id

                return redirect('otp_enter')

            else:
                messages.error(request, 'The user with that email does not exist.')
                return HttpResponseRedirect(reverse("forgot_password"))


        except Exception as e:
            print(e)
            variable = request.POST['contact']

    return render(request, 'Accounts/forgot_password.html')


# API VIEWS

from rest_framework.generics import ListAPIView


class DistrictsList(ListAPIView):
    throttle_class = [AnonRateThrottle]
    serializer_class = DistrictSerializer

    def get_queryset(self):
        My_id = self.kwargs['province_id']
        return District.objects.filter(province_id=My_id)


class LocalListView(ListAPIView):
    throttle_class = []
    serializer_class = LocalSerializer

    def get_queryset(self):
        return LocalBody.objects.filter(district_id=self.kwargs['district_id'])


def otp_enter(request):
    if request.method == 'POST':
        entered_code = request.POST['otp']
        code = request.session['otp_code']
        otp_time = request.session['otp_time']

        if code is None or otp_time is None:
            return HttpResponse("SESSION EXPIRED")

        if int(entered_code) == code:
            if (int((time.time()) - otp_time) < 120):
                request.session['otp_verified'] = True

                return redirect('reset_password_name')

            else:
                messages.error(request, "OTP Code expired. Create a new one.")
                return redirect('forgot_password')

        else:
            messages.error(request, "INVALID OTP")
            return redirect('otp_enter')

    return render(request, 'Accounts/enter_otp.html')


def reset_password(request):
    if not request.session.get('otp_verified'):
        return HttpResponse("YOU ARE NOT AUTHORIZED TO VIEW THIS URL. ")
    if request.method == 'POST':
        password_first = request.POST['password_first']
        password_last = request.POST['password_last']

        if password_first != password_last:
            messages.error(request, "Password do not match")
            return redirect('reset_password_name')
        elif len(password_first) < 8:
            messages.error(request, "Password must be at least 8 charecters long")
            return redirect('reset_password_name')
        elif password_first.isalpha():
            messages.error(request, "Password must contain at least one number ")
            return redirect('reset_password_name')

        else:
            user_id = request.session.get('user')
            user = CustomUser.objects.filter(id=user_id)
            user.update(password=make_password(password_first, salt=None, hasher='default'))

            return HttpResponse("Password updated Successfully ")
    return render(request, 'Accounts/reset_password.html')


def contact_view(request):
    if request.method == 'POST':
        issue = request.POST['issue']
        contact_detail = request.POST['contact_detail']
        email = EmailMessage(subject='You received an message',
                             body=f"Hello admin , \n\n  You have received the following message \n\n {issue} \n\n From:: {contact_detail} ",
                             from_email={settings.EMAIL_HOST_USER},
                             to=[settings.EMAIL_HOST_USER])
        email.send()
        return HttpResponse("Message sent succesfully")
    return render(request, 'Accounts/contacts.html')


def leaderboard_view(request):
    return HttpResponse(" Leaderboard is coming soon  !")


def logout_view(request):
    logout(request)
    return redirect("index")


def services_view(request):
    return render(request, 'Accounts/services.html')


def admin_page(request):
    return render(request, 'Accounts/admin_page.html')

from django.shortcuts import render,redirect
from .models import CustomUser, official_requests
from django.shortcuts import HttpResponse
from django.db.models import Q


# Create your views here.
def home_page(request):
    return render(request, 'Signup_selection.html')


def farmer_signup(request):
    if request.method == 'POST':
        Name = request.POST['Name']
        Phone = request.POST['Contact']
        Province = request.POST['Province']
        District = request.POST['District']
        local_body = request.POST['Local_body']
        CustomUser.objects.create_user(Name=Name, contact_no=Phone, Province=Province, District=District,
                                       Local_government=local_body)

    return render(request, 'farmer_signup.html')


def officer_signup(request):
    if request.method == 'POST':
        Name = request.POST['Name']
        Phone = request.POST['Contact']
        Province = request.POST['Province']
        District = request.POST['District']
        local_body = request.POST['Local_body']
        identity_proof = request.FILES['identity_proof']
        official_requests.objects.create(Name=Name, Contact_no=Phone, Province=Province, District=District,
                                         Local_government=local_body, identity_proof=identity_proof)

    return render(request, 'officer_signup.html')


def check_requests(request):
    official_request = official_requests.objects.filter(Q(status='waiting') | Q(status='rejected'))

    return render(request, 'view_requests.html', {'official_requests': official_request})


def qualify_requests(request, id):
    official_request = official_requests.objects.get(id=id)
    official_request.status = 'accepted'
    official_request.save()

    Name = official_request.Name

    Phone = official_request.Contact_no
    Province = official_request.Province
    District = official_request.District
    local_body = official_request.Local_government
    identity_proof = official_request.identity_proof

    CustomUser.objects.create_user(Name=Name, contact_no=Phone, Province=Province, District=District,
                                   Local_government=local_body, user_type='Official', identity_proof=identity_proof)

    return HttpResponse("You added them to the User database successfully")


def reject_request(request,id):
    official_request = official_requests.objects.get(id=id)
    official_request.status = 'rejected'
    official_request.save()
    return redirect('check-requests')


def approved_officials(request):
    approved = CustomUser.objects.filter(user_type='Official')
    return render(request, 'approved_officials.html', {'approved_officials': approved})

def suspend_officials(request, id):
    req_user=CustomUser.objects.get(id=id)
    req_user_contact = req_user.Contact_no


    req_user.delete()

    ##CHANGING THE STATUS INTO REJECTED IN REQUESTS

    request_to_modify=official_requests.objects.get(Contact_no=req_user_contact)
    request_to_modify.status = 'rejected'
    request_to_modify.save()

    return HttpResponse("SUSPENDED SUCCESSFULLY FROM THE OFFICIAL SECTION")

def remove_officials(request, id):
    req_user=CustomUser.objects.get(id=id)
    req_user_contact=req_user.Contact_no
    req_user.delete()

    # NOW DELETING THE REQUEST AS WELL

    request_to_delete=official_requests.objects.get(Contact_no=req_user_contact)
    request_to_delete.delete()
    return HttpResponse(" THE OFFICIAL WAS REMOVED PERMANENTLY WITHOUT")
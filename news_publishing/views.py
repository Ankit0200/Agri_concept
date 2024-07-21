from django.shortcuts import render, redirect, HttpResponse
from .models import notice_submission, scoreboard
from django.contrib.auth.decorators import login_required
from accounts.models import CustomUser
from .models import notice_submission
from django.db.models import Q
import os
from twilio.rest import Client


# Create your views here.
@login_required(login_url='login')
def home_page(request):
    if request.user.user_type == 'Official' or request.user.is_superuser:
        if request.method == 'POST':
            if 'notice' not in request.FILES:
                return HttpResponse("No file uploaded.")
            notice_file = request.FILES['notice']
            title = request.POST['title']

            new = notice_submission.objects.create(Uploader=request.user, notice=notice_file, notice_title=title)

            try:

                if request.user.scoreboard_track.Score > 20:
                    new.status = 'published'

                    request.user.scoreboard_track.Score += 1
                    request.user.scoreboard_track.save()
                    new.save()  # Save the changes to update status
            except Exception as e:
                print(e)
                print("SOMETHING WENT WRONG")
                pass  # Handle case where no scoreboard instance exists

                # Ensure the scoreboard instance exist
                print(f"Current User {request.user.Name}")
                scoreboard_instance, created = scoreboard.objects.get_or_create(User=request.user)
                print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
                if not created:
                    if scoreboard_instance.Score > 20:
                        new.status = 'published'
                        scoreboard_instance.Score += 1
                        scoreboard_instance.save()

                new.save()
            except Exception as e:
                print(f"SOMETHING WENT WRONG: {e}")

            return HttpResponse(
                "You have requested to post this news. Once the admin approves the notice will be posted")

        return render(request, 'publish_news/news_publish_form.html')
    else:
        return HttpResponse("You are not authorized to view this page.")


@login_required(login_url='login')
def published_news(request):
    published_news = notice_submission.objects.all()
    return render(request, 'publish_news/published_news.html', {'published_news': published_news})


@login_required(login_url='login')
def notice_approve(request, id):
    if request.user.is_superuser:
        notice_to_approve = notice_submission.objects.get(id=id)
        notice_to_approve.status = 'published'
        notice_to_approve.save()
        return redirect('news_list')


@login_required(login_url='login')
def personal_news(request, id):
    if request.user.user_type == 'Official':
        personal_news = notice_submission.objects.filter(Q(Uploader_id=id) & Q(status='published')).order_by(
            '-date_submitted')

        return render(request, 'publish_news/personal_news_list.html', context={
            'personal_news': personal_news
        })


def blogs_view(request):
    return HttpResponse("Blogs will be published soon . Please stay tuned ")


def gallery_view(request):
    return HttpResponse("Gallery will be published soon . Please stay tuned")


def recent_news_page(request):
    id = request.session['user_id']
    user = CustomUser.objects.filter(id=id).first()

    recent_news = notice_submission.objects.all().order_by('-date_submitted')
    to_be_submitted = []

    for char in recent_news:
        if char.Uploader.Local_government == user.Local_government:
            to_be_submitted.append(char)

    return render(request, 'publish_news/recent_news_in_area.html', {'recent_news': to_be_submitted})

    for char in recent_news:
        print(recent_news)

    return render(request, 'Accounts/recent_neews_in_area.html', {'recent_news': recent_news})


def send_in_contact(request, id):
    news = notice_submission.objects.filter(id=id).first()

    # Find your Account SID and Auth Token at twilio.com/console
    # and set the environment variables. See http://twil.io/secure


    account_sid = os.environ.get('ACCOUNT_SID')
    auth_token = os.environ.get('AUTH_TOKEN')
    client = Client(account_sid, auth_token)
    local_gov = news.Uploader.Local_government
    target_consumers = CustomUser.objects.filter(Local_government=local_gov)

    # for char in target_consumers:
    #     client = client.messages.create(
    #         to=f'+977 {char.Contact_no}',
    #         body=f'नमस्ते ,\n   "तपाईको  क्षेत्र     मा  निम्न   अनुदान बितरण    को  सूचना   आएको    छ ! \n\n {news.notice_title} थप    जानकारी     का  लागि यो   लिंक    खोली    हेर्नुहोला अथवा  हामीलाई     संपर्क  गर्नुहोस    | \n {news.notice.url} "  ',
    #         from_='+13613019732'
    #     )

    news.sent_in_phone = True
    news.save()
    return redirect('news_list')

from django.shortcuts import render, redirect, HttpResponse
from .models import notice_submission, scoreboard
from django.contrib.auth.decorators import login_required
from accounts.models import CustomUser
from . models import notice_submission


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

                    request.user.scoreboard_track.Score+=1
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

            return redirect('homepage_after_official_login')

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
        personal_news = notice_submission.objects.filter(Uploader_id=id)
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
    to_be_submitted=[]

    for char in recent_news:
        if char.Uploader.Local_government==user.Local_government:
            to_be_submitted.append(char)

    return render(request, 'publish_news/recent_news_in_area.html',{'recent_news':to_be_submitted})



    for char in recent_news:
        print(recent_news)

    return render(request, 'accounts/recent_neews_in_area.html', {'recent_news': recent_news})

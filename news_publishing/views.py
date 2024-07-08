from django.shortcuts import render, redirect, HttpResponse
from .models import notice_submission, scoreboard


# Create your views here.
def home_page(request):
    if request.user.user_type == 'Official' or request.user.is_superuser:
        if request.method == 'POST':
            if 'notice' not in request.FILES:
                return HttpResponse("No file uploaded.")
            notice_file = request.FILES['notice']
            title = request.POST['title']

            new = notice_submission.objects.create(Uploader=request.user, notice=notice_file, notice_title=title)

            try:
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

def published_news(request):
    published_news = notice_submission.objects.all()
    return render(request, 'publish_news/published_news.html', {'published_news': published_news})


def notice_approve(request, id):
    notice_to_approve = notice_submission.objects.get(id=id)
    notice_to_approve.status = 'published'
    notice_to_approve.save()
    return redirect('news_list')

def personal_news(request,id):
    personal_news = notice_submission.objects.filter(Uploader_id=id)
    return render(request, 'publish_news/personal_news_list.html',context={
        'personal_news':personal_news
    })

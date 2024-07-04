from django.shortcuts import render,redirect,HttpResponse
from .models import notice_submission,scoreboard

# Create your views here.
def home_page(request):
    if request.user.user_type=='Official' or request.user.is_superuser:
        if request.method=='POST':
            if 'notice' not in request.FILES:
                return HttpResponseBadRequest("No file uploaded.")
            notice_file=request.FILES['notice']
            new=notice_submission.objects.create(Uploader=request.user,notice=notice_file)

            try:
                if request.user.scoreboard_track.Score > 20:
                    new.status = 'published'
                   
                    request.user.scoreboard_track.Score+=1
                    request.user.scoreboard_track.save()
                    new.save()  # Save the changes to update status
            except:
                print("SOMETHING WENT WRONG")
                pass  # Handle case where no scoreboard instance exists

            new.save()
            return redirect('publish_home')

        return render(request, 'publish_news/homee.html')
    else:
        return HttpResponse("You are not authorized to view this page.")

def published_news(request):
    published_news=notice_submission.objects.all()
    return render(request, 'publish_news/published_news.html',{'published_news':published_news})


def notice_approve(request,id):
    notice_to_approve=notice_submission.objects.get(id=id)
    notice_to_approve.status = 'published'
    notice_to_approve.save()
    return redirect('news_list')

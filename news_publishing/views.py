from django.shortcuts import render,redirect
from .models import notice_submission

# Create your views here.
def home_page(request):
    if request.method=='POST':
        if 'notice' not in request.FILES:
            return HttpResponseBadRequest("No file uploaded.")
        notice_file=request.FILES['notice']
        new=notice_submission.objects.create(Uploader=request.user,notice=notice_file)
        new.save()
        return redirect('publish_home')



    return render(request, 'publish_news/homee.html')


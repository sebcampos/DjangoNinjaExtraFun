from django.shortcuts import render


# Create your views here.
def stream(request):
    return render(request, "video.html")
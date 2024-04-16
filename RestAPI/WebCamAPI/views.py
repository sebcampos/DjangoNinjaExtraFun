from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def stream(request):
    return render(request, "video.html")


@login_required
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect("login")
    return HttpResponse(status=404, content="User is not logged in")


@login_required
def tracking_view(request):
    return render(request, 'tracking.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect("stream")
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect("stream")
        return HttpResponse(status=403, content="Invalid username or password")
    return render(request, "login.html")

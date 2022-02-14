from django.shortcuts import render
from .models import * 
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404, Http404
from django.contrib.auth.models import User, auth
from .forms import UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required

def home(request):
    #movie_info = 'Jurassic Park'
    # movie_info = [
    #     {
    #         "name":"Jurassic Park",
    #         "year":"1993"
    #     },
    #     {
    #         "name":"Iron Mask",
    #         "year":"2019"
    #     },
    #     {
    #         "name":"Forrest Gump",
    #         "year":"1993"
    #     }
    # ]
    movie_info = Movie.objects.all()
    # movie_info = Movie.objects.filter(star__gt = 4, year__gt=2015)
    return render(request, 'home.html',{'movie':movie_info})

def showpage(request):
    return render(request, 'showpage.html', {})


def movie(request, movie_id):
    movie_info = Movie.objects.get(id=movie_id)
    return render(request, 'movie.html', {'movie':movie_info})

@login_required
def profile(request, *args, **kwargs):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_image_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if  user_form.is_valid() and profile_image_form.is_valid():
            user_form.save()
            profile_image_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('/')

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_image_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_image_form': profile_image_form,
    }

    return render(request, 'profile.html', context)


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['password2']

        if password == password1:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username Already Taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email Already Taken')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                messages.info(request, 'User Created')
                return redirect('login')
        else:
            messages.info(request, 'Password Not Matching')
            return redirect('register')

        return redirect('/')
    else:
        return render(request, 'register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('profile')
        else:
            messages.info(request, 'Invalid Credentials Username or Password is incorrect')
            return redirect('login')
    else:
        return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')
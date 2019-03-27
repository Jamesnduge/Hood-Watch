from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.contrib.auth import get_user_model
from django.template.context_processors import csrf

User = get_user_model()

def home(request):
    return render(request, 'index.html', locals())

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
        return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', locals())

def Login(request):
    c= {}
    c.update(csrf(request))
    return render(request, 'index.html', c)

def profile(request, username):
    profile = User.objects.get(username=username)
    try:
        profile_details = Profile.get_by_id(profile.id)
    except:
        profile_details = Profile.filter_by_id(profile.id)
    images = Image.get_profile_images(profile.id)
    title = f'@{profile.username} Hood-watch'

    return render(request, 'profile/profile.html', {'title':title, 'profile':profile, 'profile_details':profile_details})

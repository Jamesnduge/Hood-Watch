from django.shortcuts import render


def home(request):
    return render(request, 'registration/forms.html', locals())

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
        return redirect('home')
    else:
        form = SignupForm()
    return render(request, 'registration/forms.html', locals())
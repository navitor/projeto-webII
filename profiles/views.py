from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib.auth.models import User

@login_required
def profile_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        request.user.first_name = request.POST.get('first_name', request.user.first_name)
        request.user.email = request.POST.get('email', request.user.email)
        request.user.save()
        profile.telefone = request.POST.get('telefone', profile.telefone)
        profile.endereco = request.POST.get('endereco', profile.endereco)
        profile.save()
        return redirect('profiles:profile')
    return render(request, 'profiles/profile.html', {'profile': profile})

@login_required
def profile_edit(request):
    if request.method == 'POST':
        request.user.first_name = request.POST.get('first_name', request.user.first_name)
        request.user.last_name = request.POST.get('last_name', request.user.last_name)
        request.user.email = request.POST.get('email', request.user.email)
        request.user.save()
        return redirect('profiles:profile')
    return render(request, 'profiles/edit.html', {'user': request.user})
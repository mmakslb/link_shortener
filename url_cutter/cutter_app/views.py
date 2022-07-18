from django.shortcuts import render, redirect, HttpResponse
from django.http import Http404, HttpResponseRedirect
from .models import Shortener
from .forms import ShortenerForm, LoginForm, RegistrationForm
from django.contrib.auth import login, authenticate


def main_view(request):
    context = {'form': ShortenerForm()}
    if request.method == 'GET':
        return render(request, 'cutter_app/main.html', context)
    elif request.method == 'POST':
        used_form = ShortenerForm(request.POST)
        if used_form.is_valid():
            shortened_object = used_form.save()
            new_url = request.build_absolute_uri('/') + shortened_object.short_url
            long_url = shortened_object.long_url
            if request.user.is_anonymous:
                context['new_url'] = new_url
                context['long_url'] = long_url
            else:
                shortened_object.author = request.user
                context['new_url'] = new_url
                context['long_url'] = long_url
                shortened_object.save()

        context['errors'] = used_form.errors

        return render(request, 'cutter_app/shortener.html', context)


def redirect_url_view(request, shortened_part):
    try:
        shortener = Shortener.objects.get(short_url=shortened_part)
        shortener.times_followed += 1
        shortener.save()
        return HttpResponseRedirect(shortener.long_url)
    except:
        raise Http404('Sorry this link is broken :(')


def registration_view(request):
    form = RegistrationForm(request.POST or None)
    if form.is_valid():
        new_user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        email = form.cleaned_data['email']
        first_name = form.cleaned_data['first_name']
        new_user.username = username
        new_user.set_password(password)
        new_user.first_name = first_name
        new_user.email = email
        new_user.save()
        login_user = authenticate(username=username, password=password)
        if login_user:
            login(request, login_user)
            return redirect('main')
    context = {
        'form': form,
    }
    return render(request, 'cutter_app/registration.html', context)


def login_view(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        login_user = authenticate(username=username, password=password)
        if login_user:
            login(request, login_user)
            return redirect('main')
    context = {
        'form': form,
    }
    return render(request, 'cutter_app/login.html', context)


def links_view(request):
    context = {}
    if request.user.is_authenticated:
        queryset = Shortener.objects.filter(author=request.user)
        context = {
            'queryset': queryset
        }
    return render(request, 'cutter_app/links.html', context)

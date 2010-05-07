from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from sse_marquee.marquee.models import MarqueeEntry, MarqueeForm, LoginForm

def login_handler(request):
    resp_dict = {'user': request.user}
    if request.method == 'POST':
        print 'POST'
        form = LoginForm(request.POST)
        resp_dict['form'] = form
        user = None
        if form.is_valid():
            print 'valid'
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
        else:
            print 'invalid form'
            resp_dict['errors'] = ['invalid form data']
            return render_to_response('login.html', resp_dict)
        if user is not None:
            if user.is_active:
                print 'active user'
                login(request, user)
                return HttpResponseRedirect('/marquee/')
            else:
                print 'disabled'
                resp_dict['errors'] = ['your account has been disabled']
                return render_to_response('login.html', resp_dict)
        else:
            print 'invalid login attempt'
            resp_dict['errors'] = ['invalid login attempt']
            return render_to_response('login.html', resp_dict)
    else:
        print 'GET'
        resp_dict['form'] = LoginForm()
        return render_to_response('login.html', resp_dict)

def logout_handler(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required
def display(request):
    if request.method == 'POST':
        return display_post(request)
    else:
        return display_get(request)

def display_get(request, resp_dict=None):
    resp_dict = resp_dict or {'user': request.user}
    resp_dict['form'] = MarqueeForm()
    print resp_dict
    return render_to_response("uploadText.html", resp_dict)

def display_post(request):
    resp_dict = {'user': request.user}
    form = MarqueeForm(request.POST)
    form.user = request.user
    if form.is_valid():
        form.save()
        print request.POST['textTo']
        # do the marquee thing
    else:
        resp_dict['errors'] = form.errors
    return display_get(request, resp_dict)


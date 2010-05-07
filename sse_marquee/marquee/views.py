from django.shortcuts import render_to_response
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required

from sse_marquee.marquee.models import MarqueeEntry, MarqueeForm, LoginForm

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        user = None
        if form.is_valid():
            user = authenticate(username=form.username, password=form.password)
        else:
            return render_to_response('login.html', \
                   {'errors': ['your account has been disabled'], \
                    'form': form})
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/marquee/')
            else:
                return render_to_response('login.html', \
                       {'errors': ['your account has been disabled']})
        else:
            return render_to_response('login.html', \
                   {'errors': ['invalid login attempt']})
    else:
        return render_to_response('login.html')

def custom_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required
def display(request):
    resp_dict = {}
    if request.method == 'POST':
        return display_post(request)
    else:
        return display_get(request)

def display_get(request, resp_dict=None):
    resp_dict = resp_dict or {}
    resp_dict['form'] = MarqueeForm()
    return render_to_response("uploadText.html", resp_dict)

def display_post(request):
    resp_dict = {}
    form = MarqueeForm(request.POST)
    form.user = request.user
    if form.is_valid():
        form.save()
        print request.POST['textTo']
        # do the marquee thing
    else:
        resp_dict['errors'] = form.errors
    return display_get(request, resp_dict)


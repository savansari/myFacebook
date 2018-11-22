from django.shortcuts import render,redirect
from django.contrib import messages
from .models import User

# Create your views here.
def index(req):
    if 'user_id' not in req.session:
        return redirect('/users/new')
    current_user = User.objects.get(id = req.session['user_id'])
    context={
        'unmatched_users':User.objects.exclude(id=req.session['user_id']).exclude(requests_received__request_from=current_user).exclude(requests_sent__request_to=current_user),
        'requested_friends':User.objects.filter(requests_received__request_from=current_user),
        'requests_from':User.objects.filter(requests_sent__request_to=current_user),
        'mutual_friends':User.objects.filter(requests_received__request_from=current_user).filter(requests_sent__request_to=current_user)

        
    }
    return render(req,'users/index.html',context)
def new(req):
    return render(req,'users/new.html')
def create(req):
    errors=User.objects.validate(req.POST)
    if len(errors)>0:
        for error in errors:
            messages.error(req, error)
    else:
        craeted_user = User.objects.create_user_with_hash(req.POST)
        req.session['user_id']=craeted_user.id
    return redirect('/users/new')
def login(req):
    valid,result=User.objects.FindUser(req.POST)
    if valid==False:
        for error in result:
            messages.error(req, error)
    else:
        req.session['user_id']=result.id
        return redirect('/')
    return redirect('/users/new')

def logout(req):
    req.session.clear()
    return redirect('/users/new')

def create_request(req):
    User.objects.create_request(req.POST,req.session['user_id'])
    print("Done")
    return redirect('/users')
def remove_request(req):
    User.objects.delete_request(req.POST,req.session['user_id'])
    print("Done")
    return redirect('/users')
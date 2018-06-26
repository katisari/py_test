from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.core.urlresolvers import reverse
import re, bcrypt
from django.contrib.messages import get_messages
from .models import *

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

def index(request):
    return render(request, 'dashboard/login_reg.html')

def register(request):
    if len(request.POST['first_name']) < 1:
        messages.error(request, "First Name cannot be empty.")
    if len(request.POST['last_name']) < 1:
        messages.error(request, "Last Name cannot be empty.")
    if len(request.POST['email']) < 1:
        messages.error(request, "Email cannot be empty.")
    else:
        try:
            user_info = User.objects.get(email=request.POST['email'])
            messages.error(request, 'Email taken. Choose another email')
        except:
            print("Email not taken")
    if not EMAIL_REGEX.match(request.POST['email']):
        messages.error(request, "Invalid Email Address!")
    if len(request.POST['password']) < 8:
        messages.error(request, "Password must be at least 8 characters")
    if request.POST['password'] != request.POST['confirm_pw']:
        messages.error(request, "Passwords do not match")
    message_received = get_messages(request)
    if message_received:
        return redirect('/')
    else:
        hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        b=User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email =request.POST['email'], password=hashed_pw)
        messages.success(request, "User Created")
        request.session['user_id'] = b.id
        request.session['first_name'] = b.first_name
        return redirect(reverse('dashboard'))

def login(request):
    if len(request.POST['email']) < 1 or len(request.POST['password']) < 1:
        messages.error(request, "Please fill in all fields")
    try:
        user_info = User.objects.get(email=request.POST['email'])
    except:
        messages.error(request, 'Invalid login')
        return redirect('/')
    if bcrypt.checkpw(request.POST['password'].encode(), user_info.password.encode()):
        request.session['user_id'] = user_info.id
        request.session['first_name'] = user_info.first_name
        return redirect(reverse('dashboard'))
    messages.error(request, 'Invalid login')
    return redirect('/')

def dashboard(request):
    # a = Job.objects.get(id=3).liked_users.exclude(id=2).all()
    all_jobs = Job.objects.all()
    newarr = []
    for job in all_jobs:
        if not job.liked_users.filter(id =request.session['user_id']):
            newarr.append({'id': job.id, 'title': job.title, "user_id": job.user_id, "location": job.location})
    print (newarr)
    content = {
        "all_jobs": newarr,
        "my_jobs": User.objects.get(id=request.session['user_id']).liked_jobs.all()
    }
    return render(request, 'dashboard/dashboard.html', content)

def add_job(request):
    return render(request, 'dashboard/add_job.html')

def process_add(request):
    if len(request.POST['title']) <= 3:
        messages.error(request, "Title should be more than 3 characters")
    if len(request.POST['desc']) <= 10:
        messages.error(request, "Description should be more than 10 characters")
    if len(request.POST['location']) < 1:
        messages.error(request, "Location field should not be empty")
    message_received = get_messages(request)
    if message_received:
        return redirect(reverse('add_job'))
    else:
        a = User.objects.get(id=request.session['user_id'])
        Job.objects.create(title=request.POST['title'], desc=request.POST['desc'], location=request.POST['location'], user=a)
        return redirect(reverse('dashboard'))

def view_job(request, id):
    job_info = Job.objects.get(id=id)
    content = {
        "job_info": job_info
    }
    return render(request, 'dashboard/view.html', content)


def edit_job(request, id):
    job_info = Job.objects.get(id=id)
    content = {
        "job_info": job_info
    }
    return render(request, 'dashboard/edit.html', content)

def process_edit(request, id):
    # return HttpResponse("went through")
    if len(request.POST['title']) <= 3:
        messages.error(request, "Title should be more than 3 characters")
    if len(request.POST['desc']) <= 10:
        messages.error(request, "Description should be more than 10 characters")
    if len(request.POST['location']) < 1:
        messages.error(request, "Location field should not be empty")
    message_received = get_messages(request)
    if message_received:
        return redirect(reverse('edit_job'))
    else:
        a = Job.objects.get(id=id)
        a.title = request.POST['title']
        a.desc = request.POST['desc']
        a.location = request.POST['location']
        a.save()
        return redirect(reverse('dashboard'))

    # return HttpResponse("hello")

def cancel(request, id):
    b = Job.objects.get(id=id)
    b.delete()
    return redirect(reverse('dashboard'))


def add_myjobs(request, id):
    this_job = Job.objects.get(id=id)
    this_user = User.objects.get(id=request.session['user_id'])
    this_user.liked_jobs.add(this_job)

    return redirect(reverse('dashboard'))

def logoff(request):
    request.session.flush()
    return redirect('/')

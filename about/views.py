from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from tracking.models import Visitor
import json
from django.contrib.sessions.models import Session
from django.utils import timezone
# Create your views here.



# user login
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_superuser:
                login(request, user)
                messages.success(request, "You are successfully login !")
                return redirect('admin_dashboard')
            else:
                login(request, user)
                messages.success(request, "Successfully login.!")
                return redirect('vendor_dashboard')
        else:
            messages.error(request, "Sorry, You are not Register Yet.")
            return redirect('login')
    else:
        return render(request, 'about/authentication/login.html')

        

#admin dashboard
def admin_dashboard(request):
    labels = []
    user_request_data = []
    non_user_request_data = []
    for i in range(5):
        now = timezone.localtime() - timezone.timedelta(minutes=5 - i)
        labels.append(now.strftime('%H:%M:%S'))
        user_request_count_i = len(Session.objects.filter(
            expire_date__gte=now,
            expire_date__lt=now + timezone.timedelta(minutes=1),
            session_key__contains='_auth_user_id',
        ))
        user_request_data.append(user_request_count_i)
        non_user_request_count_i = len(Session.objects.filter(
                expire_date__gte=now,
                expire_date__lt=now + timezone.timedelta(minutes=1),
                session_key__icontains='guest',
            ))
        non_user_request_data.append(non_user_request_count_i)
        request_count_data = {
            'labels': labels,
            'datasets': [
                {
                    'label': 'User Requests',
                    'data': user_request_data,
                    'borderColor': 'rgb(255, 99, 132)',
                    'fill': False,
                },
                {
                    'label': 'Non-User Requests',
                    'data': non_user_request_data,
                    'borderColor': 'rgb(54, 162, 235)',
                    'fill': False,
                },
            ],
        }
        print(request_count_data)
    return render(request, 'about/admin/dashboard.html')



#vendor dashboard
def vendor_dashboard(request):
    return render(request, 'about/vendor/dashboard.html')


#vendor for admin page
def vendor(request):
    return render(request, 'about/admin/vendors.html')

def one(request):
    return render(request, 'about/one.html', context={'one_text': "ASD"})
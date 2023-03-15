from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

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
    return render(request, 'about/admin/dashboard.html')



#vendor dashboard
def vendor_dashboard(request):
    return render(request, 'about/vendor/dashboard.html')
import os
from django.conf import settings
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.sessions.models import Session
from django.utils import timezone
from . models import *
from django.db.models import Subquery, OuterRef, F
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash



# Create your views here.


# user login
def user_login(request, lg="en"):
    lg = request.GET.get('lg', '')  # Assuming 'lg' is obtained from the request

    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect(reverse("admin_dashboard"))
        else:
            return redirect(reverse("vendor_dashboard"))
    elif request.method == 'POST':
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
            if lg == 'np':
                # Logic specific to 'np' request
                context = {
                    'lg': lg,
                    # Add other context variables if needed
                }
                return render(request, 'about/authentication/login_nepali.html', context)
            else:
                # Logic for other cases
                context = {
                    'lg': lg,
                    # Add other context variables if needed
                }
                messages.error(request, "Sorry, You are not Register Yet.")
                return redirect('login')
    else:

        if lg == 'np':
            # Logic specific to 'np' request
            context = {
                'lg': lg,
                # Add other context variables if needed
            }
            return render(request, 'about/authentication/login_nepali.html', context)
        else:
            # Logic for other cases
            context = {
                'lg': lg,
                # Add other context variables if needed
            }
            return render(request, 'about/authentication/login.html', context)


# admin dashboard
def admin_dashboard(request):
    bottle_bin_count = DataR.objects.filter(category='Bottle').values('latitude', 'longitude').distinct().count()
    plastic_count = DataR.objects.filter(category='Plastic').values('latitude', 'longitude').distinct().count()
    bio_bin_count = DataR.objects.filter(category='Bio').values('latitude', 'longitude').distinct().count()
    feedback_count = Feedback.objects.all().count()
    toilet_count = Toilet.objects.all().count()
    context = {
        'bottle_bin_count': bottle_bin_count,
        'plastic_bin_count':  plastic_count,
        'bio_bin_count': bio_bin_count,
        'feedback_count': feedback_count,
        'toilet_count': toilet_count,
    }
    return render(request, 'about/admin/dashboard.html', context)


# vendor dashboard 

# for all bins
def vendor_bins(request):
    if request.user.is_authenticated:
        vendor = Vendor.objects.get(user=request.user)
        category_name = vendor.category

        bins = DataR.objects.filter(
            category=category_name
        ).annotate(
            latest_id=Subquery(
                DataR.objects.filter(
                    category=category_name,
                    latitude=OuterRef('latitude'),
                    longitude=OuterRef('longitude')
                ).order_by('-id').values('id')[:1]
            )
        ).filter(
            id=F('latest_id')
        ).values(
            'latitude',
            'longitude',
            'location',
            'distance',
            'volume',
            'created_date'
        ).order_by('-id')

        # modify the distance of every bin and calculate level in percentage
        for bin in bins:
            real_distance = 56 - (int(bin['distance'])-15) # calculate real_distance
            if real_distance < 15:
                real_distance = 15
            elif real_distance > 56:
                real_distance = 56
            else:
                real_distance= real_distance
            level = ((real_distance / 56) * 100) # calculate level in percentage
            bin['distance'] = int(level) # update distance key to level value

        context = {
            'bins': bins,
            'vendor': vendor
        }
        return render(request, 'about/vendor/dashboard.html', context)
    else:
        return redirect('login')


#for full bins
def vendor_dashboard(request):
    if request.user.is_authenticated:
        vendor = Vendor.objects.get(user=request.user)
        category_name = vendor.category

        bins = DataR.objects.filter(
                category=category_name
            ).annotate(
                latest_id=Subquery(
                    DataR.objects.filter(
                        category=category_name,
                        latitude=OuterRef('latitude'),
                        longitude=OuterRef('longitude')
                    ).order_by('-id').values('id')[:1]
                )
            ).filter(
                id=F('latest_id'),
            ).values(
                'latitude',
                'longitude',
                'location',
                'distance',
                'volume',
                'created_date'
            ).order_by('-id')


        # modify the distance of every bin and calculate level in percentage
        for bin in bins:
            real_distance = 56 - (int(bin['distance'])-15) # calculate real_distance
            
            real_distance = 56 - (int(bin['distance'])-15) # calculate real_distance
            if real_distance < 15:
                real_distance = 15
            elif real_distance > 56:
                real_distance = 56
            else:
                real_distance= real_distance
            level = ((real_distance / 56) * 100) # calculate level in percentage
            bin['distance'] = int(level) # update distance key to level value
        
        update_bins = bins.filter(distance__gt=50)
        context = {
            'bins': update_bins,
            'vendor': vendor
        }
        return render(request, 'about/vendor/dashboard.html', context)
    else:
        return redirect('login')



# About us page
def about_us(request):
    return render(request, 'about/admin/toiltes.html')

# vendor for admin page


def vendor(request):
    vendors = Vendor.objects.all()
    context = {
        'vendors': vendors
    }
    return render(request, 'about/admin/vendors.html', context)


def index(request):
    return render(request, map.html)


# delete
def delete(request, id):
    Vendor.objects.get(id=id).delete()
    return redirect('vendors')


def logout_view(request):
    logout(request)
    messages.success(request, "You are successfully logout. ")
    return redirect('login')


# bins
def bins_view(request, category_name):
    bins = DataR.objects.filter(
        category=category_name
    ).annotate(
        latest_id=Subquery(
            DataR.objects.filter(
                category=category_name,
                latitude=OuterRef('latitude'),
                longitude=OuterRef('longitude')
            ).order_by('-created_date').values('id')[:1]
        )
    ).filter(
        id=F('latest_id')
    ).values(
        'latitude',
        'longitude',
        'location',
        'distance',
        'volume',
        'created_date'
    ).order_by('-id')
    context = {
        'bins': bins
    }
    return render(request, 'about/admin/bins.html', context)


# register vendor
def add_vendor(request):
    if request.method == 'POST':
        profile_image = request.FILES.get('profile_image')
        license_image = request.FILES.get('license_image')
        if profile_image and license_image:
            # save the profile image to the static folder
            profile_dir = os.path.join(settings.STATICFILES_DIRS[0], 'images/profile')
            if not os.path.exists(profile_dir):
                os.makedirs(profile_dir)
            with open(os.path.join(profile_dir, profile_image.name), 'wb') as f:
                for chunk in profile_image.chunks():
                    f.write(chunk)
            # save the license image to the static folder
            license_dir = os.path.join(settings.STATICFILES_DIRS[0], 'images/license')
            if not os.path.exists(license_dir):
                os.makedirs(license_dir)
            with open(os.path.join(license_dir, license_image.name), 'wb') as f:
                for chunk in license_image.chunks():
                    f.write(chunk)
            name = request.POST.get('name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            dob = request.POST.get('dob')
            permanent_address = request.POST.get('permanent_address')
            current_address = request.POST.get('current_address')
            password = request.POST.get('password')
            vehicle_color = request.POST.get('vehicle_color')
            vehicle_brand = request.POST.get('vehicle_brand')
            vehicle_number = request.POST.get('vehicle_number')
            category = request.POST.get('category')
            user = User.objects.create_user(
                username=phone, email=email, password=password)
            vendor = Vendor(user=user, profile_image=f'static/images/profile/{profile_image.name}', category=category, name=name, email=email, phone=phone, dob=dob, permanent_address=permanent_address,
                            current_address=current_address, license_photo=f'static/images/license/{license_image.name}', status="Active", vehicle_brand=vehicle_brand, vehicle_color=vehicle_color,
                            vehicle_number=vehicle_number)
            vendor.save()
            messages.success(request, "Vendor Register Successfully.")
            return redirect('vendors')
        else:
            messages.error(request, "Please upload both images.")
            return redirect('add_vendor')

    return render(request, 'about/admin/add_vendor.html')


#edit vendor import os
import os
from django.conf import settings

def edit_vendor(request, id):
    vendor = Vendor.objects.get(id=id)
    if request.method == 'POST':
        # Update the vendor's profile and license images if provided
        profile_image = request.FILES.get('profile_image')
        license_image = request.FILES.get('license_image')
        if profile_image or license_image:
            # Delete the previous profile and license images (optional)
            # if vendor.profile_image:
            #     os.remove(os.path.join(settings.STATICFILES_DIRS[0], vendor.profile_image.path))
            # if vendor.license_photo:
            #     os.remove(os.path.join(settings.STATICFILES_DIRS[0], vendor.license_photo.path))
                
            # Save the new profile image to the static folder
            if profile_image:
                profile_dir = os.path.join(settings.STATICFILES_DIRS[0], 'images/profile')
                if not os.path.exists(profile_dir):
                    os.makedirs(profile_dir)
                with open(os.path.join(profile_dir, profile_image.name), 'wb') as f:
                    for chunk in profile_image.chunks():
                        f.write(chunk)
                vendor.profile_image = f'static/images/profile/{profile_image.name}'
                    
            # Save the new license image to the static folder
            if license_image:
                license_dir = os.path.join(settings.STATICFILES_DIRS[0], 'images/license')
                if not os.path.exists(license_dir):
                    os.makedirs(license_dir)
                with open(os.path.join(license_dir, license_image.name), 'wb') as f:
                    for chunk in license_image.chunks():
                        f.write(chunk)
                vendor.license_photo = f'static/images/license/{license_image.name}'
        
        # Update other vendor fields
        vendor.name = request.POST.get('name')
        vendor.email = request.POST.get('email')
        vendor.phone = request.POST.get('phone')
        vendor.dob = request.POST.get('dob')
        vendor.permanent_address = request.POST.get('permanent_address')
        vendor.current_address = request.POST.get('current_address')
        vendor.vehicle_color = request.POST.get('vehicle_color')
        vendor.vehicle_brand = request.POST.get('vehicle_brand')
        vendor.vehicle_number = request.POST.get('vehicle_number')
        vendor.category = request.POST.get('category')
        
        vendor.save()
        messages.success(request, "Vendor updated successfully.")
        return redirect('vendors')
    
    context = {
        'vendor': vendor
    }
    return render(request, 'about/admin/edit_vendor.html', context)






def view_map(request):
    if request.user.is_authenticated:
        vendor = Vendor.objects.get(user=request.user)
        context = {
            'vendor':vendor
        }
        return render(request, 'about/vendor/map.html', context)
    else:
        return redirect('login')



#user profile

def vendor_profile(request):
    if request.user.is_authenticated:
        usr  = User.objects.get(id = request.user.id)
        vendor = Vendor.objects.get(user = request.user)

        vendor = Vendor.objects.get(user = request.user)
        
        category = vendor.category  # Replace with your desired category

        # Filter DataEntry by category and retrieve the latest entry
        latest_entry = DataR.objects.filter(category=category).latest('created_date')
        current_distance = latest_entry.distance
       

        if int(current_distance) < 15:
            # Check if an unread notification already exists for the latest entry
            unread_notification = Notification.objects.filter(data_entry=latest_entry, read=False).first()

            if not unread_notification:
                # Create a new unread notification
                notification = Notification.objects.create(data_entry=latest_entry, message="Distance exceeds 90%, location:" + latest_entry.location)

            # Count the number of unread notifications
            unread_notification_count = Notification.objects.filter(data_entry=latest_entry, read=False).count()

            # Fetch the last 5 notifications for the user, ordered by the latest created date
            last_5_notifications = Notification.objects.filter(data_entry__category=category).order_by('-created_date')[:5]
        else:
            # If the distance is below 90%, mark all existing notifications as read
            Notification.objects.filter(data_entry=latest_entry).update(read=True)
            unread_notification_count = 0
            # Fetch the last 5 notifications for the user, ordered by the latest created date
            last_5_notifications = Notification.objects.filter(data_entry__category=category).order_by('-created_date')[:5]

        context = {
            'user': usr,
            'vendor': vendor,
            'show_notification': unread_notification_count > 0,
            'notification_count': unread_notification_count,
            'last_notifications': last_5_notifications,
        }
        return render(request, 'about/vendor/profile.html', context)
    else:
        return redirect('login')
    


def vendor_detail(request, id):
    if request.user.is_superuser:
        usr  = User.objects.get(id = request.user.id)
        vendor = Vendor.objects.get(id=id)
    
        context = {
            'user': usr,
            'vendor': vendor,
            
        }
        return render(request, 'about/vendor/profile.html', context)
    else:
        return redirect('login')
    

#notification read

def mark_notification_as_read(request, notification_id):
    notification = Notification.objects.get(id=notification_id)
    notification.read = True
    notification.save()
    return redirect(request.META['HTTP_REFERER'])




#notification
def notification(request):
    if request.user.is_authenticated:
        usr  = User.objects.get(id = request.user.id)
        vendor = Vendor.objects.get(user = request.user)

        vendor = Vendor.objects.get(user = request.user)
        
        category = vendor.category  # Replace with your desired category

        # Filter DataEntry by category and retrieve the latest entry
        latest_entry = DataR.objects.filter(category=category).latest('created_date')
        current_distance = latest_entry.distance
       

        if int(current_distance) < 15:
            # Check if an unread notification already exists for the latest entry
            unread_notification = Notification.objects.filter(data_entry=latest_entry, read=False).first()

            if not unread_notification:
                # Create a new unread notification
                notification = Notification.objects.create(data_entry=latest_entry, message="Distance exceeds 90%, location:" + latest_entry.location)

            # Count the number of unread notifications
            unread_notification_count = Notification.objects.filter(data_entry=latest_entry, read=False).count()

            # Fetch the last 5 notifications for the user, ordered by the latest created date
            last_5_notifications = Notification.objects.filter(data_entry__category=category).order_by('-created_date')[:5]
        else:
            # If the distance is below 90%, mark all existing notifications as read
            Notification.objects.filter(data_entry=latest_entry).update(read=True)
            unread_notification_count = 0
            # Fetch the last 5 notifications for the user, ordered by the latest created date
            last_5_notifications = Notification.objects.filter(data_entry__category=category).order_by('-created_date')[:5]

        context = {
            'user': usr,
            'vendor': vendor,
            'show_notification': unread_notification_count > 0,
            'notification_count': unread_notification_count,
            'last_notifications': last_5_notifications,
        }
        return render(context)
    else:
        return redirect('login')
    


#password change
@login_required
def change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')

        #validation
        if not request.user.check_password(old_password):
            messages.error(request, 'Incorrect old Password')
        elif new_password1 != new_password2:
            messages.error(request, 'New password do not match.')

        else:
            request.user.set_password(new_password1)
            request.user.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, 'Your password has been changed successfully.')
            return redirect('change_success')
    return render(request, 'about/authentication/change_password.html')



#change success
def change_success(request):
    return render(request, 'about/authentication/change_success.html')



#for user home
def home(request, lg='en'):
    lg = request.GET.get('lg', '')  # Assuming 'lg' is obtained from the request

    if lg == 'np':
        # Logic specific to 'np' request
        context = {
            'lg': lg,
            # Add other context variables if needed
        }
        return render(request, 'about/user/nepali.html', context)
    else:
        # Logic for other cases
        context = {
            'lg': lg,
            # Add other context variables if needed
        }
        return render(request, 'about/user/index.html', context)


def user_about(request, lg='en'):
    lg = request.GET.get('lg', '')  # Assuming 'lg' is obtained from the request

    if lg == 'np':
        # Logic specific to 'np' request
        context = {
            'lg': lg,
            # Add other context variables if needed
        }
        return render(request, 'about/user/about_nepali.html', context)
    else:
        # Logic for other cases
        context = {
            'lg': lg,
            # Add other context variables if needed
        }
        return render(request, 'about/user/about.html', context)
    

def service(request, lg='en'):
    lg = request.GET.get('lg', '')  # Assuming 'lg' is obtained from the request

    if lg == 'np':
        # Logic specific to 'np' request
        context = {
            'lg': lg,
            # Add other context variables if needed
        }
        return render(request, 'about/user/service_nepali.html', context)
    else:
        # Logic for other cases
        context = {
            'lg': lg,
            # Add other context variables if needed
        }
        return render(request, 'about/user/service.html', context)
    


def dustbins(request, lg='en'):
    lg = request.GET.get('lg', '')  # Assuming 'lg' is obtained from the request

    if lg == 'np':
        dustbins = DataR.objects.values('latitude', 'longitude', 'location').distinct()
        # Logic specific to 'np' request
        context = {
            'lg': lg,
            'data': dustbins
            # Add other context variables if needed
        }
        return render(request, 'about/user/dustbin_nepali.html', context)
    else:
        dustbins = DataR.objects.values('latitude', 'longitude', 'location').distinct()

        # Logic for other cases
        context = {
            'lg': lg,
            'data': dustbins
            # Add other context variables if needed
        }
        return render(request, 'about/user/dustbin.html', context)



def toilets(request, lg='en'):
    lg = request.GET.get('lg', '')  # Assuming 'lg' is obtained from the request

    if lg == 'np':
        toilets = Toilet.objects.all()
        # Logic specific to 'np' request
        context = {
            'lg': lg,
            'data': toilets
            # Add other context variables if needed
        }
        return render(request, 'about/user/toilet_nepali.html', context)
    else:
        # Logic for other cases
        toilets = Toilet.objects.all()
        context = {
            'lg': lg,
            'data': toilets
            # Add other context variables if needed
        }
        return render(request, 'about/user/toilet.html', context)
    

def contact(request, lg='en'):
    lg = request.GET.get('lg', '')  # Assuming 'lg' is obtained from the request
    

    if lg == 'np':
        if request.method == 'POST':
            name = request.POST.get('name')
            email = request.POST.get('email')
            address = request.POST.get('address')
            message = request.POST.get('message')
            feedback = Feedback(name=name, email=email, address=address, message=message)
            feedback.save()
            messages.success(request, "हामीलाई सम्पर्क गर्नु भएकोमा धन्यवाद")
        # Logic specific to 'np' request
        context = {
            'lg': lg,
            # Add other context variables if needed
        }
        return render(request, 'about/user/contact_nepali.html', context)
    else:
        if request.method == 'POST':
            name = request.POST.get('name')
            email = request.POST.get('email')
            address = request.POST.get('address')
            message = request.POST.get('message')
            feedback = Feedback(name=name, email=email, address=address, message=message)
            feedback.save()
            messages.success(request, "Thank you for Contacting Us.")
        # Logic for other cases
        context = {
            'lg': lg,
            # Add other context variables if needed
        }
        return render(request, 'about/user/contact.html', context)
    


def admin_feedback(request):
    feedbacks = Feedback.objects.all()
    context = {
        'feedbacks': feedbacks
    }
    return render(request, 'about/admin/feedback.html', context)



def view_dustbin(request, latitude):
    context = {
        'chart_id': latitude
    }
    return render(request, 'about/admin/chart.html', context)
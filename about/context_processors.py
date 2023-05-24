from . models import *

def notifications(request):
    if request.user.is_superuser:
        usr = User.objects.get(id=request.user.id)

        latest_entry = DataR.objects.filter().latest('created_date')
        current_distance = latest_entry.distance

        if int(current_distance) < 15:
            # Check if a notification already exists for the latest entry with the same location
            existing_notification = Notification.objects.filter(data_entry=latest_entry, data_entry__location=latest_entry.location).first()

            if not existing_notification:
                # Create a new unread notification
                notification = Notification.objects.create(data_entry=latest_entry, message="Distance exceeds 90%, location: " + latest_entry.location)

        # Count the number of unread notifications
        unread_notification_count = Notification.objects.filter(data_entry=latest_entry, read=False).count()

        # Fetch the last 5 notifications for the user, ordered by the latest created date
        last_5_notifications = Notification.objects.filter(data_entry__location=latest_entry.location).order_by('-created_date')[:5]

        context = {
            'user': usr,
            'show_notification': unread_notification_count > 0,
            'notification_count': unread_notification_count,
            'last_notifications': last_5_notifications,
        }
        return context

    elif request.user.is_authenticated:
        usr = User.objects.get(id=request.user.id)
        vendor = Vendor.objects.get(user=request.user)
        category = vendor.category

        latest_entry = DataR.objects.filter(category=category).latest('created_date')
        current_distance = latest_entry.distance

        if int(current_distance) < 15:
            # Check if a notification already exists for the latest entry with the same location
            existing_notification = Notification.objects.filter(data_entry=latest_entry, data_entry__location=latest_entry.location).first()

            if not existing_notification:
                # Create a new unread notification
                notification = Notification.objects.create(data_entry=latest_entry, message="Distance exceeds 90%, location: " + latest_entry.location)

        # Count the number of unread notifications
        unread_notification_count = Notification.objects.filter(data_entry=latest_entry, read=False).count()

        # Fetch the last 5 notifications for the user, ordered by the latest created date
        last_5_notifications = Notification.objects.filter(data_entry__category=category).order_by('-created_date')[:5]

        context = {
            'user': usr,
            'vendor': vendor,
            'show_notification': unread_notification_count > 0,
            'notification_count': unread_notification_count,
            'last_notifications': last_5_notifications,
        }
        return context
    else:
        return {}
    

from django.contrib import admin
from . models import Dustbin, Category, Vendor, Notification, Feedback

# Register your models here.
class LocationAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(region=request.user.region)

admin.site.register(Dustbin, LocationAdmin)
admin.site.register(Category)
admin.site.register(Vendor)
admin.site.register(Notification)
admin.site.register(Feedback)
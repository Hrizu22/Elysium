from django.contrib import admin
from elysium_app.models import Stock,PlatformInfo,Review
# Register your models here.
admin.site.register(Stock)
admin.site.register(PlatformInfo)
admin.site.register(Review)

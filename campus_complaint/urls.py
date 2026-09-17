from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tracker.urls')),
]

# এখানে 'if settings.DEBUG:' চেকটি সরিয়ে দেওয়া হয়েছে, যেন রেন্ডারে লাইভ প্রজেক্টেও ছবিগুলো দেখা যায়
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
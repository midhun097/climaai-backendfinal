# climavision_backend/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.http import JsonResponse  # ✅ import this

# ✅ Add a simple root view
def home(request):
    return JsonResponse({"message": "Welcome to ClimaAI Backend API"})

urlpatterns = [
    path('', home),  # 👈 Add this line to handle '/'
    path('admin/', admin.site.urls),
    path('api/accounts/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/accounts/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/accounts/', include('accounts.urls')),
    path('api/contact/', include('contact.urls')),
    path('api/recognize/', include('climate.urls')),  # ✅ keep only one
 ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# ✅ Uncommented imports
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'

urlpatterns = [
    # path for user login API
    path('login', views.login_user, name='login'),
    path("logout/", views.logout_request, name="logout"),
    path("register/", views.registration, name="register"),
    # 👉 You can later add more routes here:
    # path('register/', views.registration, name='registration'),
    # path('dealer/<int:dealer_id>/reviews/', views.get_dealer_reviews, name='dealer_reviews'),
    # path('add_review/', views.add_review, name='add_review'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
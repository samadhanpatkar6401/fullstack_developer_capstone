from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'

urlpatterns = [
    # path for user login API
    path("get_cars", views.get_cars, name="getcars"),
    path('login/', views.login_user, name='login'),
    path("logout/", views.logout_request, name="logout"),
    path("register/", views.registration, name="register"),

    # paths for dealers
    path('get_dealers/', views.get_dealerships, name='get_dealers'),
    path(
        'get_dealers/<str:state>/',
        views.get_dealerships,
        name='get_dealers_by_state'
    ),
    path(
        route='dealer/<int:dealer_id>/',
        view=views.get_dealer_details,
        name='dealer_details'
    ),

    # paths for reviews
    path(
        route='reviews/dealer/<int:dealer_id>/',
        view=views.get_dealer_reviews,
        name='dealer_reviews'  # Corrected name for clarity
    ),
    path(
        route='add_review',
        view=views.add_review,
        name='add_review'
    ),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

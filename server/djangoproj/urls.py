from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),

    # Backend APIs
    path("djangoapp/", include("djangoapp.urls")),

    # Frontend / React routes
    path("", TemplateView.as_view(template_name="Home.html")),
    path("about/", TemplateView.as_view(template_name="About.html")),
    path("contact/", TemplateView.as_view(template_name="Contact.html")),
    path("login/", TemplateView.as_view(template_name="index.html")),
    path("register/", TemplateView.as_view(template_name="index.html")),
    path("dealers/", TemplateView.as_view(template_name="index.html")),
    path(
        "dealer/<int:dealer_id>/",
        TemplateView.as_view(template_name="index.html"),
    ),
    path(
        "postreview/<int:dealer_id>/",
        TemplateView.as_view(template_name="index.html"),
    ),
]

# Serve static & media files during development
if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT,
    )
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )

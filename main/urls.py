from django.urls import path
from django.views.generic import RedirectView

from . import views


app_name = "main"

urlpatterns = [
    path("", views.IndexView.as_view(), name="home"),
    path("contact/", views.ContactView.as_view(), name="contact"),
    path("services/", views.ServicesView.as_view(), name="services"),
    path(
        "services/<slug:slug>/",
        views.ServiceDetailView.as_view(),
        name="service",
    ),
    path("portfolio/", views.PortfolioView.as_view(), name="portfolios"),
    path(
        "portfolio/<slug:slug>/",
        views.PortfolioDetailView.as_view(),
        name="portfolio",
    ),
    path("blog/", views.BlogView.as_view(), name="blogs"),
    path("blog/<slug:slug>/", views.BlogDetailView.as_view(), name="blog"),
    path(
        "projects/",
        RedirectView.as_view(pattern_name="main:portfolios", permanent=True),
        name="projects",
    ),
]

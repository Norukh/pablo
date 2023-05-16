from django.urls import path

from . import views
from .views import ContentImageView, ArtistView, PaintingView

urlpatterns = [
    path("", views.index),
    path("artists", ArtistView.as_view(), name="artists"),
    path("paintings/<int:artist_id>", PaintingView.as_view()),
    path("transfer", ContentImageView.as_view(), name="transfer"),
]

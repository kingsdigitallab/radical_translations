from django.urls import path

from radical_translations.core.views import ResourceDetailView, ResourceListView

urlpatterns = [
    path("<int:pk>/", ResourceDetailView.as_view(), name="resource-detail"),
    path("", ResourceListView.as_view(), name="resource-list"),
]

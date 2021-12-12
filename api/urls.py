from django.urls import path
from .views import (
    FormDetailAPIView,
    SubmissionListAPIView,
    SubscriberListAPIView,
    CreateSubmissionAPIView,
    UserListAPIView,
    UserDetailAPIView,
    UserUpdateAPIView,
    WorkspaceListAPIView,
    WorkspaceDetailAPIView,
    FormListAPIView,
)

urlpatterns = [
    path("subscribers/", SubscriberListAPIView.as_view(), name="form"),
    path("forms/", FormListAPIView.as_view(), name="form"),
    path("forms/<int:pk>/", FormDetailAPIView.as_view(), name="form"),
    path("f/<uuid:uuid>/", CreateSubmissionAPIView.as_view(), name="create-submission"),
    path("submissions/", SubmissionListAPIView.as_view(), name="submission"),
    path("users/", UserListAPIView.as_view(), name="user"),
    path("users/<int:pk>/", UserDetailAPIView.as_view(), name="user-retrieve"),
    path("users/update/<int:pk>/", UserUpdateAPIView.as_view(), name="user-update"),
    path("workspace/", WorkspaceListAPIView.as_view(), name="workspace"),
    path(
        "workspace/<int:pk>/",
        WorkspaceDetailAPIView.as_view(),
        name="workspace-retrieve",
    ),
]

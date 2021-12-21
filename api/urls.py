from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    FormDetailAPIView,
    FormWorkspaceAPIView,
    LoginAPIView,
    PasswordChangeAPIView,
    RegisterAPIView,
    SubmissionListAPIView,
    SubscriberListAPIView,
    SubmissionFormAPIView,
    UserListAPIView,
    UserDetailAPIView,
    UserUpdateAPIView,
    WorkspaceListAPIView,
    WorkspaceDetailAPIView,
    WorkspaceUserListAPIView,
    FormListAPIView,
)


urlpatterns = [
    path("subscribers/", SubscriberListAPIView.as_view(), name="form"),
    path("forms/", FormListAPIView.as_view(), name="form"),
    path("forms/<int:pk>/", FormWorkspaceAPIView.as_view(), name="form-workspace"),
    path("forms/detail/<uuid:uuid>/", FormDetailAPIView.as_view(), name="form-detail"),
    path("f/<uuid:uuid>/", SubmissionFormAPIView.as_view(), name="create-submission"),
    path("submissions/", SubmissionListAPIView.as_view(), name="submission"),
    path("users/", UserListAPIView.as_view(), name="user"),
    path("users/<int:pk>/", UserDetailAPIView.as_view(), name="user-retrieve"),
    path("login/", LoginAPIView.as_view(), name="user-login"),
    path("register/", RegisterAPIView.as_view(), name="user-register"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("users/update/<int:pk>/", UserUpdateAPIView.as_view(), name="user-update"),
    path(
        "users/password-change/",
        PasswordChangeAPIView.as_view(),
        name="password-change",
    ),
    path("workspace/", WorkspaceListAPIView.as_view(), name="workspace"),
    path(
        "workspace/<int:pk>/", WorkspaceUserListAPIView.as_view(), name="user-workspace"
    ),
    path(
        "workspace/detail/<int:pk>/",
        WorkspaceDetailAPIView.as_view(),
        name="workspace-retrieve",
    ),
]

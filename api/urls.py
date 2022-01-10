from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView


from .views import (
    ActivateEmailAPIView,
    FormDetailAPIView,
    GoogleLoginAPIView,
    LoginAPIView,
    PasswordChangeAPIView,
    RegisterAPIView,
    SubmissionDetailAPIView,
    SubmissionAPIView,
    SubscriberListAPIView,
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
    path("forms/<int:pk>/", FormListAPIView.as_view(), name="form-workspace"),
    path("forms/detail/<uuid:uuid>/",
         FormDetailAPIView.as_view(), name="form-detail"),
    path("f/<uuid:uuid>/", SubmissionAPIView.as_view(), name="create-submission"),
    path("submissions/", SubmissionAPIView.as_view(), name="submission"),
    path(
        "submissions/<int:pk>/",
        SubmissionDetailAPIView.as_view(),
        name="submission-delete",
    ),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("workspace/", WorkspaceListAPIView.as_view(), name="workspace"),
    path(
        "workspace/<int:pk>/", WorkspaceListAPIView.as_view(), name="user-workspace"
    ),
    path(
        "workspace/detail/<int:pk>/",
        WorkspaceDetailAPIView.as_view(),
        name="workspace-retrieve",
    ),
    path("users/", UserListAPIView.as_view(), name="user"),
    path("users/<int:pk>/", UserDetailAPIView.as_view(), name="user-retrieve"),
    path("users/update/<int:pk>/", UserUpdateAPIView.as_view(), name="user-update"),
    path(
        "users/password-change/",
        PasswordChangeAPIView.as_view(),
        name="password-change",
    ),
    path(
        "users/send-activation-email/",
        ActivateEmailAPIView.as_view(),
        name="send-activation-email",
    ),
    path("login/", LoginAPIView.as_view(), name="user-login"),
    path("register/", RegisterAPIView.as_view(), name="user-register"),
    path("google/", GoogleLoginAPIView.as_view(), name="google-login"),
]

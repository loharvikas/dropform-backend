from django.urls import path
from .views import (
    FormDetailAPIView,
    LoginAPIView,
    RegisterAPIView,
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
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("subscribers/", SubscriberListAPIView.as_view(), name="form"),
    path("forms/", FormListAPIView.as_view(), name="form"),
    path("forms/<int:pk>/", FormDetailAPIView.as_view(), name="form"),
    path("f/<uuid:uuid>/", CreateSubmissionAPIView.as_view(), name="create-submission"),
    path("submissions/", SubmissionListAPIView.as_view(), name="submission"),
    path("users/", UserListAPIView.as_view(), name="user"),
    path("users/<int:pk>/", UserDetailAPIView.as_view(), name="user-retrieve"),
    path("login/", LoginAPIView.as_view(), name="user-login"),
    path("register/", RegisterAPIView.as_view(), name="user-register"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("users/update/<int:pk>/", UserUpdateAPIView.as_view(), name="user-update"),
    path("workspace/", WorkspaceListAPIView.as_view(), name="workspace"),
    path(
        "workspace/<int:pk>/",
        WorkspaceDetailAPIView.as_view(),
        name="workspace-retrieve",
    ),
]

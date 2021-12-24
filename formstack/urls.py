from django.contrib import admin
from django.urls import path, include, re_path
from form.views import dummy_form, SubmissionCreation
from user.views import activate_user


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
    path("forms/", dummy_form),
    path("f/<uuid:uuid>/", SubmissionCreation.as_view(), name="create-submission"),
    path("activate/<uidb64>/<token>/", activate_user, name="activate"),
]

from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from helper import constants


from .managers import UserManager

payload = {

}


class User(AbstractBaseUser, PermissionsMixin):
    ACCOUNT_TYPE_CHOICES = (
        (constants.ACCOUNT_TESTING, constants.ACCOUNT_TESTING),
        (constants.ACCOUNT_STANDARD, constants.ACCOUNT_STANDARD),
        (constants.ACCOUNT_PROFESSIONAL, constants.ACCOUNT_PROFESSIONAL),
        (constants.ACCOUNT_BUSINESS, constants.ACCOUNT_BUSINESS),
    )

    email = models.EmailField("Email Address", unique=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    paid_user = models.BooleanField(default=False)
    account_type = models.CharField(
        max_length=255, choices=ACCOUNT_TYPE_CHOICES, default=constants.ACCOUNT_TESTING
    )
    stripe_customer_id = models.CharField(
        max_length=255, blank=True, null=True)

    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)
    last_modified_date = models.DateTimeField(default=timezone.now)
    # This date changes every month to reset the total submission counter of a user.
    last_rotation_date = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    @property
    def total_workspaces(self):
        """
        returns total workspace associated with user instance.
        """
        return self.workspaces.all().count()

    @property
    def total_forms(self):
        """
        returns total forms associated with user instance.
        """
        total_forms = 0
        workspaces_qs = self.workspaces.prefetch_related('forms').all()
        for workspace in workspaces_qs:
            total_forms += workspace.forms.all().count()
        return total_forms

    @property
    def total_submissions(self):
        """
        returns total submissions associated with user instance.
        """
        total_submisssions = 0
        workspaces_qs = self.workspaces.prefetch_related('forms').all()
        for workspace in workspaces_qs:
            forms_qs = workspace.forms.prefetch_related('submissions').all()
            for form in forms_qs:
                total_submisssions += form.submissions.filter(
                    created_date__gte=self.last_rotation_date).count()
        return total_submisssions

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        self.last_modified_date = timezone.now()
        super(User, self).save(*args, **kwargs)

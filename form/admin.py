from django.contrib import admin
from .models import Form
from submission.models import Submission

# Register your models here.


class SubmissionInline(admin.TabularInline):
    model = Submission


class FormAdmin(admin.ModelAdmin):
    model = Form
    inlines = [
        SubmissionInline,
    ]


admin.site.register(Form, FormAdmin)

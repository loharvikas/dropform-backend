from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from .models import Form, Submission
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


def dummy_form(request):
    return render(request, "forms/form.html")


@method_decorator(csrf_exempt, name="dispatch")
class SubmissionCreation(View):
    def post(self, request, *args, **kwargs):
        try:
            qd = request.POST
            fields = qd.dict()
            uuid = kwargs.get("uuid")
            form = Form.objects.get(uuid=uuid)
            Submission.objects.create(form=form, fields=fields)
            return HttpResponse("Done")
        except ObjectDoesNotExist:
            HttpResponse("Error")

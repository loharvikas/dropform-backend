from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from .models import Form
from submission.models import Submission
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import generics


from pprint import pprint


@method_decorator(csrf_exempt, name="dispatch")
class SubmissionCreation(View):
    def post(self, request, *args, **kwargs):
        try:
            qd = request.POST
            fields = qd.dict()
            uuid = kwargs.get("uuid")
            form = Form.objects.get(uuid=uuid)
            Submission.objects.create(form=form, fields=fields)
            return render(request, "general/redirect.html")
        except ObjectDoesNotExist:
            HttpResponse("Error")

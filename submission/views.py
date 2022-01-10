from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


from .models import Form, SubmissionFileUpload
from submission.models import Submission
from helper import constants
from .tasks import send_notification_email_task


@method_decorator(csrf_exempt, name="dispatch")
class SubmissionCreation(View):
    def post(self, request, *args, **kwargs):
        try:
            qd = request.POST
            fields = qd.dict()
            uuid = kwargs.get("uuid")
            form = Form.objects.get(uuid=uuid)
            user = form.workspace.user
            if user:
                account_limitations = constants.ACCOUNT_LIMITATIONS[
                    user.account_type.capitalize()
                ]
                if account_limitations["total_submissions"] <= user.total_submissions:
                    return render(request, "general/error.html")
                s = Submission.objects.create(form=form, fields=fields)
                for file in request.FILES.values():
                    SubmissionFileUpload.objects.create(
                        file_field=file, submission=s)
                if form.alert == True:
                    send_notification_email_task.delay(s.pk)
                return render(request, "general/redirect.html")
            return HttpResponse("Error")

        except ObjectDoesNotExist:
            HttpResponse("Error")

from ast import Sub
from django.test import TestCase
from django.db.models import ObjectDoesNotExist

from model_bakery import baker

from submission.models import Submission, SubmissionFileUpload


class TestSubmissionModel(TestCase):

    def setUp(self):
        self.user = baker.make('user.User')
        self.workspace = baker.make('workspace.Workspace', user=self.user)
        self.form = baker.make('form.Form', workspace=self.workspace)
        self.form2 = baker.make('form.Form', workspace=self.workspace)
        self.payload = {
            "fields": {
                "email": "test@gmail.com",
                "message": "Test message."
            },
            "form": self.form
        }
        self.submission = baker.make(
            'submission.Submission', form=self.form, fields=self.payload.get("fields"))

    def test_create_submission(self):
        Submission.objects.create(**self.payload)
        self.assertEqual(2, Submission.objects.all().count())

    def test_update_JSON_fields_submission(self):
        s = Submission.objects.get(pk=1)
        s.fields["email"] = "updated@gmail.com"
        s.save()
        self.assertEqual("updated@gmail.com", s.fields.get("email"))

    def test_retrieve_model_does_not_exist(self):
        with self.assertRaises(ObjectDoesNotExist):
            Submission.objects.get(pk=2)

    def test_update_form_submission(self):
        s = Submission.objects.get(pk=1)
        s.form = self.form2
        s.save()
        self.assertEqual(self.form2, s.form)

    def test_delete_submission(self):
        s = Submission.objects.get(pk=1)
        s.delete()
        with self.assertRaises(ObjectDoesNotExist):
            Submission.objects.get(pk=1)


class TestSubmissioFileModel(TestCase):
    def setUp(self):
        self.user = baker.make('user.User')
        self.workspace = baker.make('workspace.Workspace', user=self.user)
        self.form = baker.make('form.Form', workspace=self.workspace)
        self.form2 = baker.make('form.Form', workspace=self.workspace)
        self.submission = baker.make(
            'submission.Submission', form=self.form)
        self.submissionFile = baker.make('submission.SubmissionFileUpload')
        self.payload = {
            "name": "file",
            "submission": self.submission
        }

    def test_create_submission_file(self):
        SubmissionFileUpload.objects.create(**self.payload)
        self.assertEqual(2, SubmissionFileUpload.objects.all().count())

    def test_update_submission_file(self):
        s = SubmissionFileUpload.objects.get(pk=1)
        s.name = "updated"
        s.save()
        self.assertEqual("updated", s.name)

    def test_retrieve_model_doest_not_exist(self):
        with self.assertRaises(ObjectDoesNotExist):
            SubmissionFileUpload.objects.get(pk=2)

    def test_delete_submission_file(self):
        s = SubmissionFileUpload.objects.get(pk=1)
        s.delete()
        with self.assertRaises(ObjectDoesNotExist):
            SubmissionFileUpload.objects.get(pk=1)

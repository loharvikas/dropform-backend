from django.test import TestCase
from django.db.models import ObjectDoesNotExist

from model_bakery import baker

from form.models import Form


class TestFormModels(TestCase):

    def setUp(self):
        self.user = baker.make('user.User')
        self.workspace = baker.make('workspace.Workspace', user=self.user)
        self.form = baker.make('form.Form', workspace=self.workspace)
        self.payload = {
            "name": "test form",
            "description": "test description",
            "workspace": self.workspace
        }

    def test_new_form_creation(self):
        Form.objects.create(**self.payload)
        self.assertEqual(2, Form.objects.all().count())

    def test_update_form(self):
        UPDATED_NAME = "updated name"
        self.form.name = UPDATED_NAME
        self.form.save()
        self.assertEqual(UPDATED_NAME, self.form.name)

    def test_retrieve_model_doest_not_exist(self):
        with self.assertRaises(ObjectDoesNotExist):
            Form.objects.get(id=2)

    def test_delete_form(self):
        form = Form.objects.get(pk=1)
        form.delete()
        with self.assertRaises(ObjectDoesNotExist):
            Form.objects.get(id=1)

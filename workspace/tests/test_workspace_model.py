from django.test import TestCase
from django.db.models import ObjectDoesNotExist

from model_bakery import baker

from form.models import Workspace


class TestFormModels(TestCase):

    def setUp(self):
        self.user = baker.make('user.User')
        self.workspace = baker.make('workspace.Workspace', user=self.user)
        self.form = baker.make('form.Form', workspace=self.workspace)
        self.payload = {
            "name": "test form",
            "description": "test description",
            "user": self.user
        }

    def test_new_workspace_creation(self):
        Workspace.objects.create(**self.payload)
        self.assertEqual(2, Workspace.objects.all().count())

    def test_update_workspace(self):
        UPDATED_NAME = "updated name"
        self.workspace.name = UPDATED_NAME
        self.workspace.save()
        self.assertEqual(UPDATED_NAME, self.workspace.name)

    def test_retrieve_model_doest_not_exist(self):
        with self.assertRaises(ObjectDoesNotExist):
            Workspace.objects.get(id=2)

    def test_delete_workspace(self):
        workspace = Workspace.objects.get(pk=1)
        workspace.delete()
        with self.assertRaises(ObjectDoesNotExist):
            Workspace.objects.get(id=1)

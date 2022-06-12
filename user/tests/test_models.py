# from django.test import TestCase
# from django.contrib.auth import get_user_model
# from django.db.models import ObjectDoesNotExist
# from model_bakery import baker

# User = get_user_model()


# class TestModels(TestCase):

#     def setUp(self):
#         self.user = baker.make('user.User')
#         self.workspace = baker.make('workspace.Workspace', user=self.user)
#         self.form = baker.make('form.Form', workspace=self.workspace)
#         self.submission = baker.make('submission.Submission', form=self.form)
#         self.email = "test@gamil.com"
#         self.full_name = "Mark Django"

#     def test_new_user_creation(self):
#         User.objects.create(email=self.email, full_name=self.full_name)
#         self.assertEqual(2, User.objects.all().count())

#     def test_update_user(self):
#         UPDATED_NAME = "updated name"
#         self.user.name = UPDATED_NAME
#         self.user.save()
#         self.assertEqual(UPDATED_NAME, self.user.name)

#     def test_property_total_workspaces(self):
#         total_workspaces = self.user.total_workspaces
#         self.assertEqual(1, total_workspaces)

#     def test_property_total_forms(self):
#         total_forms = self.user.total_forms
#         self.assertEqual(1, total_forms)

#     def test_property_total_forms(self):
#         total_forms = self.user.total_forms
#         self.assertEqual(1, total_forms)

#     def test_delete_user(self):
#         user = User.objects.get(pk=1)
#         user.delete()
#         with self.assertRaises(ObjectDoesNotExist):
#             User.objects.get(id=1)

# from django.urls import reverse

# from rest_framework.test import APIClient, APITestCase
# from rest_framework import status


# from model_bakery import baker
# import uuid

# from form.models import Form


# FORM_URL = reverse("form")
# # FORM_LIST_URL = reverse("form-retrieve")


# def form_uuid_url(i):
#     return reverse("form-detail", args=[i])


# def workspace_form_pk_url(i):
#     return reverse("form-retrieve", args=[i])


# class TestAPI(APITestCase):

#     def setUp(self) -> None:
#         self.client = APIClient()
#         self.user = baker.make('user.User')
#         self.client.force_authenticate(user=self.user)
#         self.workspace = baker.make('workspace.Workspace', user=self.user)
#         self.form = baker.make('form.Form', workspace=self.workspace)
#         self.payload = {
#             "name": "Test form",
#             "description": "amazing",
#             "workspace": self.workspace
#         }

#     def test_retrieve_form_list(self):
#         res = self.client.get(workspace_form_pk_url(1))
#         self.assertEqual(res.status_code, status.HTTP_200_OK)

#     def test_retrieve_form_detail(self):
#         f = Form.objects.get(pk=1)
#         res = self.client.get(form_uuid_url(f.uuid))
#         self.assertEqual(res.status_code, status.HTTP_200_OK)

#     def test_retrieve_form_does_not_exist(self):
#         u = uuid.uuid1()
#         res = self.client.get(form_uuid_url(str(u)))
#         self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

#     # def test_post_form(self):
#     #     res = self.client.post(
#     #         FORM_URL, self.payload, content_type='application/json')
#     #     self.assertEqual(res.status_code, status.HTTP_201_CREATED)

#     def test_delete_user(self):
#         f = Form.objects.get(pk=1)
#         res = self.client.delete(form_uuid_url(f.uuid))
#         self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

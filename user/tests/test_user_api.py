# from rest_framework.test import APIClient, APITestCase
# from django.urls import reverse
# from model_bakery import baker
# from rest_framework import status

# import json

# USER_URL = reverse("user")
# USER_REGISTER_URL = reverse("user-register")


# def user_pk_url(i):
#     return reverse("user-retrieve", args=[i])


# class TestAPI(APITestCase):

#     def setUp(self) -> None:
#         self.client = APIClient()
#         self.user = baker.make('user.User')
#         self.client.force_authenticate(user=self.user)
#         self.payload = {
#             "email": "test@gmail.com",
#             "full_name": "django@gmail.com",
#             "password": "test12345"
#         }

#     def test_retrieve_user_list(self):
#         res = self.client.get(USER_URL)
#         self.assertEqual(res.status_code, status.HTTP_200_OK)

#     def test_retrieve_user_detail(self):
#         res = self.client.get(user_pk_url(1))
#         self.assertEqual(res.status_code, status.HTTP_200_OK)

#     def test_retrieve_user_does_not_exist(self):
#         res = self.client.get(user_pk_url(2))
#         self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

#     # def test_post_user(self):
#     #     res = self.client.post(
#     #         USER_REGISTER_URL, self.payload, content_type='application/json')
#     #     self.assertEqual(res.status_code, status.HTTP_201_CREATED)

#     def test_delete_user(self):
#         res = self.client.delete(user_pk_url(1))
#         self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

import os
import sys
import inspect

import pytest
import django

from users import urls as users_urls
from users import models as users_models


currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fyiona.settings")

django.setup()


############################################################################
############################# USERS URLS TESTS #############################
############################################################################

test_post_data = {
    "test": "test",
    "1": None,
    "2": 23,
    "3": "string",
    "4": ["list", 1234, "string"],
}


# @pytest.mark.django_db
# @pytest.mark.urls("users.urls")
# def test_login_url(client):
#     # post: right auth --> success
#     login_request = client.post(
#         "/login/",
#         data={
#             "email": os.environ.get("DJANGO_SUPERUSER_EMAIL"),
#             "password": os.environ.get("DJANGO_SUPERUSER_PASSWORD"),
#         },
#     )

#     assert login_request.status_code == 200

# # post: auth with bad password --> error
# with pytest.raises(AssertionError):
#     assert requests.post(
#         "http://localhost:8000/api/v1/accounts/login/",
#         data={
#             "email": os.environ.get("DJANGO_SUPERUSER_EMAIL"),
#             "password": "testtesttest",
#         },
#     )
# # post: auth without password --> error
# with pytest.raises(AssertionError):
#     assert requests.post(
#         "http://localhost:8000/api/v1/accounts/login/",
#         data={
#             "email": os.environ.get("DJANGO_SUPERUSER_EMAIL"),
#             "password": "",
#         },
#     )
# # post: auth witn blank fields --> error
# with pytest.raises(AssertionError):
#     assert requests.post(
#         "http://localhost:8000/api/v1/accounts/login/",
#         data={
#             "email": "",
#             "password": "",
#         },
#     )


# def test_users_list_url():
#     # get --> success
#     assert requests.get(
#         "http://localhost:8000/api/v1/accounts/",
#         auth=HTTPBasicAuth(os.environ.get("DJANGO_SUPERUSER_EMAIL"), os.environ.get("DJANGO_SUPERUSER_PASSWORD")),
#     )
#     # post --> error
#     with pytest.raises(AssertionError):
#         assert requests.post(
#             "http://localhost:8000/api/v1/accounts/",
#             data=test_post_data,
#             auth=HTTPBasicAuth(os.environ.get("DJANGO_SUPERUSER_EMAIL"), os.environ.get("DJANGO_SUPERUSER_PASSWORD")),
#         )


# def test_registration_url():
#     # get --> error
#     with pytest.raises(AssertionError):
#         assert requests.get("http://localhost:8000/api/v1/accounts/registration/")
#     # post --> success
#     assert requests.post(
#         "http://localhost:8000/api/v1/accounts/registration/",
#         data={
#             "first_name": "Example",
#             "last_name": "Example",
#             "email": "example@gmail.com",
#             "phone_number": "+996551578300",
#             "password": "qwex1053",
#             },
#     )


# @pytest.mark.parametrize("data", [
#                                     {"first_name":"John", "last_name":"Smith", "phone_number":"+996552555555"},
#                                         ])
# def test_change_profile_good(data):
#     # patch --> success
#     assert requests.patch("http://localhost:8000/api/v1/accounts/change_profile/", data=data, auth=HTTPBasicAuth("example@gmail.com", "qwex1053"))


# @pytest.mark.parametrize("data", [
#                                     {"first_name":'1244', "last_name":"1214", "phone_number":"wqrqtqtqefe"},
#                                     {"first_name":None, "last_name":None, "phone_number":None},
#                                     {"first_name":None, "last_name":None, "phone_number":"wqrqtqtqefe"},
#                                         ])
# def test_change_profile_bad(data):
#     # patch: phone_number is text --> error
#     with pytest.raises(AssertionError):
#         assert requests.patch("http://localhost:8000/api/v1/accounts/change_profile/", data=data, auth=HTTPBasicAuth(os.environ.get("DJANGO_SUPERUSER_EMAIL"), os.environ.get("DJANGO_SUPERUSER_PASSWORD")))


# def test_users_delete():
#     # delete: delete without auth --> error
#     with pytest.raises(AssertionError):
#         assert requests.delete("http://localhost:8000/api/v1/accounts/delete/")
#     # post --> error
#     with pytest.raises(AssertionError):
#         assert requests.post("http://localhost:8000/api/v1/accounts/delete/", data=test_post_data)
#     # get --> error
#     with pytest.raises(AssertionError):
#         assert requests.get("http://localhost:8000/api/v1/accounts/delete/")
#     # delete --> success
#     assert requests.delete("http://localhost:8000/api/v1/accounts/delete/", auth=HTTPBasicAuth("example@gmail.com", "qwex1053"))
#     # delete: delete one more time after delete --> error
#     with pytest.raises(AssertionError):
#         assert requests.delete("http://localhost:8000/api/v1/accounts/delete/", auth=HTTPBasicAuth("example@gmail.com", "qwex1053"))

# ###########################################################################
# ############################## POSTS TESTS ################################
# ###########################################################################

# posts_good_data = [
#     (
#         {"post_file":open(
#             "/home/rus/Desktop/work/fyiona/fyiona/media/default_profile_image.png",
#             "rb",
#         )},
#         {"caption": "some text for test create post"},
#         (
#             {"post_file":open(
#             "/home/rus/Desktop/work/fyiona/fyiona/media/default_profile_image.png",
#             "rb")},
#             {"caption":"some text for test update post"}
#         )
#     ),
# ]

# def test_posts_list_url():
#     # get --> success
#     assert requests.get(
#         "http://localhost:8000/api/v1/posts/",
#         auth=HTTPBasicAuth(os.environ.get("DJANGO_SUPERUSER_EMAIL"), os.environ.get("DJANGO_SUPERUSER_PASSWORD")),
#     )
#     # post --> error
#     with pytest.raises(AssertionError):
#         assert requests.post(
#             "http://localhost:8000/api/v1/posts/",
#             data=test_post_data,
#             auth=HTTPBasicAuth(os.environ.get("DJANGO_SUPERUSER_EMAIL"), os.environ.get("DJANGO_SUPERUSER_PASSWORD")),
#         )


# headers = {
#     "sessionid" : "19k09s5nfuod2vo3evvkw9esfziq6ul0",
#     "csrftoken" : "L2S0k0k4hgQkIbfecyRhGsBhdRgfO6uX6PhCyxC75518zgTQme9Jz0xXutyl6v5E"
# }

# token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjJmMjQ2ZDVmLTI1MzEtNDFiZC1hM2EzLWI4NzY3MDAxYzVkZCIsImV4cCI6MTYzNDU5MDczM30.7-xbaPLTU5DBGmFZRjXnHgcvsBKrltP9y-2bEtuAI1s"


# @pytest.mark.parametrize("post_file, caption, update_data", posts_good_data)
# def test_CRUD_posts_good(post_file, caption, update_data):
#     list_response = requests.get(
#         "http://localhost:8000/api/v1/posts/",
#         auth=HTTPBasicAuth(os.environ.get("DJANGO_SUPERUSER_EMAIL"), os.environ.get("DJANGO_SUPERUSER_PASSWORD"))
#     )
#     assert list_response
#     create_response = requests.post(
#         "http://localhost:8000/api/v1/posts/create/",
#         files=post_file,
#         data=caption,
#         auth=HTTPBasicAuth(os.environ.get("DJANGO_SUPERUSER_EMAIL"), os.environ.get("DJANGO_SUPERUSER_PASSWORD")),
#     )
#     assert create_response
#     post_id = json.loads(create_response.text).get("result").get("post_id")
#     update_response = requests.patch(f"http://localhost:8000/api/v1/posts/update/{post_id}/",
#     files= update_data[0],
#     data = update_data[1],
#     auth=HTTPBasicAuth(os.environ.get("DJANGO_SUPERUSER_EMAIL"), os.environ.get("DJANGO_SUPERUSER_PASSWORD")))
#     assert update_response
#     detail_response = requests.get(f"http://localhost:8000/api/v1/posts/details/{post_id}",
#     auth=HTTPBasicAuth(os.environ.get("DJANGO_SUPERUSER_EMAIL"), os.environ.get("DJANGO_SUPERUSER_PASSWORD")))
#     assert detail_response
#     delete_response =  requests.delete(f"http://localhost:8000/api/v1/posts/delete/{post_id}",
#     auth=HTTPBasicAuth(os.environ.get("DJANGO_SUPERUSER_EMAIL"), os.environ.get("DJANGO_SUPERUSER_PASSWORD")))
#     assert delete_response


# posts_bad_data = [
#     (
#         None,
#         {"caption": "some text for test"},
#     ),
#     (
#         open(
#             "/home/rus/Desktop/work/fyiona/fyiona/media/default_profile_image.png",
#             "rb",
#         ),
#         {"caption": None},
#     ),
#     (
#         open(
#             "/home/rus/Desktop/work/fyiona/fyiona/media/default_profile_image.png",
#             "rb",
#         ),
#         {"bad_field_for_test": "2312415"},
#     ),
# ]

# @pytest.mark.parametrize("post_file, caption", posts_bad_data)
# def test_posts_create_bad(post_file, caption):
#     with pytest.raises(AssertionError):
#         assert requests.post(
#             "http://localhost:8000/api/v1/posts/create/",
#             files={"post_file": post_file},
#             data=caption,
#             auth=HTTPBasicAuth(os.environ.get("DJANGO_SUPERUSER_EMAIL"), os.environ.get("DJANGO_SUPERUSER_PASSWORD")),
#         )

# posts_update_bad_data = [
#     (
#         {"post_file":open(
#             "/home/rus/Desktop/work/fyiona/fyiona/tests/test_files/test_image.png",
#             "rb",
#         )},
#         {"caption": "some text for test create post"},
#         (
#             {"post_file":open(
#                 "/home/rus/Desktop/work/fyiona/fyiona/tests/test_files/test_video.mp4",
#                 "rb",
#             )},
#             {"caption": "some text for test create post"},
#         )
#     ),
#     (
#         {"post_file":open(
#             "/home/rus/Desktop/work/fyiona/fyiona/tests/test_files/test_image.png",
#             "rb",
#         )},
#         {"caption": "some text for test create post"},
#         (
#             {"post_file":open(
#                 "/home/rus/Desktop/work/fyiona/fyiona/tests/test_files/test_sound.mp3",
#                 "rb",
#             )},
#             {"caption": "some text for test create post"},
#         )
#     ),
# ]


# @pytest.mark.parametrize("post_file, caption, update_data", posts_update_bad_data)
# def test_CRUD_posts_bad(post_file, caption, update_data):
#     create_response = requests.post(
#         "http://localhost:8000/api/v1/posts/create/",
#         files=post_file,
#         data=caption,
#         auth=HTTPBasicAuth(os.environ.get("DJANGO_SUPERUSER_EMAIL"), os.environ.get("DJANGO_SUPERUSER_PASSWORD")),
#     )
#     post_id = json.loads(create_response.text).get("result").get("post_id")
#     with pytest.raises(AssertionError):
#         update_response = requests.patch(f"http://localhost:8000/api/v1/posts/update/{post_id}/",
#         files = update_data[0],
#         data = update_data[1],
#         auth=HTTPBasicAuth(os.environ.get("DJANGO_SUPERUSER_EMAIL"), os.environ.get("DJANGO_SUPERUSER_PASSWORD")))
#         assert update_response

# ###########################################################################
# ############################# COMMENTS TESTS ##############################
# ###########################################################################

# #### Еще в разработке.....

# # @pytest.mark.django_db
# # def test_comments_CRUD_good():
# #     create_post_response = requests.post(
# #         "http://localhost:8000/api/v1/posts/create/",
# #         files=posts_good_data[0][0],
# #         data={"caption":"post for test comments"},
# #         auth=HTTPBasicAuth(os.environ.get("DJANGO_SUPERUSER_EMAIL"), os.environ.get("DJANGO_SUPERUSER_PASSWORD")),
# #     )
# #     post_id = json.loads(create_post_response.text).get("result").get("post_id")
# #     # print(Post.objects.get(id=165))
# #     list_comment = requests.get(
# #         "http://localhost:8000/api/v1/posts/comments/",
# #         auth=HTTPBasicAuth(os.environ.get("DJANGO_SUPERUSER_EMAIL"), os.environ.get("DJANGO_SUPERUSER_PASSWORD")),
# #     )
# #     assert list_comment
# #     create_comment = requests.post(
# #         "http://localhost:8000/api/v1/posts/comments/create/",
# #         data={"text":"test text for create comment", "post": Post.objects.get(pk=post_id)},
# #         auth=HTTPBasicAuth(os.environ.get("DJANGO_SUPERUSER_EMAIL"), os.environ.get("DJANGO_SUPERUSER_PASSWORD")),
# #     )

# #     assert create_comment

# #     comment_id = json.loads(create_comment.text).get("result").get("comment_id")

# #     delete_comment = requests.delete(
# #         f"http://localhost:8000/api/v1/posts/comments/delete/{comment_id}/",
# #         auth=HTTPBasicAuth(os.environ.get("DJANGO_SUPERUSER_EMAIL"), os.environ.get("DJANGO_SUPERUSER_PASSWORD")),
# #     )
# #     assert delete_comment

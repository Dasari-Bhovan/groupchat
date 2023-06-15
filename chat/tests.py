from django.test import TestCase,Client
from rest_framework.test import APIClient
from django.contrib.auth.models import User
# Create your tests here.
import unittest
import requests
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Group,Messages
from django.utils import timezone

class TestCase(APITestCase):
    base_url = "http://localhost:8000/chat/api/"
    def test_login_with_correct_user(self):
        url=self.base_url+"login"
        data={
            "username":"admin",
            "password":"bhovan"
        }
        response=requests.post(url,json=data)
        self.assertEqual(response.status_code,200)
    def test_login_with_wrong_user(self):
        url=self.base_url+"login"
        data={
            "username":"nouser",
            "password":"nopassword"
        }
        response=requests.post(url,json=data)
        self.assertEqual(response.status_code,400)
    
    def test_register(self):
        url=self.base_url+"register"
        self.client=APIClient()
        admin_user = User.objects.create_superuser(username='admin1', password='admin')
        self.client.force_login(admin_user)
        data={
            "username":"testing_user1",
            "email":"teshjt@gamil.com",
            "password":"hi123764567"
        }
        response=self.client.post(url,data,format='json')
        self.assertEqual(response.status_code,201)
        
    def test_register_noadmin(self):
        url=self.base_url+"register"
        self.client=APIClient()
        normal_user = User.objects.create(username='test1', password='normal')
        self.client.force_login(normal_user)
        data={
            "username":"testing_user1",
            "email":"teshjt@gamil.com",
            "password":"hi123764567"
        }
        response=self.client.post(url,data,format='json')
        self.assertEqual(response.status_code,403)
    def logout(self):
        url=self.base_url+"logout"
        self.client=APIClient()
        normal_user = User.objects.create(username='test1', password='normal')
        self.client.force_login(normal_user)
        response=self.client.get(url)
        self.assertEqual(response.status_code,200)


        
class GroupTest(TestCase):
    base_url = "http://localhost:8000/chat/api/"
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            username='testus',
            email='testus@example.com',
            password='test12345'
        )
        self.client.force_login(self.user)        

    def test_create_group(self):
        url = self.base_url + "groups"
        data = {
            "group_name": "Testing",
            "group_info": "Test Group Info",
            "members": [1,]
        }

        response = self.client.post(url, data,format='json')
        # print(response)
        self.assertEqual(response.status_code, 201)  # Assert that the response is successful
    #     # You can add more assertions to validate the response content or headers if needed

    def test_get_groups_empty(self):
        url = self.base_url + "groups"
        self.client=APIClient()
        normal_user = User.objects.create(username='test1', email="hi@gmail.com",password='normal')
        self.client.force_login(normal_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404) 
        
    def test_get_groups(self):
        url = self.base_url + "groups"
        self.client=APIClient()
        normal_user = User.objects.create(username='test1', email="hi@gmail.com",password='normal')
        # user=User.objects.get(normal_user)
        self.client.force_login(normal_user)
        
        self.x=Group.objects.create(group_name="hi",creater=normal_user,group_info="just a testing group")
        self.x.members.set([1,2])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test__add_members_groups(self):
        url = self.base_url + "groups"
        self.client=APIClient()
        normal_user = User.objects.create(username='test2', email="hi1@gmail.com",password='normal')
        # user=User.objects.get(normal_user)
        self.client.force_login(normal_user)
        x=Group.objects.create(group_name="hi",creater=normal_user,group_info="just a testing group")
        x.members.set([1,])
        x=Group.objects.get(group_name="hi")
        x.members.add(2)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200) 
class MessageTest(TestCase):
    base_url = "http://localhost:8000/chat/api/"
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            username='testus',
            email='testus@example.com',
            password='test12345'
        )
        self.client.force_login(self.user)
    
    def test_get_messages(self):
        # grp_name="Testing_Messages"
        # self.client=APIClient()
        # normal_user = User.objects.create(username='test1', email="hi@gmail.com",password='normal')
        # # user=User.objects.get(normal_user)
        # self.client.force_login(normal_user)
        
        # x=Group.objects.create(group_name=grp_name,creater=normal_user,group_info="just a testing group")
        # x.members.set([1,2])
        # url = self.base_url+"/groups/"+grp_name+"/messages"
        # response = self.client.get(url)
        # self.assertEqual(response.status_code, 200)
        self.client=APIClient()
        normal_user = User.objects.create(username='test1', email="hi@gmail.com",password='normal')
        # user=User.objects.get(normal_user)
        self.client.force_login(normal_user)
        grp_name="hi"
        url = self.base_url + "groups/"+grp_name+"/messages"
        self.x=Group.objects.create(group_name="hi",creater=normal_user,group_info="just a testing group")
        self.x.members.set([1,2])
        message=Messages.objects.create(parent_group=self.x,parent_user=normal_user,message_text="Hi",date_posted=timezone.localtime())
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    def test_messages_post(self):
        self.client=APIClient()
        normal_user = User.objects.create(username='test1', email="hi@gmail.com",password='normal')
        # user=User.objects.get(normal_user)
        self.client.force_login(normal_user)
        grp_name="hi"
        url = self.base_url + "groups/"+grp_name+"/messages"
        self.x=Group.objects.create(group_name="hi",creater=normal_user,group_info="just a testing group")
        self.x.members.set([1,2])
        data={
                "message_text": "Hi this is",
                "date_posted": timezone.localtime(),
                "parent_group": self.x.id,
                "parent_user": normal_user.id,
             }
        response = self.client.post(url,data,format='json')
        self.assertEqual(response.status_code, 201) 
        # Assert that the response is successful
    #     # You can add more assertions to validate the response content or headers if needed

    # # Add more test methods to cover other API endpoints and scenarios

if __name__ == "__main__":
    APITestCase.main()

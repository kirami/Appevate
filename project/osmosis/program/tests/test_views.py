from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase

from socialrebate.advertiser.models import Advertiser

from .. import views


User = get_user_model()


class AdvertiserViewTestCase(APITestCase):
    
   


    def test_advertiser_post(self):
        """
        Test advertiser post
        """

        #create user
        user = User.objects.create(email="advTest", password="111111")
        
        url = reverse('advertisers-list')
        data = {'user':user.id, 'contact_name': 'test name', "contact_phone": "11111111"}
        response = self.client.post(url, data, format='json')
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(Advertiser.objects.count(), 1)
        self.assertEquals(Advertiser.objects.get().contact_phone, "11111111")

    
    def test_advertiser_put(self):
        """
        Test advertiser patch
        """

        #create user
        user = User.objects.create(email="advTest", password="111111")
        advertiser = Advertiser.objects.create(user = user, contact_name = "test name", contact_phone="1111111")
        
        url = reverse('advertisers-detail', kwargs={'pk':user.id})
        data = { "contact_phone": "2222222"}
        response = self.client.patch(url, data, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        
        self.assertEquals(Advertiser.objects.get().contact_phone, "2222222")

    def test_advertiser_delete(self):
        """
        Test advertiser delete
        """

        #create user
        user = User.objects.create(email="advTest", password="111111")
        advertiser = Advertiser.objects.create(user = user, contact_name = "test name", contact_phone="1111111")
        
        url = reverse('advertisers-detail', kwargs={'pk':user.id})
        data = { }
        response = self.client.delete(url, data, format='json')

        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
        
        self.assertEquals(Advertiser.objects.count(), 0)

   
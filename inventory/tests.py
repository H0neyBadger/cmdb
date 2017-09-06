from django.test import TestCase

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import force_authenticate

from django.contrib.auth.models import User
from inventory.models import Host

class AccountTests(APITestCase):

    def test_create_host(self):
        """
        Ensure we can create a new host object.
        """
        url = reverse('host-list')
        data = {
            "interfaces": [
                {
                    "ip_address": [
                        {
                            "ip": "1.1.1.1",
                        },
                        {
                            "ip": "1.1.1.2",
                        }
                    ],
                    "name": "no_int",
                    "mac_address": "mac_addr",
                }
            ],
            "name": "hostname",
            "snow_id": "1122334455",
            "uuid": "4c8b3883-323b-48d7-a504-e73a724e6ac5",
            "machine_id": "4c8b3883-323b-48d7-a504-e73a724e6ac5",
            "local_name": "localhost",
            "dns_name": "hello.world.lab",
            "vm_name": None,
            "geo": None,
            "team": None,
            "domain": None,
            "hardware_type": None,
            "parent_host": None,
            "os_family": None,
            "os_distribution": None,
            "os_distribution_version": None,
            "system_team": None,
            "application_team": None
        }
        user = User.objects.create(username='unitest')
        self.client.force_authenticate(user=user)
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Host.objects.count(), 1)
        self.assertEqual(Host.objects.get().name, 'hostname')


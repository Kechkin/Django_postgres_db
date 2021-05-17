import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "convert_v2.settings")
django.setup()
from django.test import TestCase, Client


class SimpleTest(TestCase):
    def test_get_index(self):
        client = Client()
        response = client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_add(self):
        c = Client()
        response = c.post('/', {'currency': 'Евро', 'course': '82.4'})
        self.assertEqual(response.status_code, 200)

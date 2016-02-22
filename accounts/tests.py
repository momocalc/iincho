from django.test import TestCase
from django.contrib.auth.models import User

from .models import Profile


class ProfileModelTest(TestCase):
    def setUp(self):
        User.objects.create_user(username='spam', password='spam_pass')
        User.objects.create_user(username='ham', password='ham_pass')

    def test_saving_and_retrieving_items(self):
        p1 = Profile(photo='', user=User.objects.get(pk=1))
        p1.save()

        p2_photo_url = 'http://test.jpg'
        p2 = Profile(photo=p2_photo_url, user=User.objects.get(pk=2))
        p2.save()

        saved_items = Profile.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.photo, '')
        self.assertEqual(first_saved_item.user, User.objects.get(pk=1))
        self.assertEqual(second_saved_item.photo, p2_photo_url)
        self.assertEqual(second_saved_item.user, User.objects.get(pk=2))

    def test_saving_relation_with_user(self):
        p1 = Profile(photo='', user=User.objects.get(pk=1))
        p1.save()
        p2 = Profile(photo='', user=User.objects.get(pk=2))
        p2.save()

        self.assertEqual(p1, User.objects.get(pk=1).profile)
        self.assertEqual(p2, User.objects.get(pk=2).profile)

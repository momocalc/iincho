from django.contrib.auth.models import User


def create_test_user(count=1):
    for i in range(count):
        User.objects.create_user(username='test_user_{0}'.format(i + 1),
                                 password='password_{0}'.format(i + 1),
                                 first_name='first_{0}'.format(i + 1),
                                 last_name='last_{0}'.format(i + 1))

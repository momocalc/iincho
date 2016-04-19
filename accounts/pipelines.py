from django.conf import settings
import urllib.request
from .models import Profile
from social.backends.google import GoogleOAuth2
import os


def ensure_sub_dir(*dir_names):
    res = os.path.join(settings.MEDIA_ROOT, 'accounts', *dir_names)
    if not os.path.exists(res):
        os.makedirs(res)
    return res


def download_user_avator(url):
    import uuid
    ext = os.path.splitext(
        os.path.basename(url).split('?')[0])[1]
    image_name = str(uuid.uuid1()) + ext

    tmp_path = os.path.join(ensure_sub_dir('tmp'), image_name)
    local_file = open(tmp_path, 'wb')

    img = urllib.request.urlopen(url)
    local_file.write(img.read())
    local_file.close()
    img.close()
    return tmp_path, ext


def __set_avatar(url, user):
    from django.core.files import File
    # local_file = open(tmp_path)
    tmp_path, ext = download_user_avator(url)
    f = open(tmp_path, 'rb')
    user.profile.photo.save(user.username + ext, File(f))

def get_user_avatar(strategy, user, response, is_new=False, *args, **kwargs):

    if not user:
        return

    if not hasattr(user, 'profile'):
        Profile(user=user).save()

    if isinstance(kwargs['backend'], GoogleOAuth2) and not user.profile.photo:
        __set_avatar(response['image']['url'], user)
        user.profile.save()

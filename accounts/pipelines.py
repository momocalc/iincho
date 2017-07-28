from django.conf import settings
import urllib.request
from .models import Profile
from social.backends.google import GoogleOAuth2
from django.core.files import File
import os
import uuid


def ensure_sub_dir(*dir_names):
    res = os.path.join(settings.MEDIA_ROOT, 'accounts', *dir_names)
    if not os.path.exists(res):
        os.makedirs(res)
    return res


def download_user_photo(url):
    """
    アイコンを取得する
    :param url:アイコンURL
    :return:
    """
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


def __set_photo(url, user):
    """
    プロファイルにアイコンを登録する
    :param url: アイコンURL
    :param user:
    """
    tmp_path, ext = download_user_photo(url)
    f = open(tmp_path, 'rb')
    user.profile.photo.save(user.username + ext, File(f))


def get_user_avatar(strategy, user, response, is_new=False, *args, **kwargs):
    if not user:
        return

    if not hasattr(user, 'profile'):
        Profile(user=user).save()

    if isinstance(kwargs['backend'], GoogleOAuth2) and not user.profile.photo:
        __set_photo(response['image']['url'], user)
        user.profile.save()

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


def image_download(url, user_id):

    ext = os.path.splitext(
        os.path.basename(url).split('?')[0])[1]
    image_name = str(user_id) + str(ext)

    tmp_path = os.path.join(ensure_sub_dir('tmp'), image_name)
    local_file = open(tmp_path, 'wb')

    img = urllib.request.urlopen(url)
    local_file.write(img.read())
    img.close()
    local_file.close()

    # プロファイル画像ディレクトリに移動
    image_path = os.path.join(ensure_sub_dir('images', 'icon'), image_name)
    os.rename(tmp_path, image_path)
    return image_name


def get_user_avatar(strategy, user, response, is_new=False, *args, **kwargs):

    if not user:
        return

    if not hasattr(user, 'profile'):
        Profile(user=user).save()

    if is_new and isinstance(kwargs['backend'], GoogleOAuth2):
        try:
            image_name = image_download(response['image']['url'], user.id)
            if image_name:
                user.profile.photo = image_name
                user.profile.save()

        except Exception:
            pass

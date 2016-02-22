from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from .forms import BasicUploadFileForm
from django.conf import settings
import os


def upload_file(request):
    if request.method == 'POST':
        form = BasicUploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect(reverse('upload_file'))
        else:
            return render(request, 'attachments/upload.html', {'form': form})
    else:
        form = BasicUploadFileForm()
        return render(request, 'attachments/upload.html', {'form': form})


def handle_uploaded_file(f):
    '''
    ファイル保存ハンドラサンプル
    modelFormを使用せず保存する場合はこちらを利用する
    :param f:
    :return:
    '''
    with open(os.path.join(settings.MEDIA_ROOT, 'name.txt'), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


@require_http_methods(['POST'])
def upload_file_jq(request):
    form = BasicUploadFileForm(request.POST, request.FILES)

    if form.is_valid():
        form.save()
        split_name = form.instance.file.name.rsplit('/', 1)
        to_json = {
            'status': 'success',
            'file_url': form.instance.file.url,
            'file_name': split_name[0] if len(split_name) == 1 else split_name[1]
        }
    else:
        messages = list()
        for k in form.errors:
            messages.extend([x for x in form.errors[k]])

        to_json = {
            'status': 'error',
            'messages': messages,
        }

    return JsonResponse(to_json)

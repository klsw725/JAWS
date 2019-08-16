from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import numpy as np

# import mysite.facer.face_server.video

# Creates a temporary buffer which can hold the largest image we can transmit
img_buf = bytearray(9999999)
img_view = memoryview(img_buf)

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

@csrf_exempt
def face(request, user_id):
    cmd = request.POST['msg'][:5]
    if(cmd == 'image'):
        temp_shape = request.POST['msg'][6:].split(',')
        shape = tuple([int(x) for x in temp_shape])
        img_view = request.POST['img_buffer']
        img = np.array(list(int(x) for x in img_view))
        print(img)
        # img = np.fromstring(img_view, dtype='uint8').reshape(shape)

    # cmd = request.POST['msg'].decode('asii')
    return HttpResponse("Hello, world. You're at the polls index.")
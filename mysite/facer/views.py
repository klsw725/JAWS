from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Images

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

@csrf_exempt
def face(request, user_id):
    print(request.POST)
    return HttpResponse("Hello, world. You're at the polls index.")
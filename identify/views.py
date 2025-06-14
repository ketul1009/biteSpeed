from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from .models import Contact
from django.db import transaction
from django.db.models import Q

@csrf_exempt
@require_POST
def identify(request):
    data = json.loads(request.body)
    print(data)
    return JsonResponse({"status": "success"})

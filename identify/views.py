from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from .functions import get_primary_contacts, create_contact, get_consolidated_contact, check_if_contact_exists, update_primary_contact
from .serializers import ContactSerializer

@csrf_exempt
@require_POST
def identify(request):
    data = json.loads(request.body)
    email = data.get('email')
    phoneNumber = data.get('phoneNumber')
    if not email and not phoneNumber:
        return JsonResponse({"status": "ERR", "message": "Email or phoneNumber is required"}, status=400)
    
    priamry_contacts = get_primary_contacts(email, phoneNumber)
    if priamry_contacts.count() > 1:
        print("More than 1 primary contact")
        update_primary_contact(priamry_contacts[1], priamry_contacts[0])
        return JsonResponse({"contact": get_consolidated_contact(priamry_contacts[0])})
    elif priamry_contacts.count() == 1:
        print("1 primary contact")
        if check_if_contact_exists(email, phoneNumber):
            return JsonResponse({"contact": get_consolidated_contact(priamry_contacts[0])})
        else:
            if email and phoneNumber:
                new_contact = create_contact(email, phoneNumber, 'secondary', priamry_contacts[0])
                return JsonResponse({"contact": get_consolidated_contact(new_contact)})
            else:
                return JsonResponse({"contact": get_consolidated_contact(priamry_contacts[0])})
    else:
        print("No primary contact")
        new_contact = create_contact(email, phoneNumber, 'primary')
        return JsonResponse({"contact": get_consolidated_contact(new_contact)})
    

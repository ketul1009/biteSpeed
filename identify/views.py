from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
import json
import logging
from .functions import get_all_contacts, create_contact, get_consolidated_contact, update_primary_contact, check_if_new_info

logger = logging.getLogger(__name__)

@csrf_exempt
@require_POST
def identify(request):
    try:
        data = json.loads(request.body)
        logger.info(f"Received request data: {data}")
        
        if not data or not isinstance(data, dict):
            return JsonResponse({"status": "ERR", "message": "Invalid request body"}, status=400)
            
        email = data.get('email')
        phoneNumber = data.get('phoneNumber')
        
        if not email and not phoneNumber:
            return JsonResponse({"status": "ERR", "message": "Email or phoneNumber is required"}, status=400)
        
        try:
            all_contacts = get_all_contacts(email, phoneNumber)
            if all_contacts.count() == 0:
                new_contact = create_contact(email, phoneNumber, 'primary')
                return JsonResponse({"contact": get_consolidated_contact(new_contact)})
            else:
                primary_contact = all_contacts.first()
                for contact in all_contacts:
                    if contact.id != primary_contact.id and contact.linkPrecedence != 'secondary':
                        update_primary_contact(contact, primary_contact)
                if check_if_new_info(email, phoneNumber):
                    new_contact = create_contact(email, phoneNumber, 'secondary', primary_contact)
                    return JsonResponse({"contact": get_consolidated_contact(new_contact)})
                return JsonResponse({"contact": get_consolidated_contact(primary_contact)})
        except Exception as e:
            logger.error(f"Error processing request: {str(e)}", exc_info=True)
            return JsonResponse({"status": "ERR", "message": "Internal server error"}, status=500)
            
    except json.JSONDecodeError:
        logger.error("Invalid JSON in request body")
        return JsonResponse({"status": "ERR", "message": "Invalid JSON in request body"}, status=400)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        return JsonResponse({"status": "ERR", "message": "Internal server error"}, status=500)

@csrf_exempt
@require_GET
def health(request):
    return JsonResponse({"status": "OK"})

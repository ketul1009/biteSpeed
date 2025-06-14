from identify.models import Contact
from django.db.models import Q
from typing import List

def get_primary_contacts(email: str, phoneNumber: str) -> List[Contact]:
    primary_contacts = Contact.objects.filter(Q(email=email) | Q(phoneNumber=phoneNumber), linkPrecedence='primary')
    return primary_contacts
    
def check_if_contact_exists(email: str, phoneNumber: str) -> bool:
    return Contact.objects.filter(Q(email=email) & Q(phoneNumber=phoneNumber)).exists()
    
def get_secondary_contacts(contact: Contact) -> List[Contact]:
    return Contact.objects.filter(linkedId=contact.id, linkPrecedence='secondary')

def get_consolidated_contact(contact: Contact) -> dict:
    if contact.linkPrecedence != 'primary':
        primary = contact.linkedId
    else:
        primary = contact
    secondary_contacts = get_secondary_contacts(primary)
    emails = {primary.email} if primary.email else set()
    phoneNumbers = {primary.phoneNumber} if primary.phoneNumber else set()
    for secondary_contact in secondary_contacts:
        if secondary_contact.email:
            emails.add(secondary_contact.email)
        if secondary_contact.phoneNumber:
            phoneNumbers.add(secondary_contact.phoneNumber)
    secondaryContactIds = [contact.id for contact in secondary_contacts]
    return {
        "primaryContactId": primary.id,
        "emails": list(emails),
        "phoneNumbers": list(phoneNumbers),
        "secondaryContactIds": secondaryContactIds
    }

def create_contact(email: str, phoneNumber: str, linkPrecedence: str, linkedId: Contact = None) -> Contact:
    return Contact.objects.create(email=email, phoneNumber=phoneNumber, linkPrecedence=linkPrecedence, linkedId=linkedId)

def update_primary_contact(contact: Contact, linkedId: Contact) -> Contact:
    contact.linkPrecedence = 'secondary'
    contact.linkedId = linkedId
    contact.save()
    return contact

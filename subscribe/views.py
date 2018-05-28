from django.http import request
from django_twilio.decorators import twilio_view
from django_twilio.request import decompose
from twilio.twiml.messaging_response import MessagingResponse
from .models import Contacts

@twilio_view
def sms_choice(request):
    twilio_request = decompose(request)
    contact_num = twilio_request.from_
    response = twilio_request.body
    contact_info = ['Thanks for your subscription',
                    "How old are you?", "Annual Income?"]
    resp = MessagingResponse()
    contact, created = Contacts.objects.get_or_create(customer_number=contact_num)
    if created:
        resp.message(contact_info[0])
    else:
        resp.message(contact_info[1])
    print(contact_num, response)
    return resp

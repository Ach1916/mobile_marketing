from django.http import request
from django_twilio.decorators import twilio_view
from django_twilio.request import decompose, TwilioRequest
from .models import Doctors_list
from twilio.twiml.messaging_response import MessagingResponse
# Create your views here


@twilio_view
def subscription(request):
    decompose(request)

    contact_number = str(TwilioRequest.__class__('from_'))
    Doctors_list.append(contact_number)
    resp = MessagingResponse()
    resp.message('Peace God',)
    return str(resp)


print(Doctors_list)
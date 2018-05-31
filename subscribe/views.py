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
    resp = MessagingResponse()
    contact_info = ['Thanks for your subscription, How old are you?',
                    'What is your annual income?',
                    'Do you have a vehicle?']

    # 'Create Contacts instance'
    contact, created = Contacts.objects.get_or_create(customer_number=contact_num)

    # 'Send and record last sent sms'

    if created:
        resp.message(contact_info[0])
        contact.last_sms = '0'
        contact.save()

    elif not created:
        if contact.last_sms == '0':
            resp.message(contact_info[1])
            contact.last_sms = '1'
            contact.save()

        elif contact.last_sms == '1':
                resp.message(contact_info[2])
                contact.last_sms = '2'
                contact.save()

    else:
        resp.message('No record found')

    print(contact_num, response)
    return resp

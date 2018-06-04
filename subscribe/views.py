from django.http import request
from django_twilio.decorators import twilio_view
from django_twilio.request import decompose
from twilio.twiml.messaging_response import MessagingResponse
from .models import Contacts

@twilio_view
def sms_choices(request):
    twilio_request = decompose(request)
    contact_num = twilio_request.from_
    response = twilio_request.body
    resp = MessagingResponse()
    contact_info = ['Thanks for your subscription, What is your age?',
                    'What is your annual income?',
                    'Do you have a vehicle?',
                    'Is your car insured?',
                    'Does your whole family have medical insurance?',
                    'Does your household have dental insurance?',

                    ]

    # 'Create Contacts object'
    contact, created = Contacts.objects.get_or_create(customer_number=contact_num)

    # 'Send and record last sent sms'

    if created:
        resp.message(contact_info[0])
        contact.last_sms = '0'
        contact.save()

    # 'Contact age parameter'

    elif not created:
        if contact.last_sms == '0':
            if response.isnumeric() is True:
                contact.customer_age = response
                resp.message(contact_info[1])
                contact.last_sms = '1'
                contact.save()

            elif response.isnumeric() is False:
                resp.message('Tell me your age using only numbers')
                contact.last_sms = '0'
                contact.save()

    # 'Contact annual income parameter'

        elif contact.last_sms == '1':
            if response.isnumeric() is True:
                contact.customer_income = response
                resp.message(contact_info[2])
                contact.last_sms = '2'
                contact.save()

            elif response.isnumeric() is False:
                resp.message('Give me an estimate of your annual income using only numbers')
                contact.last_sms = '1'
                contact.save()

    # 'Contact car parameter'

        elif contact.last_sms == '2':
            if response.lower() == 'yes':
                contact.has_car = True
                resp.message(contact_info[3])
                contact.last_sms = '3'
                contact.save()

            elif response.lower() == 'no':
                contact.has_car = False
                resp.message(contact_info[4])
                contact.last_sms = '4'
                contact.save()

            else:
                resp.message('Please respond with yes or no')
                contact.last_sms = '2'
                contact.save()

    # 'Contact car insurance parameter'

        elif contact.last_sms == '3':
                if response.lower() == 'no':
                    contact.car_insurance = False
                    resp.message(contact_info[4])
                    contact.last_sms = '4'
                    contact.save()

                elif response.lower() == 'yes':
                    contact.car_insurance = True
                    resp.message(contact_info[4])
                    contact.last_sms = '4'
                    contact.save()

                else:
                    resp.message('Please respond with yes or no')
                    contact.last_sms = '3'
                    contact.save()

    # 'Contact med_insurance parameter'

        elif contact.last_sms == '4':
            if response.lower() == 'no':
                contact.med_insurance = False
                resp.message(contact_info[5])
                contact.last_sms = '5'
                contact.save()

            elif response.lower() == 'yes':
                contact.med_insurance = True
                resp.message(contact_info[5])
                contact.last_sms = '5'
                contact.save()

            else:
                resp.message('Please respond with yes or no')
                contact.last_sms = '4'
                contact.save()

    # 'Contact dental_insurance parameter'

        elif contact.last_sms == '5':
            if response.lower() == 'no':
                contact.dental_insurance = False
                contact.last_sms = '6'
                resp.message('Thank you for participation. As more services become available, we will be in touch')
                contact.save()

            elif response.lower() == 'yes':
                contact.dental_insurance = True
                contact.last_sms = '6'
                resp.message('Thank you for participation. As more services become available, we will be in touch')
                contact.save()

            else:
                resp.message('Please respond with yes or now')
                contact.last_sms = '5'
                contact.save()

        elif contact.last_sms == '6':
            resp.message('Thank you for participation. As more services become available, we will be in touch')
            contact.save()

# 'If a number isn't in the database and server cant create object'

    else:
        resp.message("Our apologizes, your number isn't registered. "
                     "Please visit www.Glpsmemphis.com to register")

    print(contact_num, contact.last_sms, response)
    return resp

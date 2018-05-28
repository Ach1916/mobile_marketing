from django.db import models


class Contacts (models.Model):
    customer_number = models.CharField(max_length=15)
    customer_age = models.CharField(max_length=4,
                                    null=True)
    customer_income = models.CharField(max_length=10,
                                       null=True)

    def __unicode__(self):
        return self.customer_number

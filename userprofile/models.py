from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Profile(models.Model):
	
	user = models.OneToOneField(User)
	name = models.CharField(max_length=100, blank=True, verbose_name="Name", db_index=True)
	secret = models.CharField(max_length=100, blank=True, verbose_name="Secret Key", db_index=True)

	skills = models.CharField(max_length=512, blank=True, verbose_name="skills", db_index=True)
	country = models.CharField(max_length=10, blank=True, verbose_name="country", db_index=True)
	language = models.CharField(max_length=10, blank=True, verbose_name="language", db_index=True)

	picture = models.URLField(blank=True, verbose_name="User Avatar / Company Logo")
	twitter = models.CharField(max_length=75, blank=True)

	mobile = models.CharField(max_length=20, blank=True, verbose_name="mobile_number_1")
	
	street_address_1 = models.CharField(max_length=100, blank=True, verbose_name="street_address_1")
	street_address_2 = models.CharField(max_length=100, blank=True, verbose_name="street_address_2")
	street_address_3 = models.CharField(max_length=100, blank=True, verbose_name="street_address_3")

	email_notfications = models.BooleanField(default=True)
	twitter_notifications = models.BooleanField(default=False)
	
	first_login = models.BooleanField(default=False)
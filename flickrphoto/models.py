from django.db import models

class UserData(models.Model):
	search_key = models.CharField(max_length=250)
	user_ip = models.GenericIPAddressField()

	def __str__(self):
		return self.search_key
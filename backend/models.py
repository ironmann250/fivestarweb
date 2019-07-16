from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.
#ACCOUNT phone, pwd}USER, name, pin, address
#SEARCH usertype, keyword
#STATUS user,code,action
#PACKAGE sendername, senderphone, receivername, receiverphone, destination, receiver, weight, packagenum, status

class ACCOUNT(models.Model):
	user=models.ForeignKey(User)
	name=models.TextField()
	pin=models.TextField() #only 6 chars
	address=models.TextField()

	def __str__(self):
		return self.name

class SEARCH(models.Model):
	isregistered=models.BooleanField(default=False)
	keyword=models.TextField()
	creation_date=models.DateTimeField(now())
	def __str__(self):
		return self.keyword

class STATUS(models.Model):
	user=models.ForeignKey(User)
	code=models.IntegerField()
	action=models.TextField()

	def __str__(self):
		return self.action

class PAYMENT_HOLDER(models.Model):
	isfilled=models.BooleanField(default=False)
	status=models.ForeignKey(STATUS)#package paid 1
	creation_date=models.DateTimeField(now())
	weight=models.IntegerField()
	price=models.IntegerField()
	method=models.TextField()#option: cash, bank, wechat, alipay

	def __str__(self):
		return str(self.weight)+" - "+str(self.price)

class DEPARTURE_HOLDER(models.Model):
	isfilled=models.BooleanField(default=False)
	status=models.ForeignKey(STATUS)#package departed 2
	creation_date=models.DateTimeField(now())
	expected_date=models.TextField()#transform in datetime filed later
	terminal=models.TextField() #airport: name and address

	def __str__(self):
		return "from: "+self.terminal+" arrive: "+str(self.expected_date)

class ARRIVED_HOLDER(models.Model):
	isfilled=models.BooleanField(default=False)
	status=models.ForeignKey(STATUS)#package arrived 3
	creation_date=models.DateTimeField(now())
	arrival_date=models.TextField()#transform in datetime filed later

	def __str__(self):
		return "arrived at: "+str(self.arrival_date)

class PICKUP_HOLDER(models.Model):
	isfilled=models.BooleanField(default=False)
	status=models.ForeignKey(STATUS)#package picked up 4
	creation_date=models.DateTimeField(now())


	def __str__(self):
		return "picked at: "+str(self.date)

class PACKAGE(models.Model):
	sender_name=models.TextField()
	sender_phone=models.TextField()
	receiver_name=models.TextField()
	receiver_phone=models.TextField()
	destination=models.TextField()
	init_weight=models.IntegerField()
	init_price=models.IntegerField()
	description=models.TextField()
	packagenum=models.TextField()#create pin
	creation_date=models.DateTimeField(now())
	payment_stat=models.ForeignKey(PAYMENT_HOLDER, blank=True, null=True)
	departure_stat=models.ForeignKey(DEPARTURE_HOLDER, blank=True, null=True)
	arrived_stat=models.ForeignKey(ARRIVED_HOLDER, blank=True, null=True)
	pickup_stat=models.ForeignKey(PICKUP_HOLDER, blank=True, null=True)
	status=models.ForeignKey(STATUS) #package created 0

	def __str__(self):
		return self.packagenum

class PACKAGETEST(models.Model):
	creation_date=models.DateTimeField(now())
	payment_stat=models.ForeignKey(PAYMENT_HOLDER, blank=True, null=True)

	def __str__(self):
		return str(self.creation_date)
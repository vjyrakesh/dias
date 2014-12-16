from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class DoctorDetailsManager(models.Manager):
	def get_all_specialities(self):
		return super(DoctorDetailsManager,self).get_query_set().values_list('specialization')

class Doctor(models.Model):
	qualification = models.CharField(max_length=20)
	specialization = models.CharField(max_length=20)
	years_of_experience = models.IntegerField()
	months_of_experience = models.IntegerField()
	address = models.CharField(max_length=500)
	phone_number = models.CharField(max_length=15)
	associations = models.CharField(max_length=200,blank=True)
	user = models.OneToOneField(User)
	objects = DoctorDetailsManager()

	def __unicode__(self):
		return self.user.first_name + " " + self.user.last_name

	def get_user_name(self):
		return self.user.username

	def get_absolute_url(self):
		return "/doctor/%s.%s" %(self.user.first_name,self.user.last_name)



class Patient(models.Model):
	phone_number = models.CharField(max_length=15)
	locality = models.CharField(max_length=50)
	user = models.OneToOneField(User)

	def __unicode__(self):
		return self.user.first_name + " " + self.user.last_name

	def get_user_name(self):
		return self.user.username

class Appointment(models.Model):
	apDate = models.DateField()
	apTime = models.TimeField()
	doctor = models.ForeignKey(Doctor)
	patient = models.ForeignKey(Patient)
	status = models.CharField(max_length=20)



class Slot(models.Model):
	week_day = models.CharField(max_length=10)
	begin_time = models.TimeField()
	end_time = models.TimeField()
	doctor = models.ForeignKey(Doctor)

class SlotModification(models.Model):
	mod_date = models.DateField()
	mod_slot_begin_time = models.TimeField()
	mod_slot_end_time = models.TimeField()
	doctor = models.ForeignKey(Doctor)

def get_ap_date(Appointment):
		return Appointment.apDate



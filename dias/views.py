import datetime
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User,Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password

from dias.models import Doctor,Patient,Appointment,get_ap_date
from dias.forms import PatientRegistrationForm,DivErrorList
from dias.utils import *

# Need to externalize this
slotQuantum = 15

def setSessionVariables(request):
	grp = Group.objects.filter(user=User.objects.get(pk=7))[0]
	request.session['site_user_fname'] = request.user.first_name
	request.session['usr_grp'] = str(grp.id)

#@login_required(login_url="/login/")
def home(request):
	if 'next' in request.GET:
		print request.GET['next']
	else:
		print 'next not available'
	if request.user and len(User.objects.filter(username=request.user.username))>0:
		site_user = request.user
		setSessionVariables(request)
	return render(request,'home.html',{'specialities':get_specialities_list()})
	
def get_specialities_list():
	sl = Doctor.objects.get_all_specialities()
	spl_list = [spl[0] for spl in sl]
	return spl_list

@login_required(login_url="/login/")
def doctors(request):
	if request.method == 'POST':
		#print 'specialization selected: ' + request.POST['selSpl']
		dl = Doctor.objects.filter(specialization__icontains=request.POST['selSpl'])
		return render(request,"doctors_list.html",{'spl_name':request.POST['selSpl'], 'doctors':dl})
	return render(request,'home.html',{'specialities':get_specialities_list()})

@login_required(login_url="/login/")
def doctor_profile(request,firstname,lastname):
	#print "profile for: " + firstname + " " + lastname
	doc = Doctor.objects.get(user=User.objects.get(first_name=firstname,last_name=lastname))
	slots = doc.slot_set.all()
	ord_slots = sort_days(slots)
	merged_slots_dict = merge_slots(ord_slots)
	return render(request,'doctor_profile.html',{'doc':doc,'slots_dict':merged_slots_dict})

@login_required(login_url="/login/")
def make_appointment(request,firstname,lastname):
	doc = Doctor.objects.get(user=User.objects.get(first_name=firstname,last_name=lastname))
	slots = doc.slot_set.all()
	ord_slots = sort_days(slots)
	merged_slots_dict = merge_slots(ord_slots)
	slotHours = []
	slotMins = []
	selDate = ''
	avlSlotTimeObjs = []
	if request.method == "GET":
		if 'date' in request.GET:
			selDate = request.GET['date']
			selDay = selDate[0:selDate.find(",")].lower()
			slotHours = get_slot_hours(merged_slots_dict[selDay])
			slotMins = [i*15 for i in range(0,4)]
			slotTimeObjs = []
			for oneSlotHour in slotHours:
				for oneSlotMin in slotMins:
					slotTimeObjs.append(datetime.time(oneSlotHour,oneSlotMin))
			sepIdx = selDate.find(",")
			slotDate = selDate[sepIdx+2:]
			dt = datetime.datetime.strptime(slotDate,"%d/%m/%Y").date()
			apLst = Appointment.objects.filter(apDate=dt,doctor=doc)
			apTmLst = [a.apTime for a in apLst]
			apTmLstUnq = list(set(apTmLst))
			apTm_navl = []
			for apTm in apTmLstUnq:
				if apTmLst.count(apTm) > 1:
					apTm_navl.append(apTm)
					print apTm
			avlSlotTimeObjs = [item for item in slotTimeObjs if item not in apTm_navl]
	return render(request,'doctor_appointment.html',{'doc':doc,'avlSlotTimes':avlSlotTimeObjs,'selDate':selDate})

@login_required(login_url="/login/")
def confirm_appointment(request,action):
	if request.method == "POST":
		if action == 'book':
			docFirstName = request.POST['docFirstName']
			docLastName = request.POST['docLastName']
			sepIdx = request.POST['selDate'].find(",")
			slotDate = request.POST['selDate'][sepIdx+2:]
			slDate = datetime.datetime.strptime(slotDate,'%d/%m/%Y').date()
			slotTime = datetime.datetime.strptime(request.POST['slotHour'],"%H:%M").time()
			doc = Doctor.objects.get(user=User.objects.get(first_name=docFirstName,last_name=docLastName))
			p = Patient.objects.get(user=request.user)
			ap = Appointment(apDate=slDate,apTime=slotTime,doctor=doc,patient=p)
			ap.save()
		elif action == 'cancel':
			ap = Appointment.objects.get(id=int(request.POST['apid']))
		return render(request,"confirm_appointment.html",{'ap':ap,'action':action})

@login_required(login_url="/login/")
def book_appointment(request):
	if request.method == 'POST':
		Appointment.objects.filter(id=int(request.POST['apid'])).update(status="confirmed")
		return render(request,"appointment_status.html",{'message':'Your appointment has been confirmed.'})

@login_required(login_url="/login/")
def cancel_appointment(request):
	if request.method == 'POST':
		Appointment.objects.filter(id=int(request.POST['apid'])).update(status="canceled")
		return render(request,"appointment_status.html",{'message':'Your appointment has been canceled.'})

@login_required(login_url="/login/")
def appointments_home(request):
	p = Patient.objects.get(user=request.user)
	al = p.appointment_set.all()
	return render(request,"appointments_home.html",{'user':p.user, 'al':al})

@login_required(login_url="/login/")
def appointments_home_doc(request):
	d = Doctor.objects.get(user=request.user)
	al = d.appointment_set.all()
	past_aps = []
	upcoming_aps = []
	today_dt = datetime.datetime.now().date()
	for ap in al:
		#ap_dt = datetime.datetime.strptime(ap.apDate,"%Y-%m-%d").date()
		if ap.apDate < today_dt:
			past_aps.append(ap)
		else:
			upcoming_aps.append(ap)
	return render(request,"appointments_home_doc.html",{'user':d.user, 'past_aps':sorted(past_aps,key=get_ap_date),'upcoming_aps':sorted(upcoming_aps,key=get_ap_date)})

def site_login(request):
	if request.method == 'POST':
		if request.POST['un'] and request.POST['pd']:
			username = request.POST['un']
			password = request.POST['pd']
			print 'username:' + username + ',password:' + password
			user = authenticate(username=username,password=password)
			print 'user:' + user.first_name
			if user and user.is_active:
				login(request,user)
				grp = Group.objects.get(user=user)
				setSessionVariables(request)
				if grp.name == 'Doctor':
					return HttpResponseRedirect("/appointments/doctor/")
				elif grp.name == 'Patient':
					return HttpResponseRedirect("/home/")
			else:
				return render(request,"login_form.html",{'message':'Invalid username or password'})
		else:
			return render(request,"login_form.html",{'message':'Please provide username and password'})
	else:
		return render(request,"login_form.html",{'message':''})

@login_required(login_url="/login/")
def site_logout(request):
	if request.user.is_authenticated():
		logout(request)
		return render(request,"logged_out.html")
	else:
		return render(request,"login_form.html")

def site_signup(request):
	if request.method == 'POST':
		form = PatientRegistrationForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			uname = cd['username']
			pword = cd['password']
			firstname = cd['firstname']
			lastname = cd['lastname']
			email = cd['emailid']
			mobNum = cd['mobNum']
			locality = cd['locality']
			user = User(username=uname,password=make_password(pword),first_name=firstname,last_name=lastname,email=email)
			user.backend='django.contrib.auth.backends.ModelBackend'
			user.save()
			usr = User.objects.get(username=uname)

			if usr:
				pat = Patient(phone_number=mobNum,locality=locality,user=usr)
				pat.save()
				usr.groups.add(Group.objects.get(name='Patient'))
				#usr = authenticate(username=uname,password=pword)
				login(request,user)
				request.session['new_un'] = uname
				#return HttpResponseRedirect("/signupsuccess/")
				return HttpResponseRedirect("/home/")
	else:
		form = PatientRegistrationForm(error_class=DivErrorList)
	return render(request,"signup_patient.html",{'form':form})

def signup_success(request):
	if request.session['new_un']:
		print request.session['new_un']
		uname = request.session['new_un']
		user = User.objects.get(username=uname)
		if user:
			print user.password
			usr = authenticate(username=uname,password=user.password)
			login(request,usr)
	return render(request,"signup_success.html")


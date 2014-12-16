from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'dias.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^home/$','dias.views.home'),
    url(r'^login/$','dias.views.site_login'),
    url(r'^logout/$','dias.views.site_logout'),
    url(r'^doctors/$','dias.views.doctors'),
    url(r'^doctor/(?P<firstname>\w+)\.(?P<lastname>\w+)$','dias.views.doctor_profile'),
    url(r'^appointment/(?P<firstname>\w+)\.(?P<lastname>\w+)$','dias.views.make_appointment'),
    url(r'^appointment/book/confirm/$','dias.views.confirm_appointment',{'action':'book'}),
    url(r'^appointment/book/$','dias.views.book_appointment'),
    url(r'^appointments/$','dias.views.appointments_home'),
    url(r'^appointments/doctor/$','dias.views.appointments_home_doc'),
    url(r'^appointment/cancel/confirm/$','dias.views.confirm_appointment',{'action':'cancel'}),
    url(r'^appointment/cancel/$','dias.views.cancel_appointment'),
)

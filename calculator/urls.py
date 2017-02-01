from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.test_profile_settings, name='test_profile_settings'),
    url(r'^formset/$', views.test_profile_settings, name='test_profile_settings'),
    url(r'^calculateresult/(?P<distance_pred>.+)/(?P<gender>.+)/(?P<distance1>.+)/(?P<time1>.+)/(?P<distance2>.+)/(?P<time2>.+)/(?P<distance3>.+)/(?P<time3>.+)/', 
            views.calculateresult, name='calculateresult'),
    url(r'^formset/calculateresult/(?P<distance_pred>.+)/(?P<gender>.+)/(?P<distance1>.+)/(?P<time1>.+)/(?P<distance2>.+)/(?P<time2>.+)/(?P<distance3>.+)/(?P<time3>.+)/', 
            views.calculateresult, name='calculateresult'),
    url(r'^formset/threenumbersummary/(?P<t0>.+)/(?P<t1>.+)/(?P<t2>.+)/(?P<t3>.+)/(?P<t4>.+)/(?P<t5>.+)/(?P<t6>.+)/(?P<t7>.+)/(?P<t8>.+)/(?P<t9>.+)/', 
            views.threenumbersummary, name='threenumbersummary'),
    url(r'^threenumbersummary/(?P<t0>.+)/(?P<t1>.+)/(?P<t2>.+)/(?P<t3>.+)/(?P<t4>.+)/(?P<t5>.+)/(?P<t6>.+)/(?P<t7>.+)/(?P<t8>.+)/(?P<t9>.+)/', 
            views.threenumbersummary, name='threenumbersummary'),
    url(r'^weights.csv$', views.get_weights, name='get_weights'),
]

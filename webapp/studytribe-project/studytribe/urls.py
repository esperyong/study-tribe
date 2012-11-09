from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'studytribe.views.home', name='home'),
    # url(r'^studytribe/', include('studytribe.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', 
        include('rest_framework.urls', namespace='rest_framework')),
    url(r'^', include('studytribe.studygroup.urls')),
    url(r'^', include('studytribe.studyfootmark.urls')),
    url(r'^', include('studytribe.studycalendar.urls')),
    url(r'^', include('studytribe.everythings.urls')),
    url(r'^', include('studytribe.tribemember.urls')),
    #url(r'^', include('studytribe.tribemember.urls')),

)


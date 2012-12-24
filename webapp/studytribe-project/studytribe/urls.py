from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', 
        include('rest_framework.urls', namespace='rest_framework')),
    url(r'^', include('studytribe.studygroup.urls')),
    url(r'^', include('studytribe.studyfootmark.urls')),
    url(r'^', include('studytribe.studycalendar.urls')),
    url(r'^', include('studytribe.everythings.urls')),
    url(r'^', include('studytribe.tribemember.urls')),

)


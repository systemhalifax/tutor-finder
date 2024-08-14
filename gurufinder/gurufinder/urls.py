"""gurufinder URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django_email_verification import urls as email_urls
from accounts import views as accounts_views
from accounts.views import TutorListView, TutorDetailView, BookingView, SearchTutorLanguage #ApplicationView,

urlpatterns = [
    path('', accounts_views.index, name='index'),
    path('about/', accounts_views.about, name='about'),
    path('how-it-works/', accounts_views.how_it_works, name='how_it_works'),
    path('start-tutoring/', accounts_views.tutor_application, name='application'),
    path('search-for-tutors/', TutorListView.as_view(), name='tutor_list'),
    path('search-for-tutors/search-language/', SearchTutorLanguage.as_view(), name='search_language'),
    path('search-for-tutors/<int:pk>/', TutorDetailView.as_view(), name='tutor_detail'),
    path('search-for-tutors/<int:pk>/book/', BookingView.as_view(), name='booking'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('courses/', include('classroom.urls')),
    path('accounts/', include('accounts.urls')),
    path('messages/', include('direct.urls')),
    path('admin/', admin.site.urls),
    path('email/', include(email_urls)),
    path('ratings/', include('star_ratings.urls', namespace='ratings')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


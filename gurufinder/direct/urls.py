from django.urls import path, include
from . import views

app_name = 'direct'
urlpatterns = [
    path('', views.inbox, name='inbox'),
    path('message/<username>', views.directs, name='message'),
    path('send/', views.send_direct, name='send_direct'),
    path('new/', views.user_search, name='usersearch'),
    path('new/<username>', views.new_conversation, name='newconversation'),
]
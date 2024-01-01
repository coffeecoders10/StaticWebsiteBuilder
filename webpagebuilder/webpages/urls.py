
from django.urls import path
from . import views

urlpatterns = [
    path('',views.login,name='login'),
    path('editor',views.editor,name='editor'),
    path('webpage',views.webpage,name='webpage')
]

from django.conf.urls import url, include
from django.urls import path
from .views import HelloWorldView, OptionDataView, FindCondors,\
    FindCallCredit, FindCallDebit, FindPutDebit, FindPutCredit


urlpatterns = [
    url('hello/', HelloWorldView.as_view()),


    path('get_option_data/<str:ticker>/', OptionDataView.as_view()),

    path('condors/', FindCondors.as_view()),


    path('callcredit/', FindCallCredit.as_view()),


    path('calldebit/', FindCallDebit.as_view()),


    path('putdebit/', FindPutDebit.as_view()),

    path('putcredit/', FindPutCredit.as_view())



]
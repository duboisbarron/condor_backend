from django.conf.urls import url, include
from django.urls import path
from .views import HelloWorldView, OptionDataView, FindCondors


urlpatterns = [
    url('hello/', HelloWorldView.as_view()),


    path('get_option_data/<str:ticker>/', OptionDataView.as_view()),

    path('condors/', FindCondors.as_view()),

]
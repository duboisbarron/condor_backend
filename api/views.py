from django.shortcuts import render
from rest_framework.response import Response
from .td_api import TD_API
from rest_framework.generics import RetrieveAPIView
from .IronCondorClass import IronCondor
# Create your views here.



class HelloWorldView(RetrieveAPIView):


    def get(self, request, *args, **kwargs):

        return Response({
            'message': 'hello world!'
        })



class OptionDataView(RetrieveAPIView):

    def get(self, request, *args, **kwargs):

        print(args)
        print(kwargs)
        ticker = kwargs['ticker']

        td_obj = TD_API()

        data = td_obj.get_current_price_and_expirations(ticker)
        print(data)

        return Response(data=data)


class FindCondors(RetrieveAPIView):
    def get(self, request, *args, **kwargs):

        ticker = request.query_params['ticker']
        expiration = request.query_params['expiration']

        td_obj = TD_API()


        condors = td_obj.get_condors(ticker, expiration)
        print('found {} valid iron condor configurations'.format(len(condors)))

        # condor1 = IronCondor(6, 7, 15, 20, 0.01, 0.5, 0.3, 0.1)
        # condor2 = IronCondor(4, 5, 30, 40, 0.1, 0.5, 0.2, 0.1)
        # condor_list = [condor1, condor2]

        serialized_data = []
        for index, condor in enumerate(condors):
            try:
                serialized_data.append(condor.serialize(id))
            except Exception as e:
                print(e)
                print(condor)
                continue


        #
        # data = condor.serialize()

        return Response(data=serialized_data)

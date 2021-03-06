from django.shortcuts import render
from rest_framework.response import Response
from .td_api import TD_API
from rest_framework.generics import RetrieveAPIView



class FindPutCredit(RetrieveAPIView):

    def get(self, request, *args, **kwargs):

        ticker = request.query_params['ticker']
        expiration = request.query_params['expiration']

        td_obj = TD_API()

        put_credit_spreads = td_obj.get_put_credit_spreads(ticker, expiration)

        serialized_data = []
        for index, spread in enumerate(put_credit_spreads):
            try:
                serialized_data.append(spread.serialize(index))
            except Exception as e:
                continue

        return Response(data=serialized_data)

class FindPutDebit(RetrieveAPIView):

    def get(self, request, *args, **kwargs):

        ticker = request.query_params['ticker']
        expiration = request.query_params['expiration']

        td_obj = TD_API()

        put_debit_spreads = td_obj.get_put_debit_spreads(ticker, expiration)

        serialized_data = []
        for index, spread in enumerate(put_debit_spreads):
            try:
                serialized_data.append(spread.serialize(index))
            except Exception as e:
                continue

        return Response(data=serialized_data)


class FindCallDebit(RetrieveAPIView):

    def get(self, request, *args, **kwargs):
        ticker = request.query_params['ticker']
        expiration = request.query_params['expiration']

        td_obj = TD_API()

        call_debit_spreads = td_obj.get_call_debit_spreads(ticker, expiration)

        serialized_data = []
        for index, spread in enumerate(call_debit_spreads):
            try:
                serialized_data.append(spread.serialize(index))
            except Exception as e:
                continue

        return Response(data=serialized_data)





class FindCallCredit(RetrieveAPIView):
    def get(self, request, *args, **kwargs):

        ticker = request.query_params['ticker']
        expiration = request.query_params['expiration']

        td_obj = TD_API()

        call_credit_spreads = td_obj.get_call_credit_spreads(ticker, expiration)

        serialized_data = []
        for index, spread in enumerate(call_credit_spreads):
            try:
                serialized_data.append(spread.serialize(index))
            except Exception as e:
                continue

        return Response(data=serialized_data)


class HelloWorldView(RetrieveAPIView):


    def get(self, request, *args, **kwargs):



        return Response({
            'message': 'hello world!'
        })



class OptionDataView(RetrieveAPIView):

    def get(self, request, *args, **kwargs):

        ticker = kwargs['ticker']

        td_obj = TD_API()

        data = td_obj.get_current_price_and_expirations(ticker)

        return Response(data=data)


class FindCondors(RetrieveAPIView):
    def get(self, request, *args, **kwargs):

        ticker = request.query_params['ticker']
        expiration = request.query_params['expiration']

        td_obj = TD_API()


        condors = td_obj.get_condors(ticker, expiration)


        serialized_data = []
        for index, condor in enumerate(condors):
            try:
                serialized_data.append(condor.serialize(index))
            except Exception as e:
                # print(e)
                # print(condor)
                continue


        #
        # data = condor.serialize()

        return Response(data=serialized_data)

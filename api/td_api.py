import requests
import time
from .IronCondorClass import IronCondor
from .CallCreditClass import CallCredit
import os


class TD_API:
    user_id = os.environ['td_key']
    url = 'https://api.tdameritrade.com/v1/marketdata/chains'

    def get_current_price_and_expirations(self, ticker):
        params = {
            'apikey': self.user_id,
            'symbol': ticker,
            'contractType': 'ALL'
        }
        response = requests.get(url=self.url, params=params).json()

        resp_obj = {
            'current_share_price': round(float(response['underlyingPrice']), 2),
            'expiration_dates': list(response['callExpDateMap'].keys())
        }
        return resp_obj

    def get_put_legs(self, data):
        # print(data)
        put_legs = []

        '''
        go through option chain constructing put legs 
        one after another to minimize the leg width 
        
        
        example:
        
        option chain strike prices (75, 80, 85, 90)
        
        construct legs: (75, 80), (80, 85), (85, 90)
        '''
        strike_prices = list(data.keys())
        num_strikes = len(strike_prices)

        # want buy_put strike price to be < write_put strike price
        buy_put_index = 0
        write_put_index = 1

        while write_put_index < num_strikes:

            buy_put_strike_price = strike_prices[buy_put_index]
            write_put_strike_price = strike_prices[write_put_index]

            # pop out the mark prices (mark = midpoint of bid and ask)
            mark_price_buy_put = data[buy_put_strike_price][0]['mark']
            mark_price_write_put = data[write_put_strike_price][0]['mark']

            bid_ask_str_WRITE = abs(data[write_put_strike_price][0]['bid'] - data[write_put_strike_price][0]['ask'])
            bid_ask_str_BUY = abs(data[buy_put_strike_price][0]['bid'] - data[buy_put_strike_price][0]['ask'])

            put_leg = {
                'buy_put': float(buy_put_strike_price),
                'write_put': float(write_put_strike_price),
                'buy_put_premium': float(mark_price_buy_put),
                'write_put_premium': float(mark_price_write_put),
                'buy_put_BA': bid_ask_str_BUY,
                'write_put_BA': bid_ask_str_WRITE
            }

            put_legs.append(put_leg)

            buy_put_index += 1
            write_put_index += 1
        # end while
        return put_legs

    def get_call_legs(self, data):
        call_legs = []

        '''
        go through option chain constructing call legs 
        one after another to minimize the leg width 

        example:

        option chain strike prices (75, 80, 85, 90)

        construct legs: (75, 80), (80, 85), (85, 90)
        
        ignore the possible/valid leg (75, 85) as this increases potential loss
        '''

        strike_prices = list(data.keys())
        num_strikes = len(strike_prices)

        # print(num_strikes)
        # want write_call strike price to be < buy_call strike price
        write_call_index = 0
        buy_call_index = 1
        while buy_call_index < num_strikes:

            # get the strike price of our buy and write
            write_call_strike_price = strike_prices[write_call_index]
            buy_call_strike_price = strike_prices[buy_call_index]

            mark_price_write_call = data[write_call_strike_price][0]['mark']
            mark_price_buy_call = data[buy_call_strike_price][0]['mark']

            bid_ask_str_WRITE = abs(data[write_call_strike_price][0]['bid'] - data[write_call_strike_price][0]['ask'])
            bid_ask_str_BUY = abs(data[buy_call_strike_price][0]['bid'] - data[buy_call_strike_price][0]['ask'])

            # print(mark_price_write_call, mark_price_buy_call)

            call_leg = {
                'write_call': float(write_call_strike_price),
                'buy_call': float(buy_call_strike_price),
                'write_call_premium': float(mark_price_write_call),
                'buy_call_premium': float(mark_price_buy_call),
                'buy_call_BA': bid_ask_str_BUY,
                'write_call_BA': bid_ask_str_WRITE
            }
            # print(call_leg['write_call'], call_leg['buy_call'])
            # print(call_leg['write_call_premium'], call_leg['buy_call_premium'])

            call_legs.append(call_leg)

            write_call_index += 1
            buy_call_index += 1

        # end while
        return call_legs

    def get_valid_condors(self, current_share_price, put_legs, call_legs):

        valid_condors = []


        # print(len(put_legs), len(call_legs))
        total_iterations = 0
        call_index = 0
        while call_index < len(call_legs):
            put_index = 0
            while put_index < len(put_legs):


                call_leg = call_legs[call_index]
                put_leg = put_legs[put_index]

                # attempt to construct an iron condor using these 2 legs
                try:
                    condor = IronCondor(
                        current_share_price=current_share_price,
                        buy_put=put_leg['buy_put'],
                        short_put=put_leg['write_put'],
                        short_call=call_leg['write_call'],
                        buy_call=call_leg['buy_call'],

                        bp_prem=put_leg['buy_put_premium'],
                        sp_prem=put_leg['write_put_premium'],
                        sc_prem=call_leg['write_call_premium'],
                        bc_prem=call_leg['buy_call_premium'],
                        bp_BA=put_leg['buy_put_BA'],
                        sp_BA=put_leg['write_put_BA'],
                        sc_BA=call_leg['write_call_BA'],
                        bc_BA=call_leg['buy_call_BA']
                    )
                    valid_condors.append(condor)
                except Exception as e:
                    # print(e)
                    # print('error occurred')
                    # print('this configuration invalid')
                    put_index += 1
                    total_iterations += 1
                    continue

                total_iterations += 1
                put_index += 1

            # end while
            call_index += 1
        # end while
        return valid_condors

    def get_condors(self, ticker, expiration):
        params = {
            'apikey': self.user_id,
            'symbol': ticker,
            'contractType': 'ALL'
        }
        response = requests.get(url=self.url, params=params)
        data = response.json()

        current_share_price = float(data['underlyingPrice'])


        # pop out the call and put contracts by expiration date
        put_data = data['putExpDateMap']
        call_data = data['callExpDateMap']
        set_of_put_contracts = put_data[expiration]
        set_of_call_contracts = call_data[expiration]

        # compute put legs running two indices through the puts
        put_legs = self.get_put_legs(set_of_put_contracts)

        # compute call legs running two indices through the calls
        call_legs = self.get_call_legs(set_of_call_contracts)

        valid_condors = self.get_valid_condors(current_share_price, put_legs, call_legs)

        return valid_condors



    def get_call_credit_spreads(self, ticker, expiration):
        params = {
            'apikey': self.user_id,
            'symbol': ticker,
            'contractType': 'ALL'
        }
        response = requests.get(url=self.url, params=params)
        data = response.json()

        current_share_price = float(data['underlyingPrice'])
        print(current_share_price)

        call_data = data['callExpDateMap']
        set_of_call_contracts = call_data[expiration]

        # print(set_of_call_contracts)
        good_keys = []
        for strike in set_of_call_contracts.keys():
            if float(strike) > current_share_price:
                good_keys.append(strike)


        print('current share price is: {}'.format(current_share_price))
        print(good_keys)

        valid_call_credit_spreads = []

        for index, short_strike in enumerate(good_keys):
            potential_long_strikes = good_keys[index + 1 ::]
            # print(short_strike)
            # print(potential_long_strikes)

            for long_strike in potential_long_strikes:


                try:


                    short_strike_premium = set_of_call_contracts[short_strike][0]['mark']
                    # print(set_of_call_contracts[short_strike])
                    # print(short_strike_premium)

                    long_strike_premium = set_of_call_contracts[long_strike][0]['mark']

                    bid_ask_str_WRITE = abs(set_of_call_contracts[short_strike][0]['bid'] - set_of_call_contracts[short_strike][0]['ask'])
                    bid_ask_str_BUY = abs(set_of_call_contracts[long_strike][0]['bid'] - set_of_call_contracts[long_strike][0]['ask'])


                    # print(short_strike_premium, long_strike_premium, bid_ask_str_WRITE, bid_ask_str_BUY)

                    callcreditObj = CallCredit(
                        current_share_price,
                        float(short_strike),
                        float(long_strike),
                        short_strike_premium,
                        long_strike_premium,
                        bid_ask_str_WRITE,
                        bid_ask_str_BUY
                    )

                    valid_call_credit_spreads.append(callcreditObj)


                except Exception as e:
                    # print(e)
                    # print('ERROR OCCURED')
                    continue
        return valid_call_credit_spreads


if __name__ == '__main__':
    td_api = TD_API()
    expiration_date = td_api.get_current_price_and_expirations('JNJ')['expiration_dates'][1]


    td_api.get_call_credit_spreads('AAPL', expiration_date)

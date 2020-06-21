
class IronCondor:


    def __init__(self, current_share_price, buy_put, short_put, short_call, buy_call, bp_prem, sp_prem, sc_prem, bc_prem, contract_size=100.0):

        assert buy_put < short_put < short_call < buy_call

        assert current_share_price < short_call
        assert current_share_price > short_put

        self.current_share_price = current_share_price

        self.buy_put = buy_put
        self.short_put = short_put
        self.short_call = short_call
        self.buy_call = buy_call

        self.bp_prem = bp_prem
        self.sp_prem = sp_prem
        self.sc_prem = sc_prem
        self.bc_prem = bc_prem

        self.contract_size = contract_size

    def __str__(self):
        return 'Buy Put @ ${} Strike for ${} \nWrite Put @ ${} Strike for ${} \nWrite Call @ ${} Strike for ${} \nBuy Call @ ${} Strike for ${}'.format(self.buy_put, self.bp_prem, self.short_put, self.sp_prem, self.short_call, self.sc_prem, self.buy_call, self.bp_prem)

    def is_even_winged(self):
        left_wing_width = round(self.short_put - self.buy_put, 3)
        right_wing_width = round(self.buy_call - self.short_call, 3)
        return left_wing_width == right_wing_width

    def initial_credit(self):
        return (self.sp_prem + self.sc_prem) - (self.bp_prem + self.bc_prem)

    def diff_call_strikes(self):
        return self.buy_call - self.short_call

    def diff_put_strikes(self):
        return self.short_put - self.buy_put

    def max_gain(self):
        return round(self.initial_credit() * 100.00, 2)

    def max_loss(self):
        greatest_diff = float(max(abs(self.diff_call_strikes()), abs(self.diff_put_strikes())))

        print(round((greatest_diff - self.initial_credit()) * 100.00, 2))
        return round((greatest_diff - self.initial_credit()) * 100.00, 2)

    def risk_reward_ratio(self):
        return self.max_gain() / abs(self.max_loss())

    def left_side_break_even(self):
        return self.short_call + self.initial_credit()

    def right_side_break_even(self):
        return self.short_put - self.initial_credit()

    def serialize(self):

        return {
            'buy_put': self.buy_put,
            'short_put': self.short_put,
            'current_share_price': round(self.current_share_price, 2),
            'short_call': self.short_call,
            'buy_call': self.buy_call,
            'buy_put_premium': self.bp_prem,
            'short_put_premium': self.sp_prem,
            'short_call_premium': self.sc_prem,
            'buy_call_premium': self.bc_prem,
            'max_gain': self.max_gain(),
            'max_loss': self.max_loss(),
            'risk_reward': round(self.risk_reward_ratio(), 2)
        }

if __name__ == '__main__':

    condor = IronCondor(13.0, 5.79, 10.79, 15.79, 20.79, 0.1, 0.5, 0.2, 0.1)


    print(str(condor))

    print(condor.is_even_winged())

    print(condor.initial_credit())

    print(condor.max_loss())

    print(condor.risk_reward_ratio())

    print(condor.serialize())


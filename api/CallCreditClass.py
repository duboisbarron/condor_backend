

class CallCredit:

    def __init__(self, current_share_price, short_call_strike, long_call_strike, short_call_prem, long_call_prem, sc_BA, bc_BA,):

        assert short_call_strike < long_call_strike
        assert short_call_prem > long_call_prem


        self.current_share_price = current_share_price
        self.short_call_strike = short_call_strike
        self.long_call_strike = long_call_strike
        self.short_call_prem = short_call_prem
        self.long_call_prem = long_call_prem

        self.sc_BA = sc_BA
        self.bc_BA = bc_BA

    def get_max_gain(self):
        return round(100.0 * (self.short_call_prem - self.long_call_prem), 2)

    def get_max_loss(self):
        return round(self.get_max_gain() - (100.0 * (self.long_call_strike - self.short_call_strike)), 2)

    def get_risk_reward(self):
        return round(self.get_max_gain() / self.get_max_loss(), 2)

    def serialize(self, id):
        return {
            'id': id,
            'buy_call': self.long_call_strike,
            'short_call': self.short_call_strike,
            'current_share_price': self.current_share_price,
            'buy_call_premium': self.long_call_prem,
            'short_call_premium': self.short_call_prem,
            'max_gain': self.get_max_gain(),
            'max_loss': self.get_max_loss(),
            'risk_reward': self.get_risk_reward(),
            'buy_call_BA': self.bc_BA,
            'short_call_BA': self.sc_BA
        }

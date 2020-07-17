

class PutDebit:

    def __init__(self, current_share_price, short_put_strike, long_put_strike, short_put_prem, long_put_prem, sp_BA, bp_BA):

        assert short_put_strike < long_put_strike
        assert short_put_prem < long_put_prem

        self.current_share_price = current_share_price
        self.short_put_strike = short_put_strike
        self.long_put_strike = long_put_strike
        self.short_put_prem = short_put_prem
        self.long_put_prem = long_put_prem

        self.sp_BA = sp_BA
        self.bp_BA = bp_BA

    def get_max_gain(self):
        return round( (100.0 * (self.long_put_strike - self.short_put_strike) - self.get_max_loss()), 2)

    def get_max_loss(self):
        return round(100.0 * (self.long_put_prem - self.short_put_prem), 2)

    def get_risk_reward(self):
        return round(self.get_max_gain() / abs(self.get_max_loss()), 2)

    def serialize(self, id):
        return {
            'id': id,
            'buy_put': self.long_put_strike,
            'short_put': self.short_put_strike,
            'current_share_price': round(self.current_share_price, 2),
            'buy_put_premium': self.long_put_prem,
            'short_put_premium': self.short_put_prem,
            'max_gain': self.get_max_gain(),
            'max_loss': self.get_max_loss(),
            'risk_reward': self.get_risk_reward(),
            'buy_put_BA': round(self.bp_BA, 2),
            'short_put_BA': round(self.sp_BA, 2)
        }


if __name__ == '__main__':


    put_debit = PutDebit(50, 40, 43, 2.0, 3.0, 1.1, 1.1)

    print(put_debit.serialize(1))
    print(put_debit.get_max_loss())
    print(put_debit.get_max_gain())
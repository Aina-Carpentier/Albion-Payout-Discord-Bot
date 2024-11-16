def payout(nb: int, ammount: float, repair: float, taxes = 0.105):
    pay = (ammount * (1 - taxes) - repair) / nb
    return round(pay, 1)


def payout_premium(nb: int, ammount: float, repair: float)
    return payout(nb, ammout, repair, 0.065)
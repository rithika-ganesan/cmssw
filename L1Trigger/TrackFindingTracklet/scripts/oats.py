import numpy as np

ings = {
    #        qty in g, kcal, P in g
    'oats': [40, 150, 5],
    'chia seeds': [30, 150, 5],
    'hemp seeds': [30, 166, 10],
    'on choc': [31, 120, 24],
    'ot0': [150, 90, 15],
    'cc0': [113, 85, 12]
}

def calc_cals(ings, amts):
    c = 0
    for i, key in enumerate(ings.keys()):
        amt_ = amts[i]
        ing_ = ings[key]
        c_ = ing_[1] * (amt_ / ing_[0])
        c += c_
    return c

def calc_prot(ings, amts):
    p = 0
    for i, key in enumerate(ings.keys()):
        amt_ = amts[i]
        ing_ = ings[key]
        p_ = ing_[2] * (amt_ / ing_[0])
        p += p_ 
    return p

amts = [40, 15, 15, 10, 0, 20]

amts = [None] * 6

for a in np.arange(20, 60, 5):
    amts[0] = a
    for b in np.arange(10, 35, 5):
        amts[1] = b
        for c in np.arange(4, 20, 4):
            amts[2] = c
            for d in np.arange(0, 18, 3):
                amts[3] = d
                for e in np.arange(5, 25, 5):
                    amts[4] = e
                    for f in np.arange(5, 20, 5):
                        amts[5] = f

                        myc = calc_cals(ings, amts)
                        myp = calc_prot(ings, amts)

                        if myc <= 400 and myp >= 26: 
                            print(amts, myc, myp)


# print(calc_cals(ings, amts))
# print(calc_prot(ings, amts))


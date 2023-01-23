sol = [
    [  # 1st vehicle
        [0, 1, 0, 0, 0],  # depot
        [0, 0, 0, 0, 1],  # customer 1
        [0, 0, 0, 1, 0],  # customer 2
        [1, 0, 0, 0, 0],  # customer 3
        [0, 0, 1, 0, 0],  # customer 4
    ]
]


def get_route(s):
    trip = [0]
    current_customer = 0
    while len(trip) < 6:
        for i, val in enumerate(s[0][current_customer]):
            if val:
                trip.append(i)
                current_customer = i
                break
    return trip


print(get_route(sol))

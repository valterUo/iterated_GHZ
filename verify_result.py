# This function verifies that the returned bit strings from each white node satisfy the constraints of the problem (page 6)
def verify_result(bit_strings, number_of_colors):
    for round in range(number_of_colors):
        s = bit_strings[round][0]
        t = bit_strings[round][1]
        u = bit_strings[round][2]
        prev_sum = 0
        for color in range(number_of_colors):
            sum_now = s[color] + t[color] + u[color]
            if color == 0:
                if sum_now != 1:
                    return False
            else:
                if prev_sum == 0:
                    if sum_now % 2 != 0:
                        return False
                elif prev_sum == 2:
                    if sum_now % 2 != 1:
                        return False
            prev_sum = sum_now
    return True
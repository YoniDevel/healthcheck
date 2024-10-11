def calc_control_digit(_id: str) -> int:
    _id = _id.zfill(9 - len(_id)) if len(_id) != 9 else _id
    total = 0       
    for i in range(8):
        val = int(_id[i])
        if i % 2 == 0:
            total += val
        else: 
            if val < 5:
                total += 2 * val
            else:
                total += ((2 * val) % 10) + 1
    total %= 10
    control_digit = (10 - total) % 10
    return control_digit

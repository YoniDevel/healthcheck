def calc_control_digit(_id: str) -> int:
    id_length = len(_id)
    _id = _id.zfill(9 - id_length) if id_length != 9 else _id
    total = 0       
    for i in range(id_length):
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

def validate(field):
    if field is None or field == "":
        return False

    return True

def validate_int(field):
    return int(field)

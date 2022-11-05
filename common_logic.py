async def boolean_format(public):
    if type(public) != bool:
        if public == 1 or public == "1":
            public = True
        else:
            public = False
    return public
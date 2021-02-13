def filterForNullTerminators(response):
    while (len(response) > 0 and response.startswith(b'\0')):
        response = response[1:]
    return response
def parse_http(string):
    lines = string.split(b"\r\n")
    query = lines[0].split(b' ', 2)
    headers = {}
    body = b''
    for pos, line in enumerate(lines[1:]):
        if not line.strip():
            break
        key, value = line.split(b': ', 1)
        headers[key.upper()] = value
        body = b'\r\n'.join(lines[pos + 2:])
    return query, headers, body


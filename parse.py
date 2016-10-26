from urllib.parse import unquote_plus


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


def query_parser(query):
    query = unquote_plus(query.decode()).encode()
    query = query.replace(b'\r\n', b'')
    query = query.split(b"&")
    my_dict = {}
    for i in query:
        key, value = i.split(b"=")
        my_dict[key] = value
    return my_dict


def multipart_parser(multipart,request):
    header = request.get_headers()
    boundary = b"--" + header[b'CONTENT-TYPE'].split(b"; ")[1].split(b"=")[1]

    multipart = multipart.split(boundary)

    multipart.remove(b'\r\n')
    multipart.remove(b'--\r\n')

    multipart_list = []
    for element in multipart:
        header = element.split(b"\r\n\r\n")[0]
        body = element.split(b"\r\n\r\n")[1]
        dict = {}
        body = body.replace(b"\r\n", b"")
        dict["body"] = body
        for line in header.split(b"\r\n"):
            if b'Content-Disposition: ' in line:
                dict["form"] = line[len(b'Content-Dispositon: ') + 1:].split(b"; ")[0]
                dict["name"] = line[len(b'Content-Dispositon: '):].split(b"; ")[1][len(b"name="):]
                if dict["name"] == b'"file"':
                    dict["filename"] = line[len(b'Content-Dispositon: ') - 1:].split(b"; ")[2][len(b"filename="):]
            elif b'Content-Type: ' in line:
                dict["type"] = line[len(b'Content-Type: '):]

        multipart_list.append(dict)

    return multipart_list

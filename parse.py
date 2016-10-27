from urllib.parse import unquote_plus


def parse_http(string):
    lines = string.split("\r\n")
    query = lines[0].split(' ', 2)
    headers = {}
    body = ''
    for pos, line in enumerate(lines[1:]):
        if not line.strip():
            break
        key, value = line.split(': ', 1)
        headers[key.upper()] = value
        body = '\r\n'.join(lines[pos + 2:])
    return query, headers, body


def query_parser(query):
    query = unquote_plus(query)
    query = query.replace('\r\n', '')
    query = query.split("&")
    my_dict = {}
    for i in query:
        key, value = i.split("=")
        my_dict[key] = value
    return my_dict


def multipart_parser(multipart,request):
    header = request.get_headers()
    boundary = "--" + header['CONTENT-TYPE'].split("; ")[1].split("=")[1]

    multipart = multipart.split(boundary)

    multipart.remove('\r\n')
    multipart.remove('--\r\n')

    multipart_list = []
    for element in multipart:
        header = element.split("\r\n\r\n")[0]
        body = element.split("\r\n\r\n")[1]
        dict = {}
        body = body.replace("\r\n", "")
        dict["body"] = body
        for line in header.split("\r\n"):
            if 'Content-Disposition: ' in line:
                dict["form"] = line[len('Content-Dispositon: ') + 1:].split("; ")[0]
                dict["name"] = line[len('Content-Dispositon: '):].split("; ")[1][len("name="):]
                if dict["name"] == '"file"':
                    dict["filename"] = line[len('Content-Dispositon: ') - 1:].split("; ")[2][len("filename="):]
            elif 'Content-Type: ' in line:
                dict["type"] = line[len('Content-Type: '):]

        multipart_list.append(dict)

    return multipart_list

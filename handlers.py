from response import Response


def index(request):
    body = 'html'
    return Response(request, body=body)


def about(request):
    pass


def contacts(request):
    pass

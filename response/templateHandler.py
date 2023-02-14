from response.requestHandler import RequestHandler

class TemplateHandler(RequestHandler):

    request = None

    def __init__(self, request):
        self.request = request
        super().__init__()
        self.contentType = 'text/html'

    def find(self, routeData, request_arg):

        try:
            template_file = open('templates/{}'.format(routeData['template']))
            self.contents = template_file
            self.setStatus(200)
            return True
        except:
            self.setStatus(404)
            return False


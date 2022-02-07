from django.contrib.auth.middleware import RemoteUserMiddleware


class SiteminderMiddleware(RemoteUserMiddleware):

    header = "HTTP_SM_USER"

    def process_request(self, request):
        # print("Processing "+request.META[self.header])
        # print("Username header in request: "+str(request.META[self.header]))
        # print("User in request: "+str(request.user))
        # for header_value in request.META:
        #     print("\t"+str(header_value)+":"+str(request.META[header_value]))

        super().process_request(request)

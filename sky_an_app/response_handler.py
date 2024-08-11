from rest_framework.response import Response


def api_response(status, message, response_object, status_code):

    return Response({'status': status,
                     'message': message,
                     'response_object': response_object},
                    status=status_code)

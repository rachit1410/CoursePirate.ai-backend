from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt


@csrf_exempt
@ensure_csrf_cookie
@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def csrf_init(request):
    return Response(
        {
            'status': 'true',
            'message': 'CSRF token retrieved successfully',
            'data': None,
            'error_message': None
        }
    )

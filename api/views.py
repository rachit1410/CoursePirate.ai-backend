from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import ensure_csrf_cookie

@ensure_csrf_cookie
@api_view(['GET'])
def csrf_init(request):
    return Response(
        {
            'status': 'true',
            'message': 'CSRF token retrieved successfully',
            'data': None,
            'error_message': None
        }
    )


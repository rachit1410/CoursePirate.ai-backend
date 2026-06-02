import re

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt import tokens
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from accounts.authentication import HttpOnlyJWTAuthentication
from rest_framework.permissions import IsAuthenticated
import re
from accounts.validation import email_validation, password_validation, verify_email
User = get_user_model()


# Register the user for first time
class SignUpView(APIView):
    def post(self, request):
        name = request.data.get('name')
        email = request.data.get('email')
        password = request.data.get('password')

        if not name or not email or not password:
            return Response(
                {
                    'status': False,
                    'message': 'Name, email, and password are required.',
                    'data': None,
                    'error_message': 'Missing required fields.'
                }, status=400
            )

        if not email_validation(email):
            return Response(
                {
                    'status': False,
                    'message': 'Invalid email format.',
                    'data': None,
                    'error_message': 'Invalid email format.'
                }, status=400
            )

        if User.objects.filter(email=email).exists():
            return Response(
                {
                    'status': False,
                    'message': 'Email is already in use.',
                    'data': None,
                    'error_message': 'Duplicate email.'
                }, status=400
            )

        if not verify_email(email):
            return Response(
                {
                    'status': False,
                    'message': 'Email address does not exist.',
                    'data': None,
                    'error_message': 'Email verification failed.'
                }, status=400
            )

        if not password_validation(password):
            return Response(
                {
                    'status': False,
                    'message': 'Invalid password format.',
                    'data': None,
                    'error_message': 'Invalid password format.'
                }, status=400
            )

        
        try:
            user = User.objects.create(email=email, name=name)
            user.set_password(password)
            user.save()
            return Response(
                {
                    'status': True,
                    'message': 'User registered successfully.',
                    'data': {
                        'id': user.id,
                        'name': user.name,
                        'email': user.email
                    },
                    'error_message': None
                }, status=201
            )
        except Exception as e:
            return Response(
                {
                    'status': False,
                    'message': 'User registration failed.',
                    'data': None,
                    'error_message': str(e)
                }, status=400
            )


# Authenticate the user and provide JWT tokens
class SignInView(APIView):
        def post(self, request):
            email = request.data.get('email')
            password = request.data.get('password')
            
            print('step 1 recived email: ', email, ' password: ', password)
            
            if not email or not password:
                return Response(
                    {
                        'status': False,
                        'message': 'Email and password are required.',
                        'data': None,
                        'error_message': 'Missing required fields.'
                    }, status=400
                )
            
            print('step 2')
            
            if not User.objects.filter(email=email).exists():
                print('step 3 user not found')
                return Response(
                    {
                        'status': False,
                        'message': 'User with this email does not exist.',
                        'data': None,
                        'error_message': 'User not found.'
                    }, status=404
                )
            print('step 4 user found, authenticating...')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                access_token = tokens.AccessToken.for_user(user)
                refresh_token = tokens.RefreshToken.for_user(user)
                response =  Response(
                    {
                        'status': True,
                        'message': 'User authenticated successfully.',
                        'data': {
                            'id': user.id,
                            'name': user.name,
                            'email': user.email
                        },
                        'error_message': None
                    }, status=200
                )
                
                print('step 5 authentication successful, setting cookies...')
                
                response.set_cookie(key='access_token', value=str(access_token), httponly=True)
                response.set_cookie(key='refresh_token', value=str(refresh_token), httponly=True)
                return response
            else:
                print('step 6 authentication failed, ')
                return Response(
                    {
                        'status': False,
                        'message': 'Invalid email or password.',
                        'data': None,
                        'error_message': 'Authentication failed.'
                    }, status=401
                )

# Refresh the access token using the refresh token
class RefreshTokenView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        
        if not refresh_token:
            return Response(
                {
                    'status': False,
                    'message': 'Refresh token is required.',
                    'data': None,
                    'error_message': 'Missing refresh token.'
                }, status=400
            )
        
        try:
            refresh = tokens.RefreshToken(refresh_token)
            new_access_token = refresh.access_token
            
            response = Response(
                {
                    'status': True,
                    'message': 'Access token refreshed successfully.',
                    'data': None,
                    'error_message': None
                }, status=200
            )
            response.set_cookie(key='access_token', value=str(new_access_token), httponly=True)
            return response
        except Exception as e:
            return Response(
                {
                    'status': False,
                    'message': 'Invalid refresh token.',
                    'data': None,
                    'error_message': str(e)
                }, status=401
            )

# Get the authenticated user's information
class GetUserView(APIView):
    authentication_classes = [HttpOnlyJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.is_authenticated:
            return Response(
                {
                    'status': True,
                    'message': 'User retrieved successfully.',
                    'data': {
                        'id': user.id,
                        'name': user.name,
                        'email': user.email
                    },
                    'error_message': None
                }, status=200
            )
        else:
            return Response(
                {
                    'status': False,
                    'message': 'User is not authenticated.',
                    'data': None,
                    'error_message': 'Authentication required.'
                }, status=401
            
            )


class SignOutView(APIView):
    authentication_classes = [HttpOnlyJWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        response = Response(
            {
                'status': True,
                'message': 'User signed out successfully.',
                'data': None,
                'error_message': None
            }, status=200
        )
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response

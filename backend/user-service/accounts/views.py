from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.models import User
from accounts.serializers import RegisterSerializer, UserSerializer

# AllowAny — anyone can register without a token
# api_view restricts this endpoint to POST requests only
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    # checks if all fields are valid — email format, password length etc.
    if serializer.is_valid():
        # calls create() in RegisterSerializer which calls create_user()
        user = serializer.save() # Python User object
        # returns created user details — JWT tokens are issued on login not registration
        return Response({
            'message': 'User registered successfully',
            'user': UserSerializer(user).data # converted to JSON here
        }, status=status.HTTP_201_CREATED)
    #if validation fails, returns error detials to the caller
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# AllowAny — user has no token yet at login stage
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    # extract email and password from incoming JSON request
    email = request.data.get('email')
    password = request.data.get('password')

    try:
        # query DB to find user by email
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        # same error message for both cases — avoids telling attacker which one is wrong
        return Response({
            'error': 'Invalid email or password'},
            status=status.HTTP_401_UNAUTHORIZED)

    # check_password() hashes the input and compares with stored hash — never compares plain text
    if not user.check_password(password):
        return Response({
            'error': 'Invalid email or password'},
            status=status.HTTP_401_UNAUTHORIZED)

    # generate refresh and access tokens for the authenticated user
    refresh = RefreshToken.for_user(user)
    return Response({
        'message': 'Login successful',
        'access': str(refresh.access_token),  # short lived token for API calls
        'refresh': str(refresh),              # long lived token to get new access token
        'user': UserSerializer(user).data     # user details converted to JSON
    }, status=status.HTTP_200_OK)

# IsAuthenticated — only logged in users with valid JWT token can access this
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    # request.user is automatically set by JWTAuthentication from settings.py
    # no email/password needed — user is identified from the token in header
    user = request.user
    # converts Python User object to JSON and returns profile details
    return Response({
        'user': UserSerializer(user).data
    }, status=status.HTTP_200_OK)

# IsAuthenticated — only logged in users can logout
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    try:
        # user sends back the refresh token they received during login
        refresh_token = request.data.get('refresh')
        # load the refresh token object from simplejwt
        token = RefreshToken(refresh_token)
        # blacklist it — stores in DB as invalid, cannot be used again
        token.blacklist()
        return Response({
            'message': 'Logged out successfully'
        }, status=status.HTTP_200_OK)
    # catches invalid or already blacklisted token errors
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)

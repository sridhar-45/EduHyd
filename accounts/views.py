from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import User
from .serializers import (
    UserSerializer, 
    UserRegistrationSerializer, 
    UserLoginSerializer
)

# ========================================
# USER REGISTRATION API
# ========================================
@api_view(['POST'])
@permission_classes([AllowAny])  # Anyone can register
def register_user(request):
    """
    Register a new user
    
    How it works:
    1. Frontend sends: {"username": "john", "email": "john@email.com", "password": "pass123", ...}
    2. Serializer validates the data
    3. If valid, creates user in database
    4. Returns user data + success message
    """
    
    # Step 1: Get data from request
    # request.data contains the JSON sent from frontend
    serializer = UserRegistrationSerializer(data=request.data)
    
    # Step 2: Validate data
    # Checks if all required fields are present and valid
    if serializer.is_valid():
        # Step 3: Save to database
        user = serializer.save()
        
        # Step 4: Return success response
        return Response({
            'message': 'User registered successfully',
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)
    
    # Step 5: If validation fails, return errors
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ========================================
# USER LOGIN API
# ========================================
@api_view(['POST'])
@permission_classes([AllowAny])  # Anyone can login
def login_user(request):
    """
    Login user and return JWT tokens
    
    How it works:
    1. Frontend sends: {"email": "john@email.com", "password": "pass123"}
    2. Check if user exists and password is correct
    3. Generate JWT tokens (access + refresh)
    4. Return tokens + user data
    
    JWT Token = Digital ID card that proves you're logged in
    - Access Token: Valid for 1 day (for API requests)
    - Refresh Token: Valid for 7 days (to get new access token)
    """
    
    serializer = UserLoginSerializer(data=request.data)
    
    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        
        # Step 1: Find user by email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({
                'error': 'Invalid credentials'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        # Step 2: Check password
        # authenticate() returns user if password correct, None if wrong
        user = authenticate(username=user.username, password=password)
        
        if user is not None:
            # Step 3: Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            
            # Step 4: Return tokens + user data
            return Response({
                'message': 'Login successful',
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                },
                'user': UserSerializer(user).data
            }, status=status.HTTP_200_OK)
        
        return Response({
            'error': 'Invalid credentials'
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ========================================
# GET USER PROFILE API
# ========================================
@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Must be logged in
def get_user_profile(request):
    """
    Get current logged-in user's profile
    
    How it works:
    1. Frontend sends request with JWT token in header
    2. Django validates token
    3. If valid, request.user contains the logged-in user
    4. Return user data
    """
    
    # request.user = current logged-in user (from JWT token)
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)


# ========================================
# USER VIEWSET (For Admin)
# ========================================
class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for User CRUD operations
    
    Automatic endpoints created:
    - GET    /api/users/          -> List all users
    - POST   /api/users/          -> Create user
    - GET    /api/users/{id}/     -> Get single user
    - PUT    /api/users/{id}/     -> Update user
    - PATCH  /api/users/{id}/     -> Partial update
    - DELETE /api/users/{id}/     -> Delete user
    
    How it works:
    - queryset: Which data to work with
    - serializer_class: How to convert data to JSON
    - Django REST Framework handles everything else!
    """
    
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]  # Only logged-in users
    
    # Custom filtering
    def get_queryset(self):
        """
        Filter users based on query parameters
        
        Example URLs:
        - /api/users/?user_type=student     -> Only students
        - /api/users/?search=john           -> Users with "john" in name
        """
        queryset = User.objects.all()
        
        # Get query parameters from URL
        user_type = self.request.query_params.get('user_type', None)
        search = self.request.query_params.get('search', None)
        
        # Filter by user type
        if user_type:
            queryset = queryset.filter(user_type=user_type)
        
        # Search by name or email
        if search:
            queryset = queryset.filter(
                username__icontains=search
            ) | queryset.filter(
                email__icontains=search
            )
        
        return queryset
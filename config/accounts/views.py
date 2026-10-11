from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework import authentication,permissions
from rest_framework.throttling import AnonRateThrottle ,UserRateThrottle
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import NotFound
from django.db.models import Q

from django.contrib.auth import authenticate

from .serailizer import CustomerRegisterSerailizer,StaffRegisterSerailizer,AdminSerailizer,UserProfileSerializer,UserListSerializer
from .models import CustomUser
from .permissions import IsAdminRole
from .custom_pagination import CustomPagination

class CustomerRegisterView(viewsets.ModelViewSet):
    queryset=CustomUser.objects.filter(role = 'CUSTOMER')
    serializer_class=CustomerRegisterSerailizer
    permission_classes=[permissions.AllowAny]
    throttle_classes=[AnonRateThrottle,UserRateThrottle]
    http_method_names = ['get', 'post', 'delete']
    
class StaffRegisterView(viewsets.ModelViewSet):
    queryset=CustomUser.objects.filter(role='STAFF')
    serializer_class=StaffRegisterSerailizer
    permission_classes=[permissions.AllowAny]
    throttle_classes=[AnonRateThrottle,UserRateThrottle]
    http_method_names = ['get', 'post', 'delete']

class AdminRegisterView(viewsets.ModelViewSet):
    queryset=CustomUser.objects.filter(role ='ADMIN')
    serializer_class=AdminSerailizer
    permission_classes=[permissions.AllowAny]
    throttle_classes=[AnonRateThrottle,UserRateThrottle]
    http_method_names = ['get', 'post', 'delete']

class LoginView(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    authentication_classes=[]
    permission_classes = [permissions.AllowAny]
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request,username=username,password=password)

        if not username or not password:
            return Response({
                'message':'Username and Password are required'
            },status=status.HTTP_400_BAD_REQUEST)

        if user is not None:
            if not user.is_active:
                return Response(
                    {'message': 'Account is inactive.'},
                    status=status.HTTP_403_FORBIDDEN
                )
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh':str(refresh),
                'access':str(refresh.access_token),
                'username':user.username,
                'role':user.role
            },status=status.HTTP_200_OK)
        return Response({
            'message':'invalid credentials!!!'
        })

class Profile(viewsets.ModelViewSet):
    queryset=CustomUser.objects.all()
    serializer_class=UserProfileSerializer
    authentication_classes=[JWTAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    http_method_names = ['get', 'patch', 'put', 'head', 'options']
    '''
    CUSTOMER: Can only view their own profile.
    STAFF: Can only view their own profile.
    ADMIN: Can only view their own profile.
    No one can view another user's profile.
    '''
    def get_queryset(self):
        # Every user can access only their own profile
        return CustomUser.objects.filter(id=self.request.user.id)

    def get_object(self):
        # Always return the logged-in user's profile
        return self.request.user

    '''
    CUSTOMER: Can only view their own profile.
    STAFF: Can view their own profile and the profiles of all customers.
    ADMIN: Can view their own profile and the profiles of all customers.
    '''
    # def get_queryset(self):
    #     user = self.request.user

    #     if user.role in ['STAFF', 'ADMIN']:
    #         # Staff and Admin can access their own profile
    #         # and all customer profiles
    #         return CustomUser.objects.filter(
    #             Q(id=user.id) | Q(role='CUSTOMER')
    #         )

    #     # Customers can access only their own profile
    #     return CustomUser.objects.filter(id=user.id)

    # def get_object(self):
    #     user_id = self.request.query_params.get('user_id')

    #     # Staff and Admin can select a specific customer
    #     if user_id and self.request.user.role in ['STAFF', 'ADMIN']:
    #         try:
    #             return self.get_queryset().get(
    #                 id=user_id,
    #                 role='CUSTOMER'
    #             )
    #         except CustomUser.DoesNotExist:
    #             raise NotFound("Customer profile not found.")

    #     # Otherwise, return the logged-in user's profile
    #     return self.get_queryset().get(id=self.request.user.id)

class UserListView(viewsets.ModelViewSet):
    queryset=CustomUser.objects.all().order_by('id')
    serializer_class=UserListSerializer
    permission_classes=[permissions.IsAuthenticated,IsAdminRole]
    pagination_class=CustomPagination

    @action(detail=True, methods=['patch'], url_path='role')
    def update_role(self, request, pk=None):
        user = self.get_object()

        role = request.data.get('role')
        allowed_roles = ['CUSTOMER', 'STAFF', 'ADMIN']

        if role not in allowed_roles:
            return Response(
                {
                    'error': 'Invalid role',
                    'allowed_roles': allowed_roles
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        user.role = role
        user.save(update_fields=['role'])

        return Response({
            'message': 'Role updated successfully',
            'id': user.id,
            'role': user.role
        }, status=status.HTTP_200_OK)
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from weighttrackingapi.models import Employee

ROLES = ["NP", "RD", "MD", "RN", "LPN", "CNA"] 


@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    '''Handles the authentication of a user

    Method arguments:
      request -- The full HTTP request object
    '''
    username = request.data['username']
    password = request.data['password']

    # Use the built-in authenticate method to verify
    # authenticate returns the user object or None if no user is found
    authenticated_user = authenticate(username=username, password=password)
    print(authenticated_user)

    # If authentication was successful, respond with their token
    if authenticated_user is not None:
        token = Token.objects.get(user=authenticated_user)
        name = authenticated_user.first_name
        user_id = authenticated_user.id
        print("Authenticated ID:", user_id)
        role = Employee.objects.get(user_id=user_id).role
        data = {
            'valid': True,
            'token': token.key,
            'name': name,
            'role': role
        }
        return Response(data)
    else:
        # Bad login details were provided. So we can't log the user in.
        data = {'valid': False}
        return Response(data)


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    '''Handles the creation of a new user for authentication

    Method arguments:
      request -- The full HTTP request object
    '''
    # Create a new user by invoking the `create_user` helper method
    # on Django's built-in User model
    print("HELLO!!!!!!!!")
    missing_fields = []
    username = request.data.get('username', None)
    password = request.data.get('password', None)
    first_name = request.data.get('first_name', None)
    last_name = request.data.get('last_name', None)
    email = request.data.get('email', None)
    role = request.data.get('role', None)

    if not username:
        missing_fields.append("username")
    if not password:
        missing_fields.append("password")
    if not first_name:
        missing_fields.append("first_name")
    if not last_name:
        missing_fields.append("last_name")
    if not role:
        missing_fields.append("role")
    if not email:
        missing_fields.append("email")
    
    if missing_fields:
        msg = "Please provide: " + ", ".join(missing_fields)
        return Response({'message': msg}, status=status.HTTP_400_BAD_REQUEST)
    if role not in ROLES:
        msg = f'Role {role} is not authorized. Please provide a valid role.'
        return Response({'message': msg}, status=status.HTTP_400_BAD_REQUEST)


    new_user = User.objects.create_user(
        username = request.data['username'],
        password = request.data['password'],
        first_name = request.data['first_name'],
        last_name = request.data['last_name'],
        email = request.data['email']
    )

    # Now save the extra info in the weighttrackingapi_employee table
    employee = Employee.objects.create(
        role=request.data['role'],
        user=new_user
    )

    # Use the REST Framework's token generator on the new user account
    token = Token.objects.create(user=employee.user)
    # Return the token to the client
    data = {'token': token.key}
    return Response(data)

# Session Authentication and Permission : 
from rest_framework import permissions,authentication
permission_classes = [permissions.IsAuthenticated]
permission_classes = [permissions.IsAuthenticatedOrReadOnly] --> only get requests
authentication_classes = [authentication.SessionAuthentication]

# DjangoModelPermissions

# Token Authentications
Create Token during User Login : 

from rest_framework.authtoken.models import Token

token, _ = Token.objects.get_or_create(user=user) 









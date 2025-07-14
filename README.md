# Session Authentication and Permission : 
from rest_framework import permissions,authentication
permission_classes = [permissions.IsAuthenticated]
permission_classes = [permissions.IsAuthenticatedOrReadOnly] --> only get requests
authentication_classes = [authentication.SessionAuthentication]

# DjangoModelPermissions

# Token Authentications







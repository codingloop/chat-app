from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response

from users.serializers import CreateUserSerializer, BasicUserSerializer


@api_view(['POST'])
def register(request):
    errors = None
    if request.method == 'POST':
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            return Response(BasicUserSerializer(instance).data, status=status.HTTP_201_CREATED)
    return Response(errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        try:
            user = authenticate(username=username, password=password)
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)

    return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

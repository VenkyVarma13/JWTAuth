from django.shortcuts import render
from rest_framework.views import APIView
from .serializer import userserializer
from rest_framework.response import Response
from .models import User
from rest_framework.exceptions import AuthenticationFailed
import jwt, datetime


# Create your views here.
class RegisterView(APIView):
    def post(self, request):
        serializer = userserializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class Loginview(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = User.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed('User Not Found')
        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect Password")
        payload = {
            "id": user.id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            "iat": datetime.datetime.utcnow()
        }
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        response = Response()
        response.set_cookie(key="jwt", value=token, httponly=True)
        response.data = {
            "jwt": token
        }
        return response


class userview(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated")
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated")

        user = User.objects.filter(id=payload['id']).first()
        serializer = userserializer(user)
        return Response(serializer.data)


class logoutview(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            "message": "successful"
        }
        return response
# encoding: utf-8

from django.utils import timezone
from rest_framework import generics, status, exceptions, mixins
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .authentication import generate_access_token, JWTAuthentication
from .models import UserRequestHistory, User
from .serializers import UserSerializer, UserRequestStockSerializer, UserRequestHistorySerializer, UserRequestStatsSerializer
from .producer import Publish
from django.db.models import Count

@api_view(['POST'])
def register(request):
    data = request.data

    if data['password'] != data['password_confirm']:
        raise exceptions.APIException('Password does not match')

    serializer = UserSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    user = User.objects.filter(email=email).first()

    if user is None:
        raise exceptions.AuthenticationFailed('User not found!')

    if not user.check_password(password):
        raise exceptions.AuthenticationFailed('Incorrect Password!')

    response = Response()

    token = generate_access_token(user)
    response.set_cookie(key='jwt', value=token, httponly=True)
    response.data = {
        'jwt': token
    }

    return response

@api_view(['POST'])
def logout(request):
    response = Response()
    response.delete_cookie(key='jwt')
    response.data = {
        'message': 'Logged out'
    }

    return response


class StockView(APIView):
    """
    Endpoint to allow users to query stocks
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        stock_code = request.query_params.get('q')
        stock = Publish()
        response = stock.call(stock_code)

        if response.get("message"):
            return Response(response, status=status.HTTP_404_NOT_FOUND)

        data = {
                'symbol': response['Symbol'],
                'name': response['name'],
                'date': timezone.now(),
                'open': round(float(response['Open']),2),
                'high': round(float(response['High']),2),
                'low': round(float(response['Low']),2),
                'close': round(float(response['Close']),2),
                'user': int(request.user.id)
                }

        serializer = UserRequestStockSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class HistoryView(generics.ListAPIView, mixins.ListModelMixin):
    """
    Returns queries made by current user.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = UserRequestHistory.objects.all().order_by('-date')
    serializer_class = UserRequestHistorySerializer

    def get(self, request):
        return self.list(request)

class StatsView(APIView):
    """
    Allows super users to see which are the most queried stocks.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            serializer_context = {
                'request': request,
            }
            query = (UserRequestHistory.objects
                      .values('symbol')
                      .annotate(times_requested=Count('symbol'),)
                      .order_by('-times_requested')
                      )[:5]

            serializer = UserRequestStatsSerializer(query, many=True,context=serializer_context)

            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            data = {
                'message': 'Only super users'
            }
            return Response(data, status=status.HTTP_405_METHOD_NOT_ALLOWED)
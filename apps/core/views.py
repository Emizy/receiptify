from django.contrib.auth import authenticate
from django.shortcuts import render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from apps.core.models import User, Order, OrderItem
from apps.core.serializer import LoginSerializer, UserSerializer, UserRegistrationSerializer, CreateReceiptSerializer, \
    OrderSerializer
from apps.utils.base import Addon


class AuthViewSet(ViewSet, Addon):
    context = {}
    serializer_class = UserSerializer

    @staticmethod
    def get_tokens_for_user(user):
        refresh = RefreshToken.for_user(user)
        return {
            'access': str(refresh.access_token),
        }

    @staticmethod
    def get_request_data(request) -> dict:
        return request.data if isinstance(request.data, dict) else request.data.dict()

    @swagger_auto_schema(request_body=LoginSerializer,
                         operation_description="This endpoint handle authenticating of users "
                                               "in order to gain access to the system",
                         operation_summary="LOGIN ENDPOINT FOR ALL USERS"
                         )
    @action(detail=False, methods=['post'], description='Login authentication')
    def login(self, request, *args, **kwargs):
        context = {'status': status.HTTP_200_OK}
        try:
            data = request.data
            serializer = LoginSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                user = authenticate(request, username=data.get('email'),
                                    password=data.get('password'))
                if user:
                    context.update({'data': UserSerializer(user).data, 'token': self.get_tokens_for_user(user)})
                else:
                    raise Exception('Invalid credentials,Kindly supply valid credentials')
        except Exception as ex:
            context.update({'status': status.HTTP_400_BAD_REQUEST, 'message': str(ex)})
        return Response(context, status=context['status'])

    @swagger_auto_schema(request_body=UserRegistrationSerializer,
                         operation_description="This endpoint handle onboarding of users into the system",
                         responses={},
                         operation_summary="USER REGISTRATION ENDPOINT"
                         )
    @action(detail=False, methods=['post'], description='on boarding authentication')
    def register(self, request, *args, **kwargs):
        context = {'status': status.HTTP_201_CREATED}
        try:
            try:
                data = self.get_request_data(request)
            except:
                raise Exception('Invalid data supplied')
            for key, value in data.items():
                if value is None or value == '':
                    raise Exception('{} can not be empty'.format(key))

            serializer = UserRegistrationSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                if User.objects.filter(email=data.get('email')).exists():
                    raise Exception('User with this email already exist on our system')
                payload = {
                    'username': self.generate_uuid(User, 'username'),
                    'first_name': data.get('first_name'),
                    'last_name': data.get('last_name'),
                    'mobile': data.get('mobile'),
                    'email': data.get('email'),
                }
                instance = User.objects.create(**payload)
                instance.set_password(data.get('password'))
                instance.save()
                context['message'] = 'Account has been created successfully'
        except Exception as ex:
            context.update({'status': status.HTTP_400_BAD_REQUEST, 'message': str(ex)})
        return Response(context, status=context['status'])


class ReceiptViewSet(ViewSet, Addon):
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        return self.queryset.filter(customer__user=self.request.user)

    @swagger_auto_schema(operation_description="This endpoint handle listing all generated receipt",
                         operation_summary="LIST RECEIPT"
                         )
    def list(self, request, *args, **kwargs):
        context = {'status': status.HTTP_200_OK}
        try:
            context.update({'data': self.serializer_class(self.get_queryset(), many=True).data})
        except Exception as ex:
            context.update({'status': status.HTTP_400_BAD_REQUEST, 'message': str(ex)})
        return Response(context, status=context['status'])

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING,
                                   description='name of the customer'),
            'email': openapi.Schema(type=openapi.TYPE_STRING,
                                    description='email of the customer'),
            'mobile': openapi.Schema(type=openapi.TYPE_STRING,
                                     description='customer mobile number'),
            'address': openapi.Schema(type=openapi.TYPE_STRING,
                                      description='customer mobile number'),
            'orders': openapi.Schema(type=openapi.TYPE_ARRAY,
                                     items=openapi.Items(type=openapi.TYPE_OBJECT, properties={
                                         'name': openapi.Schema(type=openapi.TYPE_STRING,
                                                                description='name of the item'),
                                         'price': openapi.Schema(type=openapi.TYPE_NUMBER,
                                                                 description='price of the item'),
                                     }))
        }
    ),
        operation_description="This endpoint handle generating of receipt for customers",
        operation_summary="CREATE RECEIPT"
    )
    def create(self, request, *args, **kwargs):
        """
        method handles creating of new receipt based on authenticated user making the request
        """

        def validate_order_item():
            for order in orders:
                if 'name' not in order or 'price' not in order:
                    raise Exception('Invalid item data supplied Kindly specify the price and item name ')
                if bool(order.get('name')) is False or bool(order.get('price')) is False:
                    raise Exception('Invalid item data supplied Kindly specify value for price and item name ')

        def create_order_entry():
            """
            inner method handles creating customer order item entry
            """
            for order in orders:
                if 'name' in order and 'price' in order:
                    order.update({'order': order_instance})
                    _ = OrderItem.objects.create(**order)
            return OrderItem.objects.filter(order=order_instance)

        context = {'status': status.HTTP_200_OK}
        try:
            serializer = CreateReceiptSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                orders = request.data.get('orders')
                if not isinstance(orders, list):
                    raise Exception('Orders must be a list of items')
                validate_order_item()
                # create a customer instance
                instance = serializer.create(
                    {'email': request.data.get('email'), 'mobile': request.data.get('mobile'),
                     'address': request.data.get('address'),
                     'name': request.data.get('name'), 'user': request.user})
                # create new order entry
                order_instance = Order.objects.create(**{'customer': instance})
                order_items = create_order_entry()
                resp = self.generate_order_pdf(order_instance.id)  # generate pdf for receipt
                context.update({'message': 'Receipt generated successfully'})
        except Exception as ex:
            context.update({'status': status.HTTP_400_BAD_REQUEST, 'message': str(ex)})
        return Response(context, status=context['status'])


def test(request):
    return render(request, 'receipt/receipt.html', locals())

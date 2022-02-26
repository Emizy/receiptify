from rest_framework import serializers

from apps.core.models import User, ReceiptHistory, Customer, Order, OrderItem


class LoginSerializer(serializers.Serializer):
    """
    User login serializer
    """
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)


class UserRegistrationSerializer(serializers.Serializer):
    """
    User registration serializer
    """
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    mobile = serializers.CharField(required=True)
    password = serializers.CharField(required=True, min_length=8)

    def update(self, instance, validated_data):
        for k, v in validated_data.items():
            instance.__setattr__(k, v)
        instance.save()
        return instance

    def create(self, validated_data):
        instance = User.objects.create(**validated_data)
        return instance


class UserSerializer(serializers.ModelSerializer):
    """
    User model serializer
    """

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'mobile', 'id']


class CreateReceiptSerializer(serializers.Serializer):
    """
    Receipt creation serializer
    """
    name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    mobile = serializers.CharField(required=True)
    address = serializers.CharField(required=True)

    def create(self, validated_data):
        instance, _ = Customer.objects.update_or_create(validated_data, email=validated_data.get('email'),
                                                        user=validated_data.get('user'))
        return instance


class ReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReceiptHistory
        fields = '__all__'


class CustomerSerailizer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    customer = CustomerSerailizer()
    item = serializers.SerializerMethodField('get_items')

    class Meta:
        model = Order
        fields = '__all__'

    @staticmethod
    def get_items(obj):
        return OrderItem.objects.filter(order=obj).count()

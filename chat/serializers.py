from rest_framework import serializers
from .models import Group,Messages
from django.contrib.auth.models import User
from rest_framework.fields import CurrentUserDefault

from django.contrib.auth import authenticate
from django.contrib.auth.models import User

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])

        return user
    
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model=Group
        fields=("group_name",'group_info','members')
        def create(self,validated_data,creater):
            validated_data["creater"]=CurrentUserDefault()
            # members = validated_data.pop('members', [])
            # print(True,type(validated_data),type(validated_data["members"]))

            # if creater in validated_data["members"]:
            #     print(True,type(validated_data),type(validated_data["members"]))
            group=Group.objects.create(validated_data["group_name"],creater,validated_data["group_info"],validated_data["members"])
            group.members.add(creater)
            group.save()
            return group
        # def create(self, validated_data):
        #     request = self.context['request']
        #     creater = request.user
        #     members = validated_data.pop('members', [])

        #     group = Group.objects.create(creater=creater, **validated_data)
        #     group.members.set(members)

        #     return group

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Messages
        fields = '__all__'

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model=Group
        fields=('members',)
        # members = serializers.ListField()

        def update(self,instance,validated_data):
            # group=Group.objects.get(group_name=parent_group)
            instance.members=validated_data.get('members',instance.members)
            # group.members.add(validated_data.members)
            instance.save()
            return instance
            
# class MessageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=Messages
#         fields=("message_text")
#         def create(self,validated_data,parent_group,parent_user):
#             validated_data["creater"]=CurrentUserDefault()
#             # print(True,type(validated_data),type(validated_data["members"]))

#             # if creater in validated_data["members"]:
#             #     print(True,type(validated_data),type(validated_data["members"]))
#             message=Messages.objects.create(parent_group,parent_user,validated_data["message"])
#             return message
    
class LoginSerializer(serializers.Serializer):
    """
    This serializer defines two fields for authentication:
      * username
      * password.
    It will try to authenticate the user with when validated.
    """
    username = serializers.CharField(
        label="Username",
        write_only=True
    )
    password = serializers.CharField(
        label="Password",
        # This will be used when the DRF browsable API is enabled
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, attrs):
        # Take username and password from request
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            # Try to authenticate the user using Django auth framework.
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if not user:
                # If we don't have a regular user, raise a ValidationError
                msg = 'Access denied: wrong username or password.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Both "username" and "password" are required.'
            raise serializers.ValidationError(msg, code='authorization')
        # We have a valid user, put it in the serializer's validated_data.
        # It will be used in the view.
        attrs['user'] = user
        return attrs
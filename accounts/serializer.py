# from django.contrib.auth.models import User
# from rest_framework import serializers
#
# from accounts.models import Profile
#
#
# class UserSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = User
#         fields = "__all__"
#
#
# class ProfileSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Profile
#         fields = "__all__"
#
#     def to_representation(self, instance):
#         ret = super().to_representation(instance)
#         user = User.objects.get(id=ret['user'])
#         ret['user'] = {
#             'username': user.username,
#             'email': user.email,
#         }
#         ret['profile_pic'] = 'https://secoia.ir' + ret['profile_pic']
#         return ret
#
#
#
#


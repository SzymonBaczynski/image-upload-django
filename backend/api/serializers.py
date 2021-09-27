from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import ImageUpload, ExpiringLink, ThumbnailSize
from customAuth.models import User

from pathlib import Path

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['username', ]

class ImageViewerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageUpload
        fields = ['pk', ]

class ImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageUpload
        fields = ['pk', 'orginalImage', 'creationTime']

    def create(self, validated_data):
        user = User.objects.get(pk = self.context['request'].user.id)
        imageFormat = Path(str(validated_data['orginalImage'])).suffix[1:]
        if imageFormat == 'jpg': 
            imageFormat = 'jpeg'
        return ImageUpload.objects.create(user = user, plan = user.userPlan, imageFormat = imageFormat, **validated_data)

class ExpiringLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpiringLink
        fields = ['image', 'expiringTime']

class ThumbnailSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThumbnailSize
        fields = ['heightSize', ]
        

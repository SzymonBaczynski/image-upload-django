# Django
from django.http import response
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.urls import reverse
# DRF
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
# Python and external libs
import datetime
from os import path
from PIL import Image
# Models and serializers
from .serializers import (
    UserSerializer, 
    ImageUploadSerializer, 
    ExpiringLinkSerializer, 
    ImageViewerSerializer, 
    ThumbnailSizeSerializer
    )
from .models import ImageUpload, ThumbnailImage, ExpiringLink, ThumbnailSize, Plan


# Authentication test 
@api_view(['GET',])
def authTestView(request):

    try:
        user = request.user # Obtain the user from the request
    except:
        return Response(status=status.HTTP_401_UNAUTHORIZED) # Return 401 in case of a failure

    # Extension of the serializer with the name of a user's plan.
    serializer = UserSerializer(user)
    serialized_data = serializer.data
    serialized_data['userPlan'] = user.userPlan.__str__()

    return Response(serialized_data) # Response with basic info of the current user 

# An image upload handler
@api_view(['POST',])
def imageUpload(request):

    # Find thumbnail sizes to create in the particular user's plan
    thumbnailSizes = request.user.userPlan.thumbnailSizesInPlan.all()

    # Populate the serializer with an incoming image 
    # Pass of request allows handle user recognition inside ImageUploadSerializer
    serializer = ImageUploadSerializer(data=request.data,  context={'request': request})

    # Validate incoming data
    if serializer.is_valid():
        
        imageUpload = serializer.save() # Save original image

        image = imageUpload.orginalImage
        file, ext = path.splitext(image.path) # Obtain path with file's name and file's extension
        
        # Creation of thumbnails according to a user's plan
        for thumbnailSize in thumbnailSizes:
            with Image.open(image) as img:
                imgSize = (img.width, thumbnailSize.heightSize) # Set expected image's size 
                img.thumbnail(imgSize) # Resize an image 
                newPath = file + "_thumbnail_" + str(thumbnailSize.heightSize) + ext # Image's name change
                img.save(newPath) # Save an image with new name

            # Create a dedicated thumbnail model object with recently saved image
            ThumbnailImage.objects.create(
                thumbnailSize = thumbnailSize, 
                processedImage = newPath, imageUpload = imageUpload 
                )

        # Response with an image's PK 
        serializer = ImageViewerSerializer(imageUpload)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
 
    return Response(status=status.HTTP_400_BAD_REQUEST) # Response in the case of a data validation failure

# Expiring links handler - crate and list available images
class userImageTempLinkCreator(APIView):

    # Get method responses with list of user's images
    def get(self, request, format=None):
        user = request.user
        images = ImageUpload.objects.filter(user = user)
        serializer = ImageViewerSerializer(images, many=True)
        return Response(serializer.data)

    # Post method creates a temp link in response to a user image's pk.
    def post(self, request, format=None):
        user = request.user

        # Does user have feature in plan to create an expiring links
        if not user.userPlan.expiringLinksFeature:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        # Populate the serializer with an incoming request
        serializer = ExpiringLinkSerializer(data=request.data)

        # Check if the user possess a image with an incoming pk
        owner = get_object_or_404(ImageUpload, pk = request.data['image']).user

        # Incoming data validation and creation of an expiring link
        if serializer.is_valid() and (owner == user) :
            createdExpiringLink = serializer.save()    

            # Response with a temp link to original image
            return Response(
                request.scheme + '://' + request.META['HTTP_HOST'] + reverse('tempLinkResolver',
                kwargs={'uuid': createdExpiringLink.id})
                )

        # 400 Response in case of a invalid data
        return Response(status=status.HTTP_400_BAD_REQUEST)        

# Handler to obtain an image from an expiring link
@api_view(['GET',])
@permission_classes([AllowAny])
def tempLinkResolver(request, uuid):

    # Find a image thanks so provided uuid from a reqest
    link = get_object_or_404(ExpiringLink, id = uuid)

    # Check if the image is still available 
    image = link.image.orginalImage
    if link.creationTime + datetime.timedelta(0, link.expiringTime) < timezone.now():
        # Response in case of the expired link
        return Response({'response': 'Link expired.'},status=status.HTTP_403_FORBIDDEN)

    imageFormat = link.image.imageFormat
    print(imageFormat)
    # An image response
    return response.HttpResponse(image, content_type= "image/" + imageFormat)

# A handler of access to original images
@api_view(['GET',])
def originalImageResolver(request, pk):
    user = request.user
    
    # Check if the user has the feature in a plan
    if not user.userPlan.urlToOriginalFileFeature:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    # Find an image and check it's owner
    image = get_object_or_404(ImageUpload, user = user, pk = pk)
    imageFormat = image.imageFormat
    # Response with the wanted image
    image = image.orginalImage
    return response.HttpResponse(image, content_type= "image/" + imageFormat)

# Handler of access to thumbnails
@api_view(['GET',])
def thumbnailImageResolver(request, pk, size):
    user = request.user
    imageUpload = get_object_or_404(ImageUpload, user = user, pk = pk)    
    thumbnailSize = get_object_or_404(ThumbnailSize, heightSize = size)
    # Find a thumbnail
    image = get_object_or_404(
        ThumbnailImage, 
        imageUpload = imageUpload, 
        thumbnailSize = thumbnailSize 
        ) 
    # Response with the wanted thumbnail 
    image = image.processedImage
    imageFormat = imageUpload.imageFormat
    return response.HttpResponse(image, content_type="image/" + imageFormat)

# List of available sizes of an image's thumbnail
@api_view(['GET',])
def availableThumbnailImageSizes(request, pk):
    user = request.user

    # Check if the user is image's owner
    thumbnailsSizes = get_object_or_404(ImageUpload, user = user, pk = pk).plan.thumbnailSizesInPlan.all()

    # Respons with a list of sizes
    serializer =ThumbnailSizeSerializer(thumbnailsSizes, many=True)
    return Response(serializer.data)


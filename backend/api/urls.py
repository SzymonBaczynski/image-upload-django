from django.urls import path
from .views import authTestView, imageUpload, tempLinkResolver, userImageTempLinkCreator, originalImageResolver, thumbnailImageResolver, availableThumbnailImageSizes

urlpatterns = [

    path('', authTestView, name='authTestView'),
    path('image-upload/', imageUpload, name='imageUpload'),
    path('create-temp-link/', userImageTempLinkCreator.as_view(), name='userImageTempLinkCreator'),
    path('temp-link/<uuid:uuid>/', tempLinkResolver, name='tempLinkResolver'),
    path('original-image/<int:pk>/', originalImageResolver, name='originalImageResolver'),
    path('thumbnail-image/<int:pk>/<int:size>/', thumbnailImageResolver, name='thumbnailImageResolver'),
    path('thumbnail-image/<int:pk>/', availableThumbnailImageSizes, name='availableThumbnailImageSizes')
    
]

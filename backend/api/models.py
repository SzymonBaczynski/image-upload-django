from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

import uuid

class ThumbnailSize(models.Model):    
    heightSize = models.PositiveIntegerField(validators=[MinValueValidator(1)], unique=True)

    def __str__(self):
        return str(self.heightSize)

class Plan(models.Model):
    planName = models.CharField(max_length=15)
    thumbnailSizesInPlan = models.ManyToManyField(ThumbnailSize, blank=True, default=None)
    urlToOriginalFileFeature = models.BooleanField(blank=False, default=False)
    expiringLinksFeature = models.BooleanField(blank=False, default=False)

    def __str__(self):
        return self.planName 

class ImageUpload(models.Model):    
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT, blank=False)
    orginalImage = models.ImageField(upload_to='images/')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, blank=False)
    creationTime = models.DateTimeField(auto_now_add=True)
    imageFormat = models.CharField(max_length=5, blank=False)

    def __str__(self):
         return str(self.user) + ' id: ' + str(self.pk)
         
class ThumbnailImage(models.Model):    
    thumbnailSize = models.ForeignKey(ThumbnailSize, on_delete=models.PROTECT)
    processedImage = models.ImageField()
    imageUpload = models.ForeignKey(ImageUpload, on_delete=models.CASCADE)
    
class ExpiringLink(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ForeignKey(ImageUpload, on_delete=models.CASCADE)
    expiringTime = models.PositiveIntegerField(validators=[MinValueValidator(300), MaxValueValidator(3000)])
    creationTime = models.DateTimeField(auto_now_add=True)

    





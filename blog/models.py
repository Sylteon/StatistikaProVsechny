from django.db import models
from azure.storage.blob import BlobServiceClient
from django.conf import settings

class ApiEndpoint(models.Model):
    name = models.CharField(max_length=255, unique=True)
    url = models.URLField()
    api_key = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class ExcelFile(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField()
    file_url = models.URLField(max_length=500, blank=True, null=True)  # New field to store the URL

    def save(self, *args, **kwargs):
        # Call the original save method to save the file locally first
        super().save(*args, **kwargs)

        if self.file:
            # Upload the file to Azure Blob Storage
            blob_service_client = BlobServiceClient(account_url=f"https://{settings.AZURE_ACCOUNT_NAME}.blob.core.windows.net", credential=settings.AZURE_ACCOUNT_KEY)
            container_name = settings.AZURE_CONTAINER_EXCEL

            # Define the file path and name
            file_name = self.file.name

            try:
                # Create a container if it doesn't exist
                container_client = blob_service_client.get_container_client(container_name)
                try:
                    container_client.create_container()
                except Exception as e:
                    # Container already exists
                    pass

                # Upload the file
                blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_name)
                with open(self.file.path, "rb") as data:
                    blob_client.upload_blob(data, blob_type="BlockBlob", overwrite=True)

                # Construct the URL for the uploaded file
                file_url = f"https://{settings.AZURE_ACCOUNT_NAME}.blob.core.windows.net/{container_name}/{file_name}"

                # Update the file_url field and save the model instance again
                self.file_url = file_url
                super().save(update_fields=['file_url'])

                # Optionally, delete the local file after uploading
                #self.file.delete(save=False)

            except Exception as e:
                # Handle any exceptions that occur during the upload process
                print(f"An error occurred: {e}")

        # Save the model instance again to update any changes
        #super().save(*args, **kwargs)
        
    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=100, unique=True)
    perex = models.TextField(max_length=255,default='')
    content = models.TextField()
    tags = models.ManyToManyField(Tag)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    measurement_unit = models.CharField(max_length=50, default='Počet')
    excel_file = models.OneToOneField(ExcelFile, on_delete=models.CASCADE, null=True, blank=True)
    api_endpoint = models.OneToOneField(ApiEndpoint, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title
from django.db import models

class ApiEndpoint(models.Model):
    url = models.URLField()
    api_key = models.CharField(max_length=255)

    def __str__(self):
        return f"API Endpoint for {self.url}"

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
    file = models.FileField(upload_to='excel/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=255, unique=True)
    content = models.TextField()
    tags = models.ManyToManyField(Tag)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    excel_file = models.OneToOneField(ExcelFile, on_delete=models.CASCADE, null=True, blank=True)
    api_endpoint = models.OneToOneField(ApiEndpoint, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title
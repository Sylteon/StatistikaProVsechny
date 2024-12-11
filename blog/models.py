from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=255, unique=True)
    content = models.TextField()
    tags = models.ManyToManyField(Tag)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    csv_file = models.ForeignKey('CSVFile', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title

class CSVFile(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='csv/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
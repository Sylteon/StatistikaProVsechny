# Generated by Django 5.1.2 on 2024-12-28 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_article_perex_alter_article_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='measurement_unit',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
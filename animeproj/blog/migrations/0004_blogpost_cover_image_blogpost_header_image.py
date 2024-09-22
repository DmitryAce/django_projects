# Generated by Django 5.1 on 2024-09-20 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_remove_blogcontentblock_content_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='cover_image',
            field=models.ImageField(default=1, upload_to='blog/blog_cover'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='blogpost',
            name='header_image',
            field=models.ImageField(blank=True, null=True, upload_to='blog/blog_headers'),
        ),
    ]
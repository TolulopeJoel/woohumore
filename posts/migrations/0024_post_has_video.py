# Generated by Django 4.1 on 2024-01-11 13:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("posts", "0023_rename_published_post_is_published_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="has_video",
            field=models.BooleanField(default=False),
        ),
    ]

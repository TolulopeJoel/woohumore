# Generated by Django 4.1 on 2024-01-11 13:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("posts", "0022_post_audio_length"),
    ]

    operations = [
        migrations.RenameField(
            model_name="post",
            old_name="published",
            new_name="is_published",
        ),
        migrations.RenameField(
            model_name="post",
            old_name="summarised",
            new_name="is_summarised",
        ),
        migrations.RemoveField(
            model_name="post",
            name="no_audio",
        ),
        migrations.RemoveField(
            model_name="post",
            name="no_body",
        ),
        migrations.AddField(
            model_name="post",
            name="has_audio",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="post",
            name="has_body",
            field=models.BooleanField(default=False),
        ),
    ]

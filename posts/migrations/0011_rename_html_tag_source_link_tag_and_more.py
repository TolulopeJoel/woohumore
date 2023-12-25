# Generated by Django 5.0 on 2023-12-25 17:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("posts", "0010_rename_body_tag_classes_source_body_tag_class_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="source",
            old_name="html_tag",
            new_name="link_tag",
        ),
        migrations.RenameField(
            model_name="source",
            old_name="html_tag_class",
            new_name="link_tag_class",
        ),
        migrations.AddField(
            model_name="source",
            name="title_tag",
            field=models.CharField(default="", max_length=255),
            preserve_default=False,
        ),
    ]
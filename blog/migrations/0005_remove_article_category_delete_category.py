# Generated by Django 4.0.3 on 2022-03-07 14:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_category_slug_tag_slug_alter_article_category_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='category',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]
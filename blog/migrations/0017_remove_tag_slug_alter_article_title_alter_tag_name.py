# Generated by Django 4.0.3 on 2022-05-25 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0016_alter_comment_parent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='slug',
        ),
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
    ]
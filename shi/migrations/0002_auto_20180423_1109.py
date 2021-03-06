# Generated by Django 2.0.4 on 2018-04-23 02:09

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('shi', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='choice',
            name='vote',
        ),
        migrations.RemoveField(
            model_name='shi',
            name='pub_date',
        ),
        migrations.AddField(
            model_name='shi',
            name='created_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='shi',
            name='published_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='shi',
            name='output_text',
            field=models.TextField(blank=True),
        ),
    ]

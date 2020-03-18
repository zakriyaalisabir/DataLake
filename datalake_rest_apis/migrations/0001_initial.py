# Generated by Django 3.0.4 on 2020-03-18 20:41

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FileItem',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4,
                                        editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=120, null=True)),
                ('path', models.TextField(blank=True, null=True)),
                ('size', models.BigIntegerField(default=0)),
                ('file_type', models.CharField(
                    blank=True, max_length=120, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('uploaded', models.BooleanField(default=False)),
            ],
        ),
    ]

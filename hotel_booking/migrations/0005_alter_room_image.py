# Generated by Django 5.1.3 on 2024-12-01 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel_booking', '0004_alter_room_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='image',
            field=models.ImageField(default='rooms/default_image.jpg', upload_to='rooms/'),
        ),
    ]
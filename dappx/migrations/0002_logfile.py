# Generated by Django 2.2.12 on 2020-04-28 05:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dappx', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LogFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('LogPath', models.CharField(max_length=512)),
                ('FileName', models.CharField(max_length=512)),
                ('PostedDate', models.DateField()),
                ('AnalyzeStatus', models.CharField(max_length=20)),
                ('PostedBy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dappx.UserProfileInfo')),
            ],
        ),
    ]

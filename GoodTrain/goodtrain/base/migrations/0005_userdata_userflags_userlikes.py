# Generated by Django 3.2.7 on 2023-10-16 19:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_rename_transaction_transactionkarma'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserFlags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='UserLikes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='UserData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('agreeableness', models.IntegerField(default=0, null=True)),
                ('conscientiousness', models.IntegerField(default=0, null=True)),
                ('extraversion', models.IntegerField(default=0, null=True)),
                ('openness', models.IntegerField(default=0, null=True)),
                ('emotional_stability', models.IntegerField(default=0, null=True)),
                ('interest_economic', models.IntegerField(default=0, null=True)),
                ('interest_social', models.IntegerField(default=0, null=True)),
                ('interest_spiritual', models.IntegerField(default=0, null=True)),
                ('interest_political', models.IntegerField(default=0, null=True)),
                ('sex', models.IntegerField(default=0, null=True)),
                ('age', models.IntegerField(default=0, null=True)),
                ('profession', models.CharField(max_length=200)),
                ('social_level', models.IntegerField(default=0, null=True)),
                ('education', models.CharField(max_length=200)),
                ('flags', models.ManyToManyField(to='base.UserFlags')),
                ('likes', models.ManyToManyField(to='base.UserLikes')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

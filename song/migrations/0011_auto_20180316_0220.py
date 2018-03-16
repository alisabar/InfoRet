# Generated by Django 2.0.2 on 2018-03-16 00:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('song', '0010_auto_20180313_2213'),
    ]

    operations = [
        migrations.CreateModel(
            name='Songofword',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('times', models.IntegerField(default=0)),
                ('indexes', models.CharField(max_length=100)),
                ('song', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='song.Songs')),
            ],
        ),
        migrations.RemoveField(
            model_name='words',
            name='indexes',
        ),
        migrations.RemoveField(
            model_name='words',
            name='song',
        ),
        migrations.RemoveField(
            model_name='words',
            name='times',
        ),
        migrations.AddField(
            model_name='words',
            name='songs',
            field=models.ManyToManyField(to='song.Songofword'),
        ),
    ]

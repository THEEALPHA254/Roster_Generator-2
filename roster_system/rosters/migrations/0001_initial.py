from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('age', models.IntegerField(default=0)),
                ('contact', models.CharField(default='', max_length=100)),
                ('roles', models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to='rosters.role')),
            ],
        ),
        migrations.CreateModel(
            name='Roster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sunday_date', models.DateField()),
                ('members', models.ManyToManyField(related_name='rosters', to='rosters.member')),
                ('roles', models.ManyToManyField(related_name='rosters', to='rosters.role')),
            ],
        ),
    ]

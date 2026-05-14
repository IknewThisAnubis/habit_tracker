# Generated migration to add mood and gratitude fields to HabitLog

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habitrack', '0002_habitlog'),
    ]

    operations = [
        migrations.AddField(
            model_name='habitlog',
            name='mood',
            field=models.IntegerField(
                blank=True,
                choices=[(1, 'Very Sad'), (2, 'Sad'), (3, 'Neutral'), (4, 'Happy'), (5, 'Very Happy')],
                null=True
            ),
        ),
        migrations.AddField(
            model_name='habitlog',
            name='gratitude',
            field=models.TextField(blank=True, null=True),
        ),
    ]

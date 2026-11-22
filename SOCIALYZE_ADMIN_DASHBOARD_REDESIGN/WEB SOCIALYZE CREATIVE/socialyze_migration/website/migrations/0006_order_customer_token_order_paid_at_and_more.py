
import uuid

from django.db import migrations, models


def generate_customer_tokens(apps, schema_editor):
    Order = apps.get_model('website', 'Order')
    database = schema_editor.connection.alias

    for order in Order.objects.using(database).filter(
        customer_token__isnull=True
    ).iterator():
        order.customer_token = uuid.uuid4()
        order.save(update_fields=['customer_token'])


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0005_article_author_article_published_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='customer_token',
            field=models.UUIDField(
                null=True,
                blank=True,
                editable=False,
            ),
        ),

        migrations.RunPython(
            generate_customer_tokens,
            migrations.RunPython.noop,
        ),

        migrations.AlterField(
            model_name='order',
            name='customer_token',
            field=models.UUIDField(
                default=uuid.uuid4,
                editable=False,
                unique=True,
            ),
        ),

        migrations.AddField(
            model_name='order',
            name='paid_at',
            field=models.DateTimeField(
                blank=True,
                null=True,
            ),
        ),

        migrations.AddField(
            model_name='order',
            name='payment_status',
            field=models.CharField(
                choices=[
                    ('PENDING', 'Menunggu pembayaran'),
                    ('SUCCESS', 'Berhasil'),
                    ('FAILED', 'Gagal'),
                    ('CANCELLED', 'Dibatalkan'),
                ],
                default='PENDING',
                max_length=20,
            ),
        ),
    ]

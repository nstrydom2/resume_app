from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0008_portfolio_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="portfolio",
            name="is_featured",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="portfolio",
            name="technologies",
            field=models.CharField(
                blank=True,
                help_text="Comma-separated list, e.g. Django, PostgreSQL, HTMX",
                max_length=300,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="portfolio",
            name="live_url",
            field=models.URLField(
                blank=True, null=True, verbose_name="Live demo URL"
            ),
        ),
        migrations.AddField(
            model_name="portfolio",
            name="repository_url",
            field=models.URLField(
                blank=True, null=True, verbose_name="Source code URL"
            ),
        ),
    ]

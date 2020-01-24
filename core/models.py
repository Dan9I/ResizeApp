from django.db import models


class Images(models.Model):

    image = models.ImageField(
        verbose_name='Image file',
        unique=True
    )

    url = models.URLField(
        unique=False,
        blank=True
    )

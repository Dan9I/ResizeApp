from django.db import models
import hashlib
import os


class Images(models.Model):

    image = models.ImageField(
        verbose_name='Image file',
        unique=True
    )

    imgHash = models.CharField(
        unique=True,
        max_length=256,
        editable=False
    )
    def save(self, *args, **kwargs):
        super(Images, self).save(*args, **kwargs)
        filename = self.image.path
        with open(filename, "rb") as f:
            bytes = f.read()
            self.imgHash = hashlib.sha256(bytes).hexdigest()
        super(Images, self).save(*args, **kwargs)

    def filename(self):
        return os.path.basename(self.image.name)


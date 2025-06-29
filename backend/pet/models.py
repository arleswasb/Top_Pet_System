from django.db import models
from datetime import date

class Pet(models.Model):
    # ...existing fields...
    birth_date = models.DateField()
    idade = models.IntegerField(default=0)
    # ...existing fields...

    def save(self, *args, **kwargs):
        if self.birth_date:
            today = date.today()
            self.idade = today.year - self.birth_date.year - (
                (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
            )
        super().save(*args, **kwargs)
    # ...existing methods...
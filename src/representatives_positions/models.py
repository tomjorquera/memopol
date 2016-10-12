from django.db import models
from django.template.defaultfilters import truncatewords
from representatives.models import Representative


KIND_CHOICES = (
    ('other', 'Other'),
    ('blog', 'Blog post'),
    ('social', 'Social network'),
    ('press', 'Press interview'),
    ('parliament', 'Parliament debate'),
    ('amendment', 'Amendment'),
)


class Position(models.Model):
    representatives = models.ManyToManyField(Representative,
                                             related_name='positions')
    datetime = models.DateField()
    kind = models.CharField(max_length=64, choices=KIND_CHOICES,
                            default='other')
    title = models.CharField(max_length=500, null=True)
    text = models.TextField()
    link = models.URLField(max_length=500)
    score = models.IntegerField(default=0)
    published = models.BooleanField(default=False)

    @property
    def short_title(self):
        return truncatewords(self.title, 5)

    @property
    def short_text(self):
        return truncatewords(self.text, 5)

    def publish(self):
        self.published = True

    def unpublish(self):
        self.published = False

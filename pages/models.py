from django.db import models


class Page(models.Model):
    name = models.CharField(max_length=500)
    url = models.CharField(max_length=500)
    enabled = models.BooleanField(default=True)
    expires = models.DateTimeField(null=True)
    email = models.EmailField("Assignee Email", blank=True)

    page_id = models.IntegerField(default=0, blank=True)
    content = models.TextField(blank=True)
    title = models.TextField(blank=True)
    seo_description = models.TextField(blank=True)
    template_id = models.IntegerField("Template ID", default=-1, blank=True)

    def __str__(self):
        return "%s" % self.name
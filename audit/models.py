from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet


class AuditRecord(models.Model):
    page_url = models.URLField(max_length=500)
    page_name = models.CharField(max_length=200)
    run_at = models.DateTimeField(auto_now_add=True)
    tool = models.CharField(max_length=20, default='pa11y')
    issues_found = models.IntegerField(default=0)
    notes = models.TextField(blank=True)
    raw_json = models.JSONField(null=True, blank=True)
    
    class Meta:
        ordering = ['-run_at']
    
    def __str__(self):
        return f'{self.page_name} - {self.run_at:%Y-%m-%d %H:%M}'


@register_snippet
class WCAGIssue(models.Model):
    audit = models.ForeignKey(AuditRecord, on_delete=models.CASCADE, related_name='wcag_issues')
    code = models.CharField(max_length=100)
    wcag = models.CharField(max_length=50, blank=True)
    message = models.TextField()
    selector = models.TextField(blank=True)
    context = models.TextField(blank=True)
    type = models.CharField(max_length=20, blank=True)
    impact = models.CharField(max_length=20, blank=True)
    
    def __str__(self):
        return f'{self.code} - {self.audit.page_name}'


class AuditIndexPage(Page):
    intro = RichTextField(blank=True)
    
    content_panels = Page.content_panels + [FieldPanel('intro')]
    
    def get_context(self, request):
        context = super().get_context(request)
        context['audits'] = AuditRecord.objects.all()[:10]
        context['total_audits'] = AuditRecord.objects.count()
        context['total_issues'] = sum(audit.issues_found for audit in AuditRecord.objects.all())
        return context

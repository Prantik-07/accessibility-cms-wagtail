import subprocess
import json
from .models import AuditRecord, WCAGIssue


def run_pa11y_audit(page_url, page_name, notes=''):
    try:
        result = subprocess.run(
            ['pa11y', '--reporter', 'json', page_url],
            capture_output=True, text=True, timeout=60, shell=True
        )
        
        issues_data = []
        if result.stdout:
            try:
                issues_data = json.loads(result.stdout)
            except json.JSONDecodeError:
                return AuditRecord.objects.create(
                    page_url=page_url, page_name=page_name, tool='pa11y',
                    issues_found=0, notes=f'Invalid JSON. {notes}'
                )
        
        audit = AuditRecord.objects.create(
            page_url=page_url, page_name=page_name, tool='pa11y',
            issues_found=len(issues_data), raw_json=issues_data, notes=notes
        )
        
        for issue in issues_data:
            WCAGIssue.objects.create(
                audit=audit, code=issue.get('code', 'Unknown'),
                wcag=issue.get('wcag', ''), message=issue.get('message', ''),
                selector=issue.get('selector', ''), context=issue.get('context', ''),
                type=issue.get('type', 'error'), impact=issue.get('impact', '')
            )
        return audit
        
    except subprocess.TimeoutExpired:
        return AuditRecord.objects.create(
            page_url=page_url, page_name=page_name, tool='pa11y',
            issues_found=0, notes=f'Timeout. {notes}'
        )
    except Exception as e:
        return AuditRecord.objects.create(
            page_url=page_url, page_name=page_name, tool='pa11y',
            issues_found=0, notes=f'Error: {str(e)}. {notes}'
        )

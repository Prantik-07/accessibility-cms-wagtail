from wagtail import hooks
from django.urls import path, reverse
from django.shortcuts import render, redirect
from django.contrib import messages
from wagtail.admin.menu import MenuItem
from .models import AuditRecord, WCAGIssue
from .services import run_pa11y_audit


@hooks.register('register_admin_urls')
def register_audit_url():
    return [path('run-audit/', run_audit_view, name='run_audit')]


@hooks.register('register_admin_menu_item')
def register_audit_menu_item():
    return MenuItem('Run Audit', reverse('run_audit'), icon_name='doc-full-inverse', order=10000)


def run_audit_view(request):
    if request.method == 'POST':
        page_url = request.POST.get('page_url')
        page_name = request.POST.get('page_name')
        notes = request.POST.get('notes', '')
        if page_url and page_name:
            audit = run_pa11y_audit(page_url, page_name, notes)
            messages.success(request, f'Audit completed! Found {audit.issues_found} issues.')
            return redirect('wagtailadmin_home')
    return render(request, 'audit/run_audit.html')

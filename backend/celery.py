from __future__ import absolute_import
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stock_risk_analysis.settings')

app = Celery('stock_risk_analysis')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

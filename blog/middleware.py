import os
from django.conf import settings
from django.core.files.storage import default_storage
from django.contrib.sessions.models import Session
from django.utils import timezone

class DeleteExpiredFilesMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the session has expired
        self.delete_expired_sessions()

        response = self.get_response(request)
        return response

    def delete_expired_sessions(self):
        now = timezone.now()
        expired_sessions = Session.objects.filter(expire_date__lt=now)
        for session in expired_sessions:
            self.delete_generated_files(session)
            session.delete()

    def delete_generated_files(self, session):
        session_data = session.get_decoded()
        generated_files = session_data.get('generated_files', [])
        for file_path in generated_files:
            if default_storage.exists(file_path):
                default_storage.delete(file_path)
"""Audit logging and role-based access middleware."""
import json
from django.utils.deprecation import MiddlewareMixin
from django.contrib.contenttypes.models import ContentType

# Lazy import to avoid circular import
def get_audit_log_model():
    from slm.models import AuditLog
    return AuditLog


def get_request_user(request):
    if hasattr(request, "user") and request.user.is_authenticated:
        return request.user
    return None


def get_client_ip(request):
    xff = request.META.get("HTTP_X_FORWARDED_FOR")
    if xff:
        return xff.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


class AuditLogMiddleware(MiddlewareMixin):
    """Log request metadata for audit (actual model changes logged in signals or views)."""
    def process_request(self, request):
        request._audit_extra = {}

    def process_response(self, request, response):
        return response


class RoleBasedAccessMiddleware(MiddlewareMixin):
    """Enforce role-based access; restrict certain paths by role."""
    AUDITOR_READ_ONLY_PATHS = ["/api/"]  # Auditor can only GET

    def process_request(self, request):
        user = get_request_user(request)
        if not user or not hasattr(user, "role"):
            return None
        if user.role == "auditor" and request.method not in ("GET", "HEAD", "OPTIONS"):
            # Block write methods for auditor on API
            if request.path.startswith("/api/") and request.method not in ("GET", "HEAD", "OPTIONS"):
                from django.http import HttpResponseForbidden
                return HttpResponseForbidden("Auditor has read-only access.")
        return None

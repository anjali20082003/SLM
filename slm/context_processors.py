"""Template context processors for dashboards and UI."""
from django.conf import settings


def dashboard_context(request):
    """Add role and dashboard-related context to templates."""
    from slm.models import Notification
    ctx = {
        "user_role": getattr(request.user, "role", None) if request.user.is_authenticated else None,
        "dark_mode": request.session.get("dark_mode", False),
    }
    if request.user.is_authenticated:
        ctx["unread_notifications"] = Notification.objects.filter(user=request.user, is_read=False).count()
        ctx["is_auditor"] = getattr(request.user, "role", None) == "auditor"
        ctx["can_edit_assets"] = getattr(request.user, "can_edit_assets", False)
        ctx["can_edit_finance"] = getattr(request.user, "can_edit_finance", False)
        ctx["can_edit"] = ctx.get("can_edit_assets") or ctx.get("can_edit_finance") or getattr(request.user, "role", None) == "super_admin"
    else:
        ctx["unread_notifications"] = 0
        ctx["is_auditor"] = False
        ctx["can_edit"] = False
    return ctx

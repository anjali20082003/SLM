import os
from .base import *

env = os.environ.get("DJANGO_ENV", "development")
if env == "production":
    from .production import *  # noqa: F401, F403
elif env == "minimal":
    from .minimal import *  # noqa: F401, F403
else:
    from .development import *  # noqa: F401, F403

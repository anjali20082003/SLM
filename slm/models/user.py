"""User, Department, Branch models with RBAC."""
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

ROLE_CHOICES = [
    ("super_admin", "Super Admin"),
    ("it_manager", "IT Manager"),
    ("it_staff", "IT Staff"),
    ("finance_manager", "Finance Manager"),
    ("accounts_officer", "Accounts Officer"),
    ("department_head", "Department Head"),
    ("auditor", "Auditor (Read-Only)"),
]


class Branch(models.Model):
    """Multi-branch support."""
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)
    address = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Branches"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Department(models.Model):
    """Department for allocation and reporting."""
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True, related_name="departments")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **kwargs):
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)
        kwargs.setdefault("role", "super_admin")
        if kwargs.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email, password, **kwargs)


class User(AbstractUser):
    """Custom user with role and department."""
    username = None
    email = models.EmailField("email address", unique=True)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default="it_staff")
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True, blank=True, related_name="users"
    )
    branch = models.ForeignKey(
        Branch, on_delete=models.SET_NULL, null=True, blank=True, related_name="users"
    )
    phone = models.CharField(max_length=30, blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()

    class Meta:
        ordering = ["email"]

    def __str__(self):
        return self.email

    @property
    def is_auditor(self):
        return self.role == "auditor"

    @property
    def can_approve(self):
        return self.role in ("super_admin", "it_manager", "finance_manager", "department_head")

    @property
    def can_edit_finance(self):
        return self.role in ("super_admin", "finance_manager", "accounts_officer")

    @property
    def can_edit_assets(self):
        return self.role in ("super_admin", "it_manager", "it_staff")

    @property
    def can_view_all(self):
        return self.role in ("super_admin", "it_manager", "finance_manager", "auditor")

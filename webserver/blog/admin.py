from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models import Comment, Post

from typing import Set

from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

admin.site.unregister(User)


@admin.register(User)
class CustomUserAdmin(UserAdmin):

  def get_form(self, request, obj=None, **kwargs):
    form = super().get_form(request, obj, **kwargs)
    is_superuser = request.user.is_superuser
    disabled_fields = set()  # type: Set[str]

    if not is_superuser:
      disabled_fields |= {
          'username',
          'is_superuser',
          'user_permissions',
      }

    # Prevent non-superusers from editing their own permissions
    if (not is_superuser and obj is not None and obj == request.user):
      disabled_fields |= {
          'is_staff',
          'is_superuser',
          'groups',
          'user_permissions',
      }

    for f in disabled_fields:
      if f in form.base_fields:
        form.base_fields[f].disabled = True

    return form


class PostAdmin(SummernoteModelAdmin):
  list_display = ("title", "slug", "status", "created_on")
  list_filter = ("status", "created_on")
  search_fields = ["title", "content"]
  prepopulated_fields = {"slug": ("title", )}

  summernote_fields = ("content", )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
  list_display = ("name", "body", "post", "created_on", "active")
  list_filter = ("active", "created_on")
  search_fields = ("name", "email", "body")
  actions = ["approve_comments"]

  def approve_comments(self, request, queryset):
    queryset.update(active=True)


admin.site.register(Post, PostAdmin)

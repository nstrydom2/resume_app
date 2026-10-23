from django.contrib import admin

from .models import (
    Blog,
    Certificate,
    ContactProfile,
    Media,
    Portfolio,
    Skill,
    Testimonial,
    UserProfile,
)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "title")
    search_fields = ("user__username", "user__first_name", "user__last_name", "title")


@admin.register(ContactProfile)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("id", "timestamp", "name", "email", "service", "business_name")
    list_filter = ("service", "budget_range", "preferred_contact")
    search_fields = ("name", "email", "business_name", "message", "current_process")
    readonly_fields = ("timestamp",)
    fieldsets = (
        (
            "Contact",
            {
                "fields": (
                    "timestamp",
                    "name",
                    "email",
                    "business_name",
                    "preferred_contact",
                )
            },
        ),
        (
            "Inquiry",
            {
                "fields": (
                    "service",
                    "message",
                    "current_process",
                    "volume_frequency",
                    "desired_deadline",
                    "budget_range",
                )
            },
        ),
    )


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "role", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "role", "quote")


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "is_image")


@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "date", "is_featured", "is_demo", "is_active")
    list_filter = ("is_active", "is_featured", "is_demo")
    search_fields = ("name", "description", "technologies")
    readonly_fields = ("slug",)
    fieldsets = (
        (None, {"fields": ("name", "slug", "date", "description", "body", "image")}),
        (
            "Showcase",
            {
                "fields": (
                    "technologies",
                    "live_url",
                    "repository_url",
                    "is_featured",
                    "is_demo",
                    "is_active",
                )
            },
        ),
    )


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "author", "timestamp", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "description", "body", "author")
    readonly_fields = ("slug",)


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "title", "date", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "title", "description")


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "score", "is_key_skill")
    list_filter = ("is_key_skill",)
    search_fields = ("name",)

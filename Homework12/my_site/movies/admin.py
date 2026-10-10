from django.contrib import admin

from .models import Actor, Movie, Studio


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = (
        "title", "actors_list", "studio", "year", "status", "updated_at"
    )
    list_display_links = ("title",)
    list_editable = ("status",)

    ordering = ("title",)
    list_per_page = 10
    empty_value_display = "---"

    list_filter = (
        "status",
        ("studio", admin.RelatedOnlyFieldListFilter),
        "created_at",
    )
    search_fields = ("title", "^slug")

    fieldsets = (
        (None, {"fields": (("title", "slug"), "description")}),
        ("Деталі", {
            "classes": ("collapse",),
            "fields": (("year", "duration_min"), ("status", "studio"), "actors"),
        }),
    )
    readonly_fields = ("created_at",)

    actions = ["make_released"]

    def actors_list(self, obj):
        # obj = Movie
        my_actors = obj.actors.all()
        return ", ".join(a.full_name for a in my_actors) if my_actors else "--"

    @admin.action(description="Позначити як випущені")
    def make_released(self, request, queryset):
        queryset.update(status=Movie.Status.RELEASED)


@admin.register(Studio)
class StudioAdmin(admin.ModelAdmin):
    ...


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    ...
# Register your models here.

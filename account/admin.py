from django.contrib import admin
from .models import User , course , certificate ,TrainingCalendar , TestModel
from django.utils.safestring import mark_safe

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'profile_image_thumbnail', 'tc', 'bio', 'phone_number', 'social_media_links', 'website','linkedin','twitter','instagram','youtube','facebook','created_at', 'is_active', 'is_admin')
    search_fields = ('email', 'name')
    list_filter = ('is_admin', 'is_active')
    fieldsets = (
        ('User Credentials', {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('name', 'tc', 'bio', 'phone_number', 'social_media_links', 'website', 'linkedin','twitter','instagram','youtube','facebook','profile_image')}),
        ('Permissions', {'fields': ('is_admin', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'tc', 'bio', 'phone_number', 'social_media_links','linkedin','twitter','instagram','youtube','facebook','website', 'profile_image', 'password1', 'password2'),
        }),
    )
    ordering = ('email', 'id')
    filter_horizontal = ()

    def profile_image_thumbnail(self, obj):
        if obj.profile_image:
            return mark_safe(f'<img src="{obj.profile_image.url}" height="50px" />')
        else:
            return ''
    profile_image_thumbnail.short_description = 'Profile Image'
    profile_image_thumbnail.allow_tags = True


admin.site.register(course)
admin.site.register(certificate)
admin.site.register(TrainingCalendar)
admin.site.register(TestModel)
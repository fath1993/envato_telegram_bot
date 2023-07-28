from django.contrib import admin

from custom_logs.models import CustomLog


@admin.register(CustomLog)
class CustomLogAdmin(admin.ModelAdmin):
    using = 'log_db'

    list_display = (
        'created_at_display',
        'description_display',
        'log_level',
    )

    readonly_fields = (
        'created_at',
    )
    list_filter = (
        'log_level',
    )

    search_fields = (
        'description',
    )

    fields = (
        'description',
        'log_level',
        'created_at',
    )

    @admin.display(description="تاریخ ایجاد", empty_value='???')
    def created_at_display(self, obj):
        data_time = str(obj.created_at.strftime('%y-%m-%d - %H:%M:%S %Z'))
        return data_time

    @admin.display(description="خلاصه", empty_value='???')
    def description_display(self, obj):
        description_summary = str(obj.description[:150])
        return description_summary

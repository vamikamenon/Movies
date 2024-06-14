from django.contrib import admin
from .models import Movies,Details,Category

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Movies)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Details)
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Tag, Scope


class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        super().clean()
        
        # Проверяем, что есть хотя бы одна форма
        forms = [f for f in self.forms if not f.cleaned_data or not f.deleted]
        main_count = sum(1 for f in forms if f.cleaned_data.get('is_main'))
        
        if main_count != 1:
            raise ValidationError('У каждой статьи должен быть ровно один основной раздел.')
        return super().clean()


class ScopeInline(admin.TabularInline):
    model = Scope
    formset = ScopeInlineFormset
    extra = 1


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ScopeInline]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass

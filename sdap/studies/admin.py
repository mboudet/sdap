from django.contrib import admin
from django import forms
from .models import *
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin
import sdap.tools.forms as tool_forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.apps import apps

class ExpressionStudyAdmin(admin.ModelAdmin, DynamicArrayMixin):
    fieldsets = [
        (None,               {'fields': ['article', 'pmid', 'ome', 'technology', 'species', 'experimental_design', 'topics', 'tissues', 'sex',
                                        'dev_stage', 'age', 'antibody', 'mutant', 'cell_sorted', 'keywords', 'samples_count', 'data'
                                        ]
                             }
        ),
    ]

class ExpressionDataAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['name', 'file',
                                        ]
                             }
        ),
    ]



admin.site.register(ExpressionStudy, ExpressionStudyAdmin)
admin.site.register(ExpressionData, ExpressionDataAdmin)




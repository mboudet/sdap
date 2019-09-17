from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout
from crispy_forms.bootstrap import FormActions

class default_form(forms.Form):

    job_name = forms.CharField(label='Job_name', max_length=100)

    def __init__(self, *args, **kwargs):

        self.arguments = kwargs.pop('arguments', None)
        super(default_form, self).__init__(*args, **kwargs)

        if self.arguments:
            for argument in self.arguments.all():
                if argument.user_filled:
                    if argument.argument_type.type == "Text":
                        self.fields[argument.label] = forms.CharField(label="{} ({})".format(argument.label, argument.parameter), max_length=100)
                    if argument.optional:
                        self.fields[argument.label].required = False

        self.helper = FormHelper(self)
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('save', 'Submit job'))

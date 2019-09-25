from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout
from crispy_forms.bootstrap import FormActions

from django.core.validators import MaxValueValidator, MinValueValidator
from .models import File, Folder


class VisualisationArgumentForm(forms.Form):

    def __init__(self, *args, **kwargs):

        visu_type = kwargs.pop('visu_type', False)
        table = kwargs.pop('table', False)
        super(VisualisationArgumentForm, self).__init__(*args, **kwargs)

        if visu_type and (visu_type == "Pieplot" or visu_type == "Barplot"):
            self.fields['Yvalues'] = forms.IntegerField(validators=[
                MaxValueValidator(len(table.index)),
                MinValueValidator(0)
            ])

        self.helper = FormHelper(self)
        self.helper.form_id= "visualization_form"
        self.helper.form_method = 'POST'

class FileCreateForm(forms.ModelForm):

    folder = forms.ModelChoiceField(Folder.objects.all(), empty_label="/", required=False)

    class Meta:
        model = File
        fields = ["name", "description", "type", "file", "folder","tags"]
        labels = {
            "name": "Name of the file",
            "description": "A short description of the file",
            "type": "Type of the file",
            "folder": "This file will be placed in this folder",
            "tags":"File annotation",
        }

    def __init__(self, *args, **kwargs):
        self.current_folder = kwargs.pop('current_folder', None)
        self.folders = kwargs.pop('folders', None)

        super(FileCreateForm, self).__init__(*args, **kwargs)

        if self.folders:
            self.fields['folder'].queryset = self.folders
            if self.current_folder:
                self.fields['folder'].initial = self.current_folder

        self.helper = FormHelper(self)
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('save', 'Save'))

class FolderCreateForm(forms.ModelForm):

    folder = forms.ModelChoiceField(Folder.objects.all(), empty_label="/", required=False)

    class Meta:
        model = Folder
        fields = ["name", "folder"]
        labels = {
            "name": "Name of the file",
            "folder": "Containing folder",
        }

    def __init__(self, *args, **kwargs):
        self.current_folder = kwargs.pop('current_folder', None)
        self.folders = kwargs.pop('folders', None)

        super(FolderCreateForm, self).__init__(*args, **kwargs)

        if self.folders:
            self.fields['folder'].queryset = self.folders
            if self.current_folder:
                self.fields['folder'].initial = self.current_folder

        self.helper = FormHelper(self)
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('save', 'Save'))


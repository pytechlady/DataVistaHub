from django import forms


class DataForm(forms.Form):
    data_set = forms.FileField(label="Data File", required=True, error_messages={
        'required': "Please upload a csv file"})
    set_x = forms.CharField(widget=forms.Select(choices=()), required=False, label="X-axis")
    set_y = forms.CharField(widget=forms.Select(choices=()), required=False, label="Y-axis")
    title = forms.CharField(max_length=200, label="Title")
    

    def __init__(self, *args, **kwargs):
        super(DataForm, self).__init__(*args, **kwargs)
        self.fields['set_x'].widget.choices = []
        self.fields['set_y'].widget.choices = []


class FormSubmit(forms.Form):
    data_set = forms.FileField(label="Data File", required=True, error_messages={
        'required': "Please upload a csv file"})
    x_axis = forms.CharField(widget=forms.Select(choices=()), required=False, label="X-axis")
    title = forms.CharField(max_length=200, label="Title")
    
    def __init__(self, *args, **kwargs):
        super(FormSubmit, self).__init__(*args, **kwargs)
        self.fields['x_axis'].widget.choices = []
        

class DailyReturnForm(forms.Form):
    data_set = forms.FileField(label="Data File", required=True, error_messages={
        'required': "Please upload a csv file"})
    x_axis = forms.CharField(widget=forms.Select(choices=()), required=False, label="X-axis")
    title = forms.CharField(max_length=200, label="Title")
    
    def __init__(self, *args, **kwargs):
        super(FormSubmit, self).__init__(*args, **kwargs)
        self.fields['x_axis'].widget.choices = []


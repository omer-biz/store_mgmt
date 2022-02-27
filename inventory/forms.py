from django import forms

from inventory.models import Employee

class CheckOutForm(forms.Form):
    employee = forms.ModelChoiceField(queryset=Employee.objects.all(), label="Employee", widget=forms.Select)
    quantity = forms.IntegerField(label="How Many")

    def clean(self):
        super(CheckOutForm, self).clean()

        quantity = self.cleaned_data.get('quantity')
        if quantity <= 0:
            self._errors['quantity'] = self.error_class([
                'Quantity can not be less than or equal to 0'
            ])

        return self.cleaned_data
    

class CheckInForm(forms.Form):
    quantity = forms.IntegerField(label="How Many")

    def clean(self):
        super(CheckInForm, self).clean()

        quantity = self.cleaned_data.get('quantity')
        if quantity <= 0:
            self._errors['quantity'] = self.error_class([
                'Quantity can not be less than or equal to 0'
            ])

        return self.cleaned_data

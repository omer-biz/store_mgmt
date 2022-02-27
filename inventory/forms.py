from django import forms

from inventory.models import Employee, OrderByEmployee

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

class OrderForm(forms.ModelForm):
    ordered_by = forms.ModelChoiceField(
        queryset=Employee.objects.all(),
        widget=forms.Select,
        label="Ordered By",
    )
    secret_key = forms.CharField(label="Secret Key", widget=forms.PasswordInput)
    class Meta:
        model = OrderByEmployee
        fields = ("name", "description",)

    
    def clean(self):
        super(OrderForm, self).clean()

        employee = self.cleaned_data.get('ordered_by')
        secret_key = self.cleaned_data.get('secret_key')

        if employee.secret_key != secret_key:
            self._errors['secret_key'] = self.error_class([
                f"Wrong secrect key for {employee}"
            ])

        return self.cleaned_data

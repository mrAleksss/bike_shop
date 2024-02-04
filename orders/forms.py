import re
from django import forms


class CreateOrderForm(forms.Form):

    first_name = forms.CharField()
    last_name = forms.CharField()
    phone = forms.CharField()
    requires_delivery = forms.ChoiceField(choices=[
            ("0", False),
            ("1", True),
        ])
    delivery_address = forms.CharField(required=False)
    payment_on_get = forms.ChoiceField(choices=[
            ("0", False),
            ("1", True),
        ])
    
    # change 12 on 10 after migrations make
    def clean_phone(self):
        data = self.cleaned_data['phone']

        if not data.isdigit():
            raise forms.ValidationError('Номер телефону має містити лише цифри')
        
        pattern = re.compile(r'^\d{12}$')
        if not pattern.match(data):
            raise forms.ValidationError('Невірний формат номера, має бути 12 цифр')
        
        return data

    # first_name = forms.CharField(
    #     widget=forms.TextInput(
    #         attrs={
    #             'class': 'form-control',
    #             'placeholder': "Введіть ваше ім'я"
    #         }
    #     )
    # )

    # last_name = forms.CharField(
    #     widget=forms.TextInput(
    #         attrs={
    #             'class': 'form-control',
    #             'placeholder': 'Введіть ваше прізвище'
    #         }
    #     )
    # )

    # phone = forms.CharField(
    #     widget=forms.TextInput(
    #         attrs={
    #             'class': 'form-control',
    #             'placeholder': 'Номер телефону'
    #         }
    #     )
    # )

    # requires_delivery = forms.ChoiceField(
    #     widget=forms.RadioSelect(),
    #     choices=[
    #         ("0", False),
    #         ("1", True)
    #     ],
    #     initial=0,
    # )

    # delivery_address = forms.CharField(
    #     widget=forms.Textarea(
    #         attrs={
    #             'class': 'form-control',
    #             'id': 'delivery_address',
    #             'rows': 2,
    #             'placeholder': 'Введіть адресу доставки'
    #         }
    #     ),
    #     required=False,
    # )

    # payment_on_get = forms.ChoiceField(
    #     widget=forms.RadioSelect(),
    #     choices=[
    #         ("0", False),
    #         ("1", True)
    #     ],
    #     initial='card',
    # )

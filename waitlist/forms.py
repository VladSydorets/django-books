from django import forms


class WaitlistForm(forms.Form):
    email = forms.EmailField(
        label='Email Address',
        max_length=254,
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'})
    )

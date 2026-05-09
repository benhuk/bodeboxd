from django import forms


class UsernameForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        label="Seu usuário do Letterboxd",
        widget=forms.TextInput(attrs={
            "placeholder": "ex: nysnarc",
            "autofocus": True,
        }),
    )


class CompatibilidadeForm(forms.Form):
    username1 = forms.CharField(
        max_length=100,
        label="Primeiro usuário",
        widget=forms.TextInput(attrs={"placeholder": "ex: nysnarc", "autofocus": True}),
    )
    username2 = forms.CharField(
        max_length=100,
        label="Segundo usuário",
        widget=forms.TextInput(attrs={"placeholder": "ex: outro_user"}),
    )

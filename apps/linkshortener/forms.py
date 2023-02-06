from django import forms


class LinkshortenerCreateForm(forms.Form):
    link = forms.URLField(label='Shorten your link:', required=True)
    subpart = forms.CharField(label='Your subpart', required=False, min_length=6, max_length=6)

    link.widget.attrs['class'] = 'form-control'
    link.widget.attrs['autofocus'] = 'autofocus'
    subpart.widget.attrs['class'] = 'form-control'

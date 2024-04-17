from django import forms
from .models import Contact


class ImageUploadForm(forms.Form):
    image = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'id': 'id_image'}),
        required=False
    )
    quality = forms.IntegerField(
        initial=75,
        min_value=1,
        max_value=100,
        help_text="Set the quality of the image"
    )
    output_format = forms.ChoiceField(
        choices=[('JPEG', 'JPEG'), ('PNG', 'PNG')],
        help_text="Select format of the image."
    )
    width = forms.IntegerField(min_value=1, required=False)
    height = forms.IntegerField(min_value=1, required=False)
    resize_percentage = forms.IntegerField(initial=75, min_value=1, max_value=100, required=False,
                                           label="Resize Percentage:"
                                           )
    resize_mode = forms.ChoiceField(
        choices=[('crop', 'Crop'), ('stretch', 'Stretch'), ('fit', 'Fit')],
        required=False,
    )
    # Anahtar açık olduğunda 'True', kapalıyken 'False' değeri alacak
    is_manual_resize = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'manual-resize-toggle', 'id': 'manual-resize-toggle'}))


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'content']

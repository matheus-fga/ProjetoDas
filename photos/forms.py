from django import forms
from photos.models import Image

class ImageForm(forms.ModelForm):

	class Meta:
		model = Image
		fields = ('image', 'description')
		exclude = ['user']
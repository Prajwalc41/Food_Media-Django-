from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['dish_name', 'image', 'caption']
        widgets = {
            'dish_name': forms.TextInput(attrs={
                'placeholder': 'e.g., Butter Chicken, Tiramisu...',
                'id': 'id_dish_name'
            }),
            'caption': forms.Textarea(attrs={
                'placeholder': 'Tell the story behind this dish... (optional)',
                'rows': 4,
                'id': 'id_caption',
                'maxlength': 500
            }),
            'image': forms.FileInput(attrs={'accept': 'image/jpeg,image/png,image/webp', 'id': 'id_image'}),
        }
        labels = {
            'dish_name': 'Dish Name',
            'image': 'Dish Photo',
            'caption': 'Caption (optional)',
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if image.size > 5 * 1024 * 1024:
                raise forms.ValidationError('Image must be under 5MB.')
            ext = image.name.split('.')[-1].lower()
            if ext not in ['jpg', 'jpeg', 'png', 'webp']:
                raise forms.ValidationError('Only JPG, PNG, and WEBP images are allowed.')
        return image


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'placeholder': 'Share your thoughts on this dish...',
                'rows': 3,
                'maxlength': 500,
                'id': 'id_comment_text'
            })
        }
        labels = {'text': ''}

from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from .models import CustomUser
import re


class EnthusiastRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'id': 'id_password_ent'}),
        label='Password'
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'id': 'id_confirm_password_ent'}),
        label='Confirm Password'
    )
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = ['full_name', 'username', 'email', 'profile_picture', 'bio']
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Full Name'}),
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email Address'}),
            'bio': forms.Textarea(attrs={'placeholder': 'Tell us about yourself... (optional)', 'rows': 3}),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            raise forms.ValidationError('Username may only contain letters, numbers, and underscores.')
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError('This username is already taken.')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already registered.')
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError('Password must be at least 8 characters.')
        if not any(char.isdigit() for char in password):
            raise forms.ValidationError('Password must contain at least one number.')
        return password

    def clean_profile_picture(self):
        picture = self.cleaned_data.get('profile_picture')
        if picture:
            if picture.size > 2 * 1024 * 1024:
                raise forms.ValidationError('Profile picture must be under 2MB.')
            ext = picture.name.split('.')[-1].lower()
            if ext not in ['jpg', 'jpeg', 'png', 'webp']:
                raise forms.ValidationError('Only JPG, PNG, and WEBP images are allowed.')
        return picture

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', 'Passwords do not match.')
        return cleaned_data


class RestaurantRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'id': 'id_password_res'}),
        label='Password'
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'id': 'id_confirm_password_res'}),
        label='Confirm Password'
    )
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = ['full_name', 'username', 'email', 'profile_picture', 'bio', 'restaurant_address', 'contact_number']
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Restaurant Name'}),
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email Address'}),
            'bio': forms.Textarea(attrs={'placeholder': 'Describe your restaurant... (optional)', 'rows': 3}),
            'restaurant_address': forms.TextInput(attrs={'placeholder': 'Full Address (e.g., 123 Main St, Bangalore)'}),
            'contact_number': forms.TextInput(attrs={'placeholder': 'Contact Number'}),
        }
        labels = {
            'full_name': 'Restaurant Name',
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            raise forms.ValidationError('Username may only contain letters, numbers, and underscores.')
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError('This username is already taken.')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already registered.')
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError('Password must be at least 8 characters.')
        if not any(char.isdigit() for char in password):
            raise forms.ValidationError('Password must contain at least one number.')
        return password

    def clean_profile_picture(self):
        picture = self.cleaned_data.get('profile_picture')
        if picture:
            if picture.size > 2 * 1024 * 1024:
                raise forms.ValidationError('Profile picture must be under 2MB.')
            ext = picture.name.split('.')[-1].lower()
            if ext not in ['jpg', 'jpeg', 'png', 'webp']:
                raise forms.ValidationError('Only JPG, PNG, and WEBP images are allowed.')
        return picture

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', 'Passwords do not match.')
        return cleaned_data


class EnthusiastProfileEditForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = ['full_name', 'profile_picture', 'bio']
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Full Name'}),
            'bio': forms.Textarea(attrs={'placeholder': 'Tell us about yourself...', 'rows': 4}),
        }

    def clean_profile_picture(self):
        picture = self.cleaned_data.get('profile_picture')
        if picture and hasattr(picture, 'size'):
            if picture.size > 2 * 1024 * 1024:
                raise forms.ValidationError('Profile picture must be under 2MB.')
            ext = picture.name.split('.')[-1].lower()
            if ext not in ['jpg', 'jpeg', 'png', 'webp']:
                raise forms.ValidationError('Only JPG, PNG, and WEBP images are allowed.')
        return picture


class RestaurantProfileEditForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = ['full_name', 'profile_picture', 'bio', 'restaurant_address', 'contact_number']
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Restaurant Name'}),
            'bio': forms.Textarea(attrs={'placeholder': 'Describe your restaurant...', 'rows': 4}),
            'restaurant_address': forms.TextInput(attrs={'placeholder': 'Full Address'}),
            'contact_number': forms.TextInput(attrs={'placeholder': 'Contact Number'}),
        }
        labels = {
            'full_name': 'Restaurant Name',
        }

    def clean_profile_picture(self):
        picture = self.cleaned_data.get('profile_picture')
        if picture and hasattr(picture, 'size'):
            if picture.size > 2 * 1024 * 1024:
                raise forms.ValidationError('Profile picture must be under 2MB.')
            ext = picture.name.split('.')[-1].lower()
            if ext not in ['jpg', 'jpeg', 'png', 'webp']:
                raise forms.ValidationError('Only JPG, PNG, and WEBP images are allowed.')
        return picture

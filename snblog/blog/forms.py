from django import forms


from .models import User, Post, Comment


class UserEditForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ('username','email', 'first_name', 'last_name')


class CreatePostForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = ('title', 'text', 'category', 'location', 'pub_date', 'image')
        widgets = {
            'pub_date': forms.DateInput(attrs={'type': 'date'})
        }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)
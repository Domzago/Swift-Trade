from django import forms
from . models import Item, Conversation, ConversationMessage

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = '__all__'

class MessageForm(forms.ModelForm):
    class Meta:
        model = ConversationMessage
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'w-full rounded border py-4'
            })
        }
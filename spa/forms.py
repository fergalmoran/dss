from crispy_forms.bootstrap import FormActions
from crispy_forms.layout import  Submit, Fieldset, Layout
from django import forms
from django.contrib.auth.models import User

from django.forms.models import ModelForm
from crispy_forms.helper import FormHelper
from spa.models.UserProfile import UserProfile

class UserForm(ModelForm):
    avatar_image_select = forms.ChoiceField(
        choices=(
            ('gravatar', "Use gravatar image."),
            ('social', "Use Twitter/Facebook image."),
            ('custom', "Use custom image (upload below).")
            ),

        label="Avatar Image",
        widget=forms.RadioSelect,
        initial='option_gravatar',
        help_text="Select the source of your avatar image."
    )
    avatar_image = forms.ImageField(
        label="",
        required=False
    )

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'User details',
                'display_name',
                'email',
                'first_name',
                'last_name',
                'avatar_image_select',
                'avatar_image'
            ),
            FormActions(
                Submit('save_changes', 'Save changes', css_class="btn-primary"),
                Submit('cancel', 'Cancel'),
            )
        )

        self.helper.form_class = 'form-horizontal'
        self.helper.form_id = 'id-new-user-form'

        self.helper.form_method = 'post'
        self.helper.form_error_title = 'Ooopsies'
        self.helper.formset_error_title = 'Ooopsies'

        self.helper.form_show_errors = True

    def save(self, *args, **kwargs):
        user = super(UserForm, self).save(*args, **kwargs)
        profile = UserProfile.objects.filter(user=user)[0]
        if profile is None:
            profile = UserProfile()

        profile.user = user
        profile.avatar_type = self.cleaned_data['avatar_image_select']
        profile.avatar_image = self.cleaned_data['avatar_image']
        # and so on with the remaining fields
        profile.save()
        return profile


from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import RBACUser, Role, UserRole


from rbac.models import Role, UserRole

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=[
        ('Student', 'Student'),
        ('Public', 'Public'),
    ]) 

    class Meta:
        model = RBACUser
        fields = ['username', 'email', 'password1', 'password2', 'role']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.set_password(self.cleaned_data['password1'])  # Hash the password

        if commit:
            user.save()
            # Fetch the Role instance
            role_name = self.cleaned_data['role']
            try:
                role_instance = Role.objects.get(role_name=role_name)
                # Assign the role to the UserRole table
                UserRole.objects.create(user=user, role=role_instance)
                # Add the role to the user's ManyToMany field
                user.roles.add(role_instance)
            except Role.DoesNotExist:
                raise ValueError(f"Role '{role_name}' does not exist. Ensure roles are set up in the database.")
        
        return user

class AssignRoleForm(forms.Form):
    user = forms.ModelChoiceField(queryset=RBACUser.objects.all(), required=True)
    role = forms.ModelChoiceField(queryset=Role.objects.all(), required=True)

    def save(self):
        user = self.cleaned_data['user']
        role = self.cleaned_data['role']
        user.roles.add(role)
        user.save()

class DeleteUserForm(forms.Form):
    user = forms.ModelChoiceField(queryset=RBACUser.objects.all(), label="Select a user to delete")
from datetime import datetime, timedelta

from self import self
from django import forms
from .models import Customer, Item, Bid
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, ReadOnlyPasswordHashField
from bootstrap_datepicker_plus import DateTimePickerInput
from django.forms import ValidationError

# create customer form
class CustomerCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = Customer
        fields = (
        "username", "first_name", "last_name", "email", "mobile_num", "street_address", "city", "state", "zipcode")
        # fields =("email","mobile_num","street_address","city","state","zipcode")

# edit customer details form
class CustomerEditProfileForm(UserChangeForm):
    password = ReadOnlyPasswordHashField(
        label=("Password"),
        help_text=(
            "<span class='text-white'>Click here to change your password </span>"
            "<u><a class='text-white' href=\"../password_change/\">Change My Password</a></u>."
        ),
    )

    class Meta:
        model = Customer
        fields = ("first_name", "last_name", "email", "mobile_num", "street_address", "city", "state", "zipcode")

    def __init__(self, *args, **kwargs):
        super(CustomerEditProfileForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['email'].widget.attrs['readonly'] = True

# form for customer item details
class CustomerItemsForm(forms.ModelForm):
    # comments = forms.CharField(label=False)
    class Meta:
        model = Item
        fields = ("name", "price", "start_date", "image", "comments",)
        widgets = {
            'comments': forms.Textarea(attrs={'placeholder': 'tell about the item..', 'rows': 5, }),
            'price': forms.TextInput(attrs={'placeholder': 'In dollars($)', }),
            'start_date': DateTimePickerInput,
        }

    def clean_start_date(self):
        start_date = self.cleaned_data['start_date']
        print('start_date', start_date)
        start_date = start_date.replace(tzinfo=None)
        print('start_date', start_date)
        now = datetime.today()
        now = now.replace(second=0, microsecond=0)
        print('now', now)
        if start_date < now:
            raise ValidationError('Start Date should be current or future time')
        return start_date

# form for editing customers items
class CustomerEditItemsForm(forms.ModelForm):
    # comments = forms.CharField(label=False)
    class Meta:
        model = Item
        fields = ("name", "price", "start_date", "end_date", "image", "comments",)
        widgets = {
            'comments': forms.Textarea(attrs={'placeholder': 'tell about the item..', 'rows': 5, }),
        }

    def __init__(self, *args, **kwargs):
        super(CustomerEditItemsForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['price'].widget.attrs['readonly'] = True
            self.fields['start_date'].widget.attrs['readonly'] = True
            self.fields['end_date'].widget.attrs['readonly'] = True

# form for reposting customer items
class CustomerRepostItemsForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ("name", "price", "start_date", "image", "comments",)
        widgets = {
            'comments': forms.Textarea(attrs={'placeholder': 'tell about the item..', 'rows': 5, }),
            'start_date': DateTimePickerInput,
            'price': forms.TextInput(attrs={'placeholder': 'In dollars($)', }),
        }

    def __init__(self, *args, **kwargs):
        super(CustomerRepostItemsForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['name'].widget.attrs['readonly'] = True

    def clean_start_date(self):
        cleaned_data = super(CustomerRepostItemsForm, self).clean()
        start_date = cleaned_data.get('start_date')
        print('start_date', start_date)
        start_date = start_date.replace(tzinfo=None)
        print('start_date', start_date)
        msg = 'Start Date should be current or future time'
        if start_date < datetime.today():
            raise ValidationError (msg)
        return cleaned_data

# form for customer bids details
class CustomerBidsForm(forms.ModelForm):
    # comments = forms.CharField(label=False)
    class Meta:
        model = Bid
        fields = ("amount",)
        widgets = {
            'amount': forms.TextInput(attrs={'placeholder': 'In dollars($)',})
        }

    def __init__(self, *args, **kwargs):
        self.identifier = kwargs.pop('identifier', None)
        super(CustomerBidsForm, self).__init__(*args, **kwargs)

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        maxBid = Bid.objects.filter(item_id=self.identifier.id).order_by('-time').first()
        if maxBid is None:
            if amount.__lt__(self.identifier.price):
                raise ValidationError('Price must be greater than the Original Price', self.identifier.price)
        else:
            if amount.__lt__(self.identifier.price) or amount.__le__(maxBid.amount):
                raise ValidationError('Price must be greater than the Original Price  and latest amount bid',
                                      self.identifier.price)

        return amount



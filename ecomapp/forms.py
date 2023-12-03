from django import forms
from .models import Order,Customer,Product
from django.contrib.auth.models import User


class CheckoutForm(forms.ModelForm):
    class Meta:
        model=Order
        fields=['ordered_by','shipping_address','mobile','email']
        widgets={
            'ordered_by':forms.TextInput(attrs={
                'class':'form-control'  
            }),
            'shipping_address':forms.TextInput(attrs={
                'class':'form-control'
            }),
             'mobile':forms.TextInput(attrs={
                'class':'form-control'
            }),
             'email':forms.TextInput(attrs={
                'class':'form-control'
            }),
        }




class CustomerRegistrationForm(forms.ModelForm):
    username=forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control'
    }))
    password=forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'form-control'
    }))
    email=forms.CharField(widget=forms.EmailInput(attrs={
        'class':'form-control'
    }))
    full_name=forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control'
    }))
    address=forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control'
    }))


    class Meta:
        model=Customer 
        fields=['username','password','email','full_name','address']
        
    def clean_username(self):
        uname=self.cleaned_data.get('username')
        if User.objects.filter(username=uname).exists():
            raise forms.ValidationError('Đã tồn tại username này!')
        return uname
    def clean_email(self):
        email=self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Đã tồn tại email này!')
        return email
    
class CustomerLoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'Nhập username'
    }))
    password=forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'form-control',
        'placeholder':'Nhập password'
    }))

    

class ProductForm(forms.ModelForm):
   
    class Meta:
        model=Product
        fields=['title','slug','category','image','marked_price','selling_price','description','warranty','return_policy']
        widgets={
            'title':forms.TextInput(attrs={
                'class':'form-control'
                
            }),
            'slug':forms.TextInput(attrs={
                'class':'form-control'
            }),
            'category':forms.Select(attrs={
                'class':'form-control'
            }),
            'image':forms.ClearableFileInput(attrs={ 

                # 'multiple':False
            }),
            'marked_price':forms.NumberInput(attrs={
                'class':'form-control'
            }),
            'selling_price':forms.NumberInput(attrs={
                'class':'form-control'
            }),
            'description':forms.Textarea(attrs={
                'class':'form-control',
                'rows': 5
            }),
            'warranty':forms.TextInput(attrs={
                'class':'form-control'
            }),
            'return_policy':forms.TextInput(attrs={
                'class':'form-control'
            }),
        }

class PasswordForgotForm(forms.Form):
    email=forms.CharField(widget=forms.EmailInput(attrs={
        'class':'form-control',
        'placeholder':'Nhập email ...'
    }))

    def clean_email(self):
        e=self.cleaned_data.get('email')
        if Customer.objects.filter(user__email=e).exists():
            pass
        else:
            raise forms.ValidationError('Không tồn tại tài khoản có email này.')

        return e
    
class PasswordResetForm(forms.Form):
    new_password=forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'form-control',
        'autocomplete':'new-password',
        'placeholder':'Enter new Password',
    }), label='New password')
    confirm_new_password=forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'form-control',
        'autocomplete':'new-password',
        'placeholder':'Confirm New Password',
    }),label='Confirm New Password')

    def clean_confirm_new_password(self):
        new_password=self.cleaned_data.get('new_password')
        confirm_new_password=self.cleaned_data.get('confirm_new_password')

        if new_password != confirm_new_password:
            raise forms.ValidationError('Mật khẩu không trùng nhau!')
        return confirm_new_password
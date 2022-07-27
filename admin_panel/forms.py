from django import forms
from store. models import products
from category. models import category

class add_product(forms.ModelForm):
    class Meta:
        model=products
        fields=['product_name','description','category','price','count','size','color','company','gender','discount']
        def _init_(self,args,*kwargs) :
            super(add_product,self)._init_(args,*kwargs)
            self.fields['product_name'].widget.attrs['placeholder'] = 'Enter product Name'
            self.fields['description'].widget.attrs['placeholder'] = 'description'
            self.fields['category'].widget.attrs['placeholder'] = 'Category'
            self.fields['price'].widget.attrs['placeholder'] = 'Price'
            self.fields['count'].widget.attrs['placeholder'] = 'Count'
            self.fields['size'].widget.attrs['placeholder'] = 'Size'
            self.fields['color'].widget.attrs['placeholder'] = 'Color'
            self.fields['company'].widget.attrs['placeholder'] = 'Company'
            self.fields['gender'].widget.attrs['placeholder'] = 'gender'
            self.fields['discount'].widget.attrs['placeholder'] = 'discount'


            for field in self.fields:
                
                self.fields[field].widget.attrs['class']='form-control'
            
class edit_product(forms.ModelForm):
    class Meta:
        model=products
        fields=['product_name','description','category','price','count','size','color','company','gender','discount']

        
    def _init_(self,args,*kwargs):
        super(edit_product,self)._init_(args,*kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'
            # self.fields['is_available'].widget.attrs['class'] =''
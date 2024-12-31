from django import forms
from django.core.cache import cache
from .models import Configs, Committeecalendarinused, Committeebranch, Profile, Location, Gender, Profilerole, Role, Office, OfficeRole, Zone, Committee, Committeesupportlocation, Committeecalendar, CustomUser
from django_select2.forms import Select2Widget, ModelSelect2Widget
from django.core.exceptions import ValidationError
#from django_jalali.forms import jDateTimeField
from jalali_date.fields import JalaliDateField, SplitJalaliDateTimeField, JalaliDateTimeField
from jalali_date.widgets import AdminJalaliDateWidget, AdminSplitJalaliDateTime
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from datetime import datetime
from django.utils.timezone import make_aware




class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'

    location = forms.ModelChoiceField(
        queryset= Location.objects.all(),     
        widget = ModelSelect2Widget (
                model = Location,
                search_fields = ['name__icontains'],
                attrs = {'class': 'form-control'}
            ),
        required=False
    )

    gender = forms.ChoiceField(
        choices=[],  # We'll set choices dynamically in __init__
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        user = getattr(self, 'current_user', None)
        #print(user)

        if user:

            prov = (
    Location.objects.filter(id=getattr(user, 'province', None)).values().first()
    or
    Location.objects.filter(id=getattr(user, 'location', None)).values().first()
)

            print('prov>>>>>>>>>>>>>>>>>',prov)

            # Check if prov is not None (to avoid errors in the next steps)
            if prov is not None:
                # Fetch the 'parentid' from the prov dictionary
                parent_id = prov.get('parentid')
                parent_id1 = prov.get('id')  # Use the appropriate key as per your model
                print('parentid>>>>',parent_id)
                print('parent_id1>>>>',parent_id1)
                # Ensure that parentid is an integer (if it is not null)
                if parent_id is not None or parent_id1 is not None:
                    self.fields['location'].queryset = Location.objects.filter(
                                Q(parentid=parent_id) | Q(parentid=parent_id1)
                            )
                else:
                    # Handle case when parentid is None as needed
                    self.fields['location'].queryset = Location.objects.none()  # No valid queryset
            else:
                # Handle case when no matching province was found
                self.fields['location'].queryset = Location.objects.all()  # No valid queryset

        self.fields['location'].label = 'شهر/استان'
        self.fields['gender'].label = 'جنسیت'
        self.fields['username'].label = 'نام کاربری'
        self.fields['NATIONALID'].required = True
        self.fields['firstname'].required = True
        self.fields['lastname'].required = True
        self.fields['username'].required = True
        self.fields['password'].required = True
        self.fields['force_password_change'].required = True
        self.fields['force_profile_completion'].required = True
        self.fields['usertype'].required = True
        self.fields['gender'].required = True
        self.fields['mobilenumber'].required = True
        self.fields['location'].required = True
        

        # Cache key for genders
        gender_cache_key = 'gender_choices'
        # Try to get cached data
        gender_choices = cache.get(gender_cache_key)
        if gender_choices is None:
            # If not cached, fetch from database
            gender_choices = [
                (gen.id, gen.name) for gen in Gender.objects.all()
            ]
            # Cache the fetched data
            cache.set(gender_cache_key, gender_choices, timeout=3600)  # Cache for 1 hour
        self.fields['gender'].choices = gender_choices


    def clean_location(self):
        location = self.cleaned_data['location']
        if location:
            if not Location.objects.filter(id=location.id).exists():
                raise forms.ValidationError("Invalid location selected.")
            return location.id
        return None

    def clean_gender(self):
        gender_id = self.cleaned_data['gender']
        if gender_id:
            try:
                gender_id = int(gender_id)
                if not Gender.objects.filter(id=gender_id).exists():
                    raise forms.ValidationError("Invalid gender selected.")
                return gender_id
            except ValueError:
                raise forms.ValidationError("Invalid gender selected.")
        return None
    

class ProfileRoleForm(forms.ModelForm):
    class Meta:
        model = Profilerole
        fields = '__all__'  # Include all fields or specify a list of fields
        # widgets = {
        #     'role': ModelSelect2Widget (
        #         model = Role,
        #         search_fields = ['name__icontains'],
        #         attrs = {'class': 'form-control'}
        #     ),
        
        # }

    profile = forms.ModelChoiceField(
        queryset=Profile.objects.all(),
        required=False,
        empty_label="Select PROFILE"
    )

    role = forms.ModelChoiceField(
        queryset=Role.objects.all(),
        widget = ModelSelect2Widget (
                model = Role,
                search_fields = ['name__icontains'],
                attrs = {'class': 'form-control'}
            ),
        required=False,
        empty_label="انتخاب نقش..."
    )


class CommitteeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['office'].label = 'اداره'

    class Meta:
        model = Committee
        fields = '__all__'  # Include all fields or specify a list of fields
        widgets = {
            'office': ModelSelect2Widget (
                model = Office,
                search_fields = ['name__icontains'],
                attrs = {'class': 'form-control'}
            ),
        
        }

    # office = forms.ModelChoiceField(
    #     queryset=Office.objects.all(),
    #     required=False,
    #     widget=forms.Select(attrs={'class': 'form-control'})
    # )

    office = forms.ModelChoiceField(
        queryset= Office.objects.all(),        
        widget = ModelSelect2Widget (
                model = Office,
                search_fields = ['name__icontains'],
                attrs = {'class': 'form-control'}
            ),
        required=False
    )

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        user = getattr(self, 'current_user', None)
        print('current_user>',user)

        self.fields['office'].label = 'اداره'
        

        if user:
            prov = (
                Location.objects.filter(id=getattr(user, 'province', None)).values().first()
                or
                Location.objects.filter(id=getattr(user, 'location', None)).values().first()
            )

            if prov is not None:
                #print('prov>>>', prov)
                parent_id = prov.get('id')
                #print('parent_id>>>', parent_id)
                if parent_id is not None:
                    parent_office = Office.objects.filter(location_id=parent_id).values().first()
                    #print('parent_office>>>', parent_office.get('id'))
                    self.fields['office'].queryset = Office.objects.filter(Q(parentid=parent_office.get('id')) | Q(location_id=parent_id))
                    #self.fields['location'].queryset = Location.objects.filter(id=user.province)
                else:
                    self.fields['office'].queryset = Office.objects.all()
            else:
                self.fields['office'].queryset = Office.objects.all()


class OfficeForm(forms.ModelForm):
    class Meta:
        model = Office
        fields = '__all__'  # Include all fields or specify a list of fields
           

    office = forms.ModelChoiceField(
        queryset=Office.objects.all(),
        widget = ModelSelect2Widget (
                model = Office,
                search_fields = ['name__icontains'],
                attrs = {'class': 'form-control'}
            ),
        required=False,
        empty_label="انتخاب اداره..."
    )

    committee = forms.ModelChoiceField(
        queryset=Committee.objects.all(),
        widget = ModelSelect2Widget (
                model = Committee,
                search_fields = ['name__icontains'],
                attrs = {'class': 'form-control'}
            ),
        required=False,
        empty_label="انتخاب کمیته..."
    )

    office_role = forms.ChoiceField(
        choices=[(off.id, off.description) for off in OfficeRole.objects.all()],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        user = getattr(self, 'current_user', None)
        print('current_user>',user)

        if user:
            prov = (
    Location.objects.filter(id=getattr(user, 'province', None)).values().first()
    or
    Location.objects.filter(id=getattr(user, 'location', None)).values().first()
)

            #print('prov>>>', prov)
            if prov is not None:
                parent_id = prov.get('id')
                #print('parent_id>>>', parent_id)
                if parent_id is not None:
                    parent_office = Office.objects.filter(location_id=parent_id).values().first()
                    #print('parent_office>>>', parent_office.get('id'))
                    self.fields['office'].queryset = Office.objects.filter(Q(parentid=parent_office.get('id')) | Q(location_id=parent_id))
                    self.fields['committee'].queryset = Committee.objects.filter(office__in=self.fields['office'].queryset)
                    #self.fields['location'].queryset = Location.objects.filter(id=user.province)
                else:
                    self.fields['office'].queryset = Office.objects.all()
                    self.fields['committee'].queryset = Committee.objects.all()
            else:
                self.fields['office'].queryset = Office.objects.all()
                self.fields['committee'].queryset = Committee.objects.all()



    # zone_id = forms.ChoiceField(
    #     choices=[('', 'Select Zone')],  # Add an empty choice
    #     required=False,
    #     widget=forms.Select(attrs={'class': 'form-control'})
    # )

    # location_id = forms.ChoiceField(
    #     choices=[('', 'Select Location')],  # Add an empty choice
    #     required=False,
    #     widget=forms.Select(attrs={'class': 'form-control'},)
    # )

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

    #     # Cache key for locations
    #     location_cache_key = 'location_choices'
    #     # Try to get cached data
    #     location_choices = cache.get(location_cache_key)
    #     if location_choices is None:
    #         # If not cached, fetch from database
    #         location_choices = [
    #             (loc.id, f"{loc.name} ({loc.get_parent().name if loc.get_parent() else 'No Parent'})")
    #             for loc in Location.objects.filter(parentid__isnull=False)
    #         ]
    #         # Cache the fetched data
    #         cache.set(location_cache_key, location_choices, timeout=3600)  # Cache for 1 hour
    #     self.fields['location_id'].choices += location_choices

    #     # Cache key for zones
    #     zone_cache_key = 'zone_choices'
    #     # Try to get cached data
    #     zone_choices = cache.get(zone_cache_key)
    #     if zone_choices is None:
    #         # If not cached, fetch from database
    #         zone_choices = [
    #             (zone.city_id, f"{zone.city_name} ({zone.municipality_name})") for zone in Zone.objects.all()
    #         ]
    #         # Cache the fetched data
    #         cache.set(zone_cache_key, zone_choices, timeout=3600)  # Cache for 1 hour
    #     self.fields['zone_id'].choices += zone_choices

    # def clean_location_id(self):
    #     location_id = self.cleaned_data['location_id']
    #     if location_id:
    #         try:
    #             location_id = int(location_id)
    #             if not Location.objects.filter(id=location_id).exists():
    #                 raise forms.ValidationError("Invalid location selected.")
    #             return location_id
    #         except ValueError:
    #             raise forms.ValidationError("Invalid location selected.")
    #     return None

    # def clean_office_role(self):
    #     office_role = self.cleaned_data['office_role']
    #     if office_role:
    #         try:
    #             office_role = int(office_role)
    #             if not OfficeRole.objects.filter(id=office_role).exists():
    #                 raise forms.ValidationError("Invalid office role selected.")
    #             return office_role
    #         except ValueError:
    #             raise forms.ValidationError("Invalid office role selected.")
    #     return None

    # def clean_zone_id(self):
    #     zone_id = self.cleaned_data['zone_id']
    #     if zone_id:
    #         try:
    #             zone_id = int(zone_id)
    #             if not Zone.objects.filter(city_id=zone_id).exists():
    #                 raise forms.ValidationError("Invalid zone selected.")
    #             return zone_id
    #         except ValueError:
    #             raise forms.ValidationError("Invalid zone selected.")
    #     return None


class CommitteesupportlocationForm(forms.ModelForm):
    class Meta:
        model = Committeesupportlocation
        fields = '__all__'


    location = forms.ModelChoiceField(
        queryset= Location.objects.all(),        
        widget = ModelSelect2Widget (
                model = Location,
                search_fields = ['name__icontains'],
                attrs = {'class': 'form-control'}
            ),
        required=False
    )

    zone = forms.ModelChoiceField(
        queryset= Zone.objects.all(),        
        widget = ModelSelect2Widget (
                model = Zone,
                search_fields = ['name__icontains'],
                attrs = {'class': 'form-control'}
            ),
        required=False
    )

    def clean_location(self):
        location = self.cleaned_data.get('location')
        if location:
            return location.id  # return the ID to be saved in the model
        return None
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.location_id = self.cleaned_data.get('location')  # or set a relevant field
        if commit:
            instance.save()
        return instance
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = getattr(self, 'current_user', None)
        print('current_user>',user)
        self.fields['location'].label = 'شهر/استان'
        self.fields['zone'].label = 'منطقه شهرداری'

        if user:
            prov = (
    Location.objects.filter(id=getattr(user, 'province', None)).values().first()
    or
    Location.objects.filter(id=getattr(user, 'location', None)).values().first()
)

            print('prov>>>', prov)
            if prov is  not None:
                parent_id = prov.get('id')
                print('parent_id>>>', parent_id)
                if parent_id is None:
                    self.fields['location'].queryset = Location.objects.filter(parentid=parent_id)
                    self.fields['zone'].queryset = Zone.objects.filter(location__in = Location.objects.filter(parentid=parent_id).values_list('id', flat=True))
                else:
                    self.fields['zone'].queryset = Zone.objects.all()
            else:
                self.fields['zone'].queryset = Zone.objects.all()


class ZoneForm(forms.ModelForm):
    class Meta:
        model = Zone
        fields = '__all__'

    location = forms.ModelChoiceField(
        queryset= Location.objects.all(),        
        widget = ModelSelect2Widget (
                model = Location,
                search_fields = ['name__icontains'],
                attrs = {'class': 'form-control'}
            ),
        required=False
    )

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        user = getattr(self, 'current_user', None)
        print('current_user>',user)

        if user:
            prov = Location.objects.filter(id=user.province).values().first()
            print('prov>>>', prov)
            parent_id = prov.get('id')
            print('parent_id>>>', parent_id)
            self.fields['location'].queryset = Location.objects.filter(parentid=parent_id)


class CommitteecalendarForm(forms.ModelForm):


    class Meta:
        model = Committeecalendar
        fields = '__all__'

    branch = forms.ModelChoiceField(
        queryset= Committeebranch.objects.all(),     
        widget = ModelSelect2Widget (
                model = Committeebranch,
                search_fields = ['name__icontains'],
                attrs = {'class': 'form-control'}
            ),
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['branch'].label = 'شعبه'

        self.fields['used_times'] = forms.CharField(
            label="Used Times",
            required=False,
            widget=forms.Textarea(attrs={'readonly': 'readonly', 'class': 'form-control'}),
        )

        # Populate the 'used_times' field with values
        if self.instance and self.instance.pk:
            # Query the Committeecalendarinused table
            used_times = Committeecalendarinused.objects.filter(
                committeecalendar=self.instance.pk
            ).values_list('usedmeetingdate', flat=True)

            # Format the dates for display
            formatted_times = [ut.strftime('%Y-%m-%d %H:%M:%S') for ut in used_times if ut]
            self.fields['used_times'].initial = "\n".join(formatted_times)

    def clean(self):
        cleaned_data = super().clean()
        availabledate = cleaned_data.get('availabledate')
        committeecalendar_obj = cleaned_data.get('id')  # This will be the Committeecalendar object

        if committeecalendar_obj:
            committeecalendar_id = committeecalendar_obj.pk
            # Retrieve the original object from the database
            try:
                original_obj = Committeecalendar.objects.get(pk=committeecalendar_id)
            except Committeecalendar.DoesNotExist:
                original_obj = None

            if original_obj:
                # Check if restricted fields are being changed
                # if (
                #     availabledate != original_obj.availabledate
                #     and availabledate <= datetime.now()
                # ):
                #     raise forms.ValidationError("این تقویم استفاده شده است و امکان ویرایش ندارد")

                if Committeecalendarinused.objects.filter(committeecalendar=committeecalendar_id).exists():
                    
                    # Check if other fields are being modified
                    restricted_fields = ['availabledate']
                    for field in restricted_fields:
                        if cleaned_data.get(field) != getattr(original_obj, field):
                            raise forms.ValidationError("این تقویم استفاده شده است و امکان ویرایش ندارد")
                        
        try:
            start_time_config = Configs.objects.get(config_name='CC_START_TIME')
            end_time_config = Configs.objects.get(config_name='CC_END_TIME')

            start_time_str = '0' + start_time_config.config_value  # Add leading 0 if necessary
            end_time_str = end_time_config.config_value

            # Parse the start and end times as datetime objects (only the hour part matters)
            start_time = datetime.strptime(start_time_str, "%H")  # Assuming format is HH:MM
            end_time = datetime.strptime(end_time_str, "%H")  # Assuming format is HH:MM

            # Convert to timezone-aware datetimes
            start_time = make_aware(start_time)
            end_time = make_aware(end_time)

            # Ensure availabledate is timezone-aware (if it's naive, make it aware)
            if availabledate and availabledate.tzinfo is None:
                availabledate = make_aware(availabledate)

            # Extract only the hour from availabledate, start_time, and end_time
            available_hour = availabledate.hour if availabledate else None
            start_hour = start_time.hour
            end_hour = end_time.hour

            # If availabledate has changed, perform validation
            if committeecalendar_obj and availabledate and availabledate != committeecalendar_obj.availabledate:
                # Check if the availabledate's hour is between the start_hour and end_hour
                if available_hour < start_hour or available_hour > end_hour:
                    raise ValidationError(
                        f"زمان انتخابی میبایست بین ساعات {start_hour} و {end_hour} باشد"
                    )

        except Configs.DoesNotExist:
            raise ValidationError("Configuration for start and end time is missing.")

        return cleaned_data
    #     # Use AdminJalaliDateTimeWidget for datetime input
    #     self.fields['availabledate'] = forms.DateField(
    #         label='تاریخ های در دسترس'
    #     )

        # Add a class for custom styling to date input
        #self.fields['availabledate'].widget.attrs.update({'class': 'jalali_date-date'})

        # # If you need to explicitly separate date and time fields:
        # self.fields['availabledate'] = JalaliDateField(
        #     label='تاریخ',
        #     widget=AdminJalaliDateWidget(
        #         attrs={'class': 'jalali_date-date'}  # Date picker widget
        #     ),
        # )

        # self.fields['availabledate'] = forms.TimeField(
        #     label='زمان',
        #     widget=forms.TimeInput(attrs={'class': 'jalali_date-time'})  # Time picker widget
        # )


class CustomUserForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput, required=False)

    class Meta:
        model = CustomUser
        fields = '__all__'

    province = forms.ModelChoiceField(
        queryset= Location.objects.all(),        
        widget = ModelSelect2Widget (
                model = Location,
                search_fields = ['name__icontains'],
                attrs = {'class': 'form-control'}
            ),
        required=False
    )

    def __init__(self, *args, **kwargs):

        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            allowed_locations = [group.name.split('-')[1] for group in user.groups.all() if group.name.startswith('CanCreateUser-')]
            self.fields['province'].queryset = Location.objects.filter(name__in=allowed_locations)

        self.fields['province'].label = 'شهر/استان'

    def clean_province(self):
        province = self.cleaned_data['province']
        if province:
            if not Location.objects.filter(id=province.id).exists():
                raise forms.ValidationError("Invalid location selected.")
            return province.id
        return None
    
    def save(self, commit=True):
        user = super().save(commit=False)
        # If a new password has been entered, set it
        if self.cleaned_data['password']:
            user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class CustomUserAddForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'province')

    province = forms.ModelChoiceField(
        queryset= Location.objects.all(),        
        widget = ModelSelect2Widget (
                model = Location,
                search_fields = ['name__icontains'],
                attrs = {'class': 'form-control'}
            ),
        required=False
    )


    def __init__(self, *args, **kwargs):

        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            # Filter locations based on user's group
            allowed_locations = [
                group.name.split('-')[1]
                for group in user.groups.all()
                if group.name.startswith('CanCreateUser-')
            ]
            self.fields['province'].queryset = Location.objects.filter(name__in=allowed_locations)

        self.fields['province'].label = 'شهر/استان'

    def clean_province(self):
        province = self.cleaned_data['province']
        if province:
            if not Location.objects.filter(id=province.id).exists():
                raise forms.ValidationError("Invalid location selected.")
            return province.id
        return None
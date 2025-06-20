from django.contrib.auth.forms import AuthenticationForm


class CustomLoginForm(AuthenticationForm):
    """Authentication form with Bootstrap styling and accessibility support."""

    BASE_CSS_CLASS = 'form-control'
    BACKGROUND_CLASS = 'bg-secondary bg-opacity-50'
    BORDER_CLASS = 'border-secondary'

    def __init__(self, *args, **kwargs):
        """Initializes the login form with custom Bootstrap styles."""
        super().__init__(*args, **kwargs)

        bs_cls = (
            f'{self.BASE_CSS_CLASS} '
            f'{self.BACKGROUND_CLASS} '
            f'{self.BORDER_CLASS}'
        )
        
        for field_name, field in self.fields.items():
            existing_class = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = f'{existing_class} {bs_cls}'.strip()
            
            field.widget.attrs['placeholder'] = _(field.label)
            
            field.widget.attrs.update({
                'aria-label': _(field.label),
                'id': f'id_{field_name}'
            })

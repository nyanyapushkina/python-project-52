from task_manager.users.forms import (
    CustomUserChangeForm,
    CustomUserCreationForm,
)
from task_manager.users.models import User
from task_manager.users.tests.testcase import UserTestCase


class TestCustomUserCreationForm(UserTestCase):
    """Tests for user creation form validation."""
    
    SHORT_PASSWORD = '12'  # NOSONAR
    INVALID_PASSWORD_CONFIRM = 'Different123'  # NOSONAR
    LONG_USERNAME = 'x' * 151

    def get_form(self, overrides=None):
        """Return a pre-filled user creation form, optionally overridden."""
        data = self.valid_user_data.copy()
        if overrides:
            data.update(overrides)
        return CustomUserCreationForm(data=data)

    def test_valid_creation(self):
        """Test form with valid data."""
        form = self.get_form()
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.username, self.valid_user_data['username'])
        self.assertTrue(user.check_password(self.valid_user_data['password1']))
        self.assertEqual(User.objects.count(), self.initial_user_count + 1)

    def test_missing_required_fields(self):
        """Test validation when required fields are missing."""
        required_fields = ['username', 'password1', 'password2']
        
        for field in required_fields:
            with self.subTest(field=field):
                invalid_data = self.valid_user_data.copy()
                invalid_data.pop(field)
                form = CustomUserCreationForm(data=invalid_data)
                self.assertFalse(form.is_valid())
                self.assertIn(field, form.errors)

    def test_password_validation(self):
        """Test password validation scenarios."""
        test_cases = [
            (
                {'password1': self.SHORT_PASSWORD, 
                 'password2': self.SHORT_PASSWORD},
                'password2'
            ),
            (
                {'password1': 'ValidPass123', 
                 'password2': self.INVALID_PASSWORD_CONFIRM},  # NOSONAR
                'password2'
            ),
        ]

        for data, error_field in test_cases:
            with self.subTest(data=data):
                form = self.get_form(data)
                self.assertFalse(form.is_valid())
                self.assertIn(error_field, form.errors)

    def test_username_validation(self):
        """Test username format validation."""
        invalid_usernames = [
            '!!!',
            'user#name',
            'user name',
            self.LONG_USERNAME,
            '',  # empty
        ]

        for username in invalid_usernames:
            with self.subTest(username=username):
                form = self.get_form({'username': username})
                self.assertFalse(form.is_valid())
                self.assertIn('username', form.errors)

    def test_duplicate_username(self):
        """Test unique username validation."""
        form = self.get_form({'username': 
                              'queen_lucy'})  # Already exists in fixtures
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)


class TestCustomUserChangeForm(UserTestCase):
    """Tests for user change form validation."""
    
    NEW_VALID_PASSWORD = 'QueenInNorth456'  # NOSONAR
    SHORT_PASSWORD = '12'  # NOSONAR
    WRONG_CONFIRM = 'WrongConfirm'  # NOSONAR

    def get_form(self, overrides=None):
        """Return user change form with updated data."""
        data = {
            'username': 'updated_user',
            'first_name': 'Updated',
            'last_name': 'User',
            'password1': 'NewValidPass123',  # NOSONAR
            'password2': 'NewValidPass123'   # NOSONAR
        }
        if overrides:
            data.update(overrides)
        return CustomUserChangeForm(data=data, instance=self.user1)

    def test_valid_update(self):
        """Test successful user update."""
        form = self.get_form()
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.username, 'updated_user')
        self.assertTrue(user.check_password('NewValidPass123'))

    def test_password_update_validation(self):
        """Test password update scenarios."""
        test_cases = [
            (
                {'password1': self.SHORT_PASSWORD, 
                 'password2': self.SHORT_PASSWORD},
                'password2'
            ),
            (
                {'password1': 'ValidPass123', 
                 'password2': self.WRONG_CONFIRM},  # NOSONAR
                'password2'
            ),
            (
                {'password1': '', 'password2': 'ValidPass123'},  # NOSONAR
                '__all__'
            ),
        ]

        for data, error_field in test_cases:
            with self.subTest(data=data):
                form = self.get_form(data)
                self.assertFalse(form.is_valid())
                if error_field != '__all__':
                    self.assertIn(error_field, form.errors)

    def test_update_without_password_change(self):
        """Test form validation when password isn't being changed."""
        form = CustomUserChangeForm(
            data={
                'username': 'no_pass_change',
                'first_name': 'Test',
                'last_name': 'User'
            },
            instance=self.user1
        )
        self.assertTrue(form.is_valid())

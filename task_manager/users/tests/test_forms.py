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

    def test_valid_data(self):
        """Test form with valid data."""
        form = self.get_form()
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.username, self.valid_user_data['username'])
        self.assertTrue(user.check_password(self.valid_user_data['password1']))
        self.assertEqual(User.objects.count(), self.user_count + 1)


    def test_missing_fields(self):
        """Test form with missing required fields."""
        test_cases = [
            {'username': self.valid_user_data['username']},
            {
                'username': self.valid_user_data['username'],
                'password1': 'test123',  # NOSONAR
            },
            {'first_name': 'Test', 'last_name': 'User'},
        ]

        for data in test_cases:
            with self.subTest(data=data):
                form = CustomUserCreationForm(data=data)
                self.assertFalse(form.is_valid())

    def test_password_too_short(self):
        """Test password minimum length validation."""
        form = self.get_form({
            'password1': self.SHORT_PASSWORD,
            'password2': self.SHORT_PASSWORD
        })
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_invalid_username(self):
        """Test username format validation."""
        test_cases = [
            '!!!',
            'user#name',
            'user name',
            self.LONG_USERNAME,
        ]

        for username in test_cases:
            with self.subTest(username=username):
                form = self.get_form({'username': username})
                self.assertFalse(form.is_valid())
                self.assertIn('username', form.errors)

    def test_passwords_do_not_match(self):
        """Test password confirmation validation."""
        form = self.get_form({'password2': self.INVALID_PASSWORD_CONFIRM})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['password2'],
            ['The two password fields didn\'t match.']
        )

    def test_empty_strings(self):
        """Test empty required fields validation."""
        form = self.get_form({
            'first_name': '',
            'last_name': '',
            'username': '',
        })
        self.assertFalse(form.is_valid())
        for field in ['first_name', 'last_name', 'username']:
            self.assertIn(field, form.errors)

    def test_duplicate_username(self):
        """Test unique username validation."""
        form = self.get_form({'username': 'john_snow'})
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)


class TestCustomUserChangeForm(UserTestCase):
    """Tests for user change form validation."""
    
    NEW_VALID_PASSWORD = 'QueenInNorth456'  # NOSONAR
    SHORT_PASSWORD = '12'  # NOSONAR
    WRONG_CONFIRM = 'WrongConfirm'  # NOSONAR

    def get_form(self, overrides=None):
        """Return user change form with updated data and passwords."""
        data = self.update_user_data.copy()
        data.update({
            'password1': data.pop('password1'),
            'password2': data.pop('password2')
        })
        if overrides:
            data.update(overrides)
        return CustomUserChangeForm(data=data, instance=self.user1)

    def test_valid_password_update(self):
        """Test successful password update."""
        form = self.get_form()
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.username, self.update_user_data['username'])
        self.assertTrue(user.check_password(
            self.update_user_data['password1']
        ))

    def test_passwords_do_not_match(self):
        """Test password confirmation validation."""
        form = self.get_form({'password2': self.WRONG_CONFIRM})
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_short_password(self):
        """Test password minimum length validation."""
        form = self.get_form({
            'password1': self.SHORT_PASSWORD,
            'password2': self.SHORT_PASSWORD
        })
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_missing_password_fields(self):
        """Test partial password fields validation."""
        test_cases = [
            {'password1': '', 'password2': 'SomePassword'},  # NOSONAR
            {'password1': 'SomePassword', 'password2': ''}   # NOSONAR
        ]

        for case in test_cases:
            with self.subTest(case=case):
                form = self.get_form(case)
                self.assertFalse(form.is_valid())
                self.assertTrue(
                    'password1' in form.errors or 'password2' in form.errors
                )

    def test_update_with_existing_valid_password(self):
        """Test password update with new valid password."""
        form = self.get_form({
            'password1': self.NEW_VALID_PASSWORD,
            'password2': self.NEW_VALID_PASSWORD,
        })
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertTrue(user.check_password(self.NEW_VALID_PASSWORD))

    def test_update_without_password_change(self):
        """Test form validation when password isn't being changed."""
        data = self.update_user_data.copy()
        data.pop('password1')
        data.pop('password2')
        form = CustomUserChangeForm(data=data, instance=self.user1)
        self.assertTrue(form.is_valid())

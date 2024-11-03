from django.test import TestCase

# Импорты для валидатора
from django.core.exceptions import ValidationError
from lms.validators import validate_youtube_url


# Тесты для проверки валидатора
class ValidatorTest(TestCase):

    def test_valid_youtube_url(self):
        # Проверяем валидную ссылку на YouTube
        valid_url = 'https://www.youtube.com/watch?v=abc123'
        try:
            validate_youtube_url(valid_url)
        except ValidationError:
            self.fail("Валидная ссылка YouTube вызвала ValidationError.")

    def test_invalid_url(self):
        # Проверяем невалидную ссылку (не YouTube)
        invalid_url = 'https://www.example.com'
        with self.assertRaises(ValidationError):
            validate_youtube_url(invalid_url)

    def test_shortened_youtube_url(self):
        # Проверяем валидную сокращённую ссылку на YouTube
        valid_url = 'https://youtu.be/abc123'
        try:
            validate_youtube_url(valid_url)
        except ValidationError:
            self.fail("Валидная сокращённая ссылка YouTube вызвала ValidationError.")

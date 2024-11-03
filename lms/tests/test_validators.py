import pytest
from django.core.exceptions import ValidationError
from lms.validators import validate_youtube_url


def test_valid_youtube_url():
    valid_url = 'https://www.youtube.com/watch?v=abc123'
    try:
        validate_youtube_url(valid_url)
    except ValidationError:
        pytest.fail("Valid YouTube URL raised ValidationError.")


def test_invalid_url():
    invalid_url = 'https://www.example.com'
    with pytest.raises(ValidationError):
        validate_youtube_url(invalid_url)


def test_shortened_youtube_url():
    valid_url = 'https://youtu.be/abc123'
    try:
        validate_youtube_url(valid_url)
    except ValidationError:
        pytest.fail("Valid shortened YouTube URL raised ValidationError.")

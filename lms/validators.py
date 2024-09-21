from django.core.exceptions import ValidationError
import re

def validate_youtube_url(value):
    """
    Проверяет, что ссылка принадлежит youtube.com.
    """
    youtube_pattern = r'(https?://)?(www\.)?(youtube|youtu\.be)(\.com)?/.+'
    if not re.match(youtube_pattern, value):
        raise ValidationError("Только ссылки на YouTube разрешены.")
    return value

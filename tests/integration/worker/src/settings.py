"""Конфиг."""

from functools import lru_cache

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Настройки приложения."""

    container: str = Field("integration")

    url: str = Field("http://localhost:8000/api/v1")

    # Публичный ключ для декодирования токенов авторизации.
    # Значение по умолчанию НЕ ДЛЯ ПРОДАКШЕНА - для локальных запусков.
    jwt_rsa_public_key: str = Field(
        """-----BEGIN RSA PUBLIC KEY-----
MIGJAoGBAM36n1r2gzKpHORp7zIt0lwQrQ7RZ6wfomIzP4oOulTACgAz8o8OfEWd
E4kNIEfIcSY9WfnHwapXmVD37qX3uN0QRw+jrCSyHJwzzZ+BzE6a+0DLhSjGr8B6
mViqmWFxRMZW6jhmV04uY3ySwabOFamw51PRuRiKkcKfmxZnF3bVAgMBAAE=
-----END RSA PUBLIC KEY-----""",
    )

    jwt_rsa_private_key: str = Field(
        """-----BEGIN RSA PRIVATE KEY-----
MIICXgIBAAKBgQDN+p9a9oMyqRzkae8yLdJcEK0O0WesH6JiMz+KDrpUwAoAM/KP
DnxFnROJDSBHyHEmPVn5x8GqV5lQ9+6l97jdEEcPo6wkshycM82fgcxOmvtAy4Uo
xq/AeplYqplhcUTGVuo4ZldOLmN8ksGmzhWpsOdT0bkYipHCn5sWZxd21QIDAQAB
AoGBAMJ0++KVXXEDZMpjFDWsOq898xNNMHG3/8ZzmWXN161RC1/7qt/RjhLuYtX9
NV9vZRrzyrDcHAKj5pMhLgUzpColKzvdG2vKCldUs2b0c8HEGmjsmpmgoI1Tdf9D
G1QK+q9pKHlbj/MLr4vZPX6xEwAFeqRKlzL30JPD+O6mOXs1AkEA8UDzfadH1Y+H
bcNN2COvCqzqJMwLNRMXHDmUsjHfR2gtzk6D5dDyEaL+O4FLiQCaNXGWWoDTy/HJ
Clh1Z0+KYwJBANqRtJ+RvdgHMq0Yd45MMyy0ODGr1B3PoRbUK8EdXpyUNMi1g3iJ
tXMbLywNkTfcEXZTlbbkVYwrEl6P2N1r42cCQQDb9UQLBEFSTRJE2RRYQ/CL4yt3
cTGmqkkfyr/v19ii2jEpMBzBo8eQnPL+fdvIhWwT3gQfb+WqxD9v10bzcmnRAkEA
mzTgeHd7wg3KdJRtQYTmyhXn2Y3VAJ5SG+3qbCW466NqoCQVCeFwEh75rmSr/Giv
lcDhDZCzFuf3EWNAcmuMfQJARsWfM6q7v2p6vkYLLJ7+VvIwookkr6wymF5Zgb9d
E6oTM2EeUPSyyrj5IdsU2JCNBH1m3JnUflz8p8/NYCoOZg==
-----END RSA PRIVATE KEY-----"""
    )

    # Настройки MongoDB
    mongo_dsn = Field("mongodb://localhost:27017")
    mongo_db = Field("ugc_movies")


@lru_cache()
def get_settings() -> Settings:
    """Фабрика настроек.

    Returns:
        Settings: Класс с настройками приложения.
    """
    return Settings()

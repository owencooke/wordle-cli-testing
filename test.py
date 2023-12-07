from unittest.mock import patch
import platform

class MockedPlatform:
    def __init__(self, release):
        self.release = release

def test_platform():
    return MockedPlatform("microsoft-standard-x.x.x-xxx")

with patch('platform.uname', return_value=test_platform()) as mock_uname:
    result = hasattr(platform.uname(), "release") and "microsoft-standard" in platform.uname().release

print(result)  # This should output True
import re
from django.core.exceptions import ValidationError
import math
from typing import Optional, Dict


SEQUENCE_PATTERNS = [
    "abcdefghijklmnopqrstuvwxyz",
    "qwertyuiopasdfghjklzxcvbnm",
    "0123456789",
]


class PasswordStrengthValidator:
    """
    this class is used to validate the strength of a password based on the following criteria:
    - Minimum length
    - Maximum length
    - Recommended length
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit
    - At least one special character
    - Maximum repetition of a character
    - Blacklist of common passwords
    The default values for these criteria can be overridden by passing in different values to the constructor.
    """

    def __init__(
        self,
        min_length: int = 8,
        max_length: int = 128,
        recomended_length: int = 12,
        required_upper: bool = True,
        required_lower: bool = True,
        required_digit: bool = True,
        required_special: bool = True,
        maximum_repetition: int = 3,
        blacklist: Optional[set] = None,
    ) -> None:
        self.min_length = min_length
        self.max_length = max_length
        self.recomended_length = recomended_length
        self.required_upper = required_upper
        self.required_lower = required_lower
        self.required_digit = required_digit
        self.required_special = required_special
        self.maximum_repetition = maximum_repetition
        self.blacklist = blacklist

    def char_class(self, password: str) -> Dict[str, int]:
        """
        This method returns a dictionary with the count of different character classes in the password.
        """
        counts = {
            "upper": len(re.findall(r"[A-Z]", password)),
            "lower": len(re.findall(r"[a-z]", password)),
            "digit": len(re.findall(r"\d", password)),
            "special": len(re.findall(r"[^A-Za-z0-9]", password)),
        }
        return counts

    def shannon_entropy(self, password: str) -> float:
        """
        This method calculates the Shannon entropy of the password.
        """
        if not password:
            return 0.0

        freq = {}
        for char in password:
            freq[char] = freq.get(char, 0) + 1
        entropy = 0.0
        length = len(password)
        for count in freq.values():
            p = count / length
            entropy -= p * math.log2(p)
        return entropy 

    def has_sequence(self, password: str, seq_length: int = 4) -> bool:
        """
        This method checks if the password contains any sequential characters of a given length.
        """
        if len(password) < seq_length:
            return False

        pw = password.lower()
        for pattern in SEQUENCE_PATTERNS:
            for i in range(len(pattern) - seq_length + 1):
                subseq = pattern[i : i + seq_length]
                if subseq in pw:
                    return True
                if subseq[::-1] in pw:
                    return True
        return False

    def has_consecutive_repeat(self, password: str) -> bool:
        """
        This method checks if the password contains more than the allowed maximum consecutive repeated characters.
        """
        max_run = 1
        run = 1
        for i in range(1, len(password)):
            if password[i] == password[i - 1]:
                run += 1
                if run > max_run:
                    max_run = run
            else:
                run = 1
        return max_run > self.maximum_repetition


    def check(self, password: str) -> list[str]:
        """
            Validate the password against all criteria and return a list of error messages (if any).
        """
        errors = []

        if len(password) < self.min_length or len(password) > self.max_length:
            errors.append(f"password length must be in range {self.min_length} - {self.max_length}")

        
        counts = self.char_class(password)
        if self.required_upper and counts["upper"] == 0:
            errors.append(f"Password must have at last 1 upper letter")
        if self.required_lower and counts["lower"] == 0:
            errors.append(f"Password must have at last 1 lower letter")
        if self.required_digit and counts["digit"] == 0:
            errors.append(f"Password must have at last 1 digit")
        if self.required_special and counts["special"] == 0:
            errors.append(f"Password must have at last 1 special character")

        if self.has_sequence(password):
            errors.append(f"This password have sequence.")

        if self.has_consecutive_repeat(password):
            errors.append(f"Password have consecutive_repeat") 

        entropy = self.shannon_entropy(password)
        if entropy < 3.5:
            errors.append(f"I think you can create a stronger password")

        return errors

    
    def validate(self, password: str) -> None:
        errors = self.check(password)
        if errors:
            raise ValidationError(errors)





        




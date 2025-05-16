from enum import Enum


class UserRole(str, Enum):
    USER = "USER"
    STUDENT = "STUDENT"
    TEACHER = "TEACHER"
    UNIVERSITY_ADMIN = "UNIVERSITY_ADMIN"

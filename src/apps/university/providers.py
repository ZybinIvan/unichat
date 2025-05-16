from dishka import Provider, Scope

from src.apps.university.repositories import UniversityRepository

university_provider = Provider(scope=Scope.REQUEST)
university_provider.provide(UniversityRepository)

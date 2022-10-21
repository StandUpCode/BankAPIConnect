from typing import TypeVar, Optional

from domain.base import Singleton

AdapterGetterType = TypeVar('AdapterGetterType')


def adapter_getter(adapter: AdapterGetterType) -> AdapterGetterType:
    if adapter:
        return adapter
    raise NotImplementedError()


def adapter_setter_value(attribute, value, adapter_name, type_, *, single_assign=False):
    if single_assign and attribute:
        raise ValueError(f"DomainRegistry.{adapter_name} is already set.")
    if isinstance(value, type_):
        return value

    raise TypeError(f"Expected {adapter_name} of type {type_.__name__}, got {type(value).__name__}")


class DomainRegistry(metaclass=Singleton):
    def __init__(self):
        from domain.model.SlipVerification import SlipVerificationService, SlipRepositoryAbstract

        self._slip_verification_service: Optional[SlipVerificationService] = None
        self._slip_repository: Optional[SlipRepositoryAbstract] = None

    def reset(self):
        self._slip_verification_service = None
        self._slip_repository = None

    def assign_defaults(self):
        from domain.model.SlipVerification import SlipVerificationService
        self._slip_verification_service = SlipVerificationService()

    @property
    def slip_verification_service(self):
        return adapter_getter(self._slip_verification_service)

    @slip_verification_service.setter
    def slip_verification_service(self, service):
        from domain.model.SlipVerification import SlipVerificationService
        self.slip_verification_service = adapter_setter_value(self._slip_verification_service, service,
                                                              'slip_verification_service', SlipVerificationService)

    @property
    def slip_repository(self):
        return adapter_getter(self._slip_repository)

    @slip_repository.setter
    def slip_repository(self, repository):
        from domain.model.SlipVerification import SlipRepositoryAbstract
        self._slip_repository = adapter_setter_value(self._slip_repository, repository,
                                                     'slip_repository', SlipRepositoryAbstract)

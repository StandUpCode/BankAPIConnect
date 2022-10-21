from domain.model.SlipVerification import SlipVerificationService
from domain.model.registry import DomainRegistry


def create_domain_registry(mongo_db):
    registry = DomainRegistry()
    registry.assign_defaults()

    registry.slip_verification_service = SlipVerificationService()

    return registry

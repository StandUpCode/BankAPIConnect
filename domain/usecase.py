from domain.model.registry import DomainRegistry


async def verify_silp(file):
    result = await DomainRegistry().slip_verification_service
    return result

from domain.base import transaction
from domain.model.SlipVerification import Slip
from domain.model.registry import DomainRegistry
from utils.slip import SlipQRData


class SlipVerificationService:
    def __init__(self):
        self.registry = DomainRegistry()

    async def verify(self, image):
        slip_data = SlipQRData.create_from_image(image)

        slip = Slip(
            qr_data=slip_data.payload
        )

        
        # await self._save_new_slip(slip)

    @transaction
    async def _save_new_slip(self, slip: Slip):
        return await self.registry.slip_repository.save(slip)

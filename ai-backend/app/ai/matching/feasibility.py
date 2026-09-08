from abc import ABC, abstractmethod

class BaseDeliveryFeasibilityProvider(ABC):
    @abstractmethod
    async def estimate_delivery_days(self, artisan_region: str, delivery_location: str, quantity: int, lead_time_days: int) -> int:
        pass

class MockDeliveryFeasibilityProvider(BaseDeliveryFeasibilityProvider):
    async def estimate_delivery_days(self, artisan_region: str, delivery_location: str, quantity: int, lead_time_days: int) -> int:
        # Mock logic: production lead time + 5 days transport
        # Region similarity could lower transport time, etc.
        transport_days = 5
        if artisan_region.lower() == delivery_location.lower():
            transport_days = 2
        return lead_time_days + transport_days

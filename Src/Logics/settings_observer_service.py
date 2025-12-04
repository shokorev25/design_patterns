from Src.Core.abstract_logic import abstract_logic
from Src.Core.observe_service import observe_service
from Src.Core.event_type import event_type
from Src.settings_manager import settings_manager

class settings_observer_service(abstract_logic):
    def __init__(self):
        super().__init__()
        observe_service.add(self)

    def handle(self, event: str, params):
        super().handle(event, params)
        if event == event_type.change_block_period():
            sm = settings_manager()
            sm.save()
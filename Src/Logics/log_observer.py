import datetime
import json
from Src.Core.abstract_logic import abstract_logic
from Src.Core.validator import validator
from Src.Core.log_level import log_level
from Src.Core.event_type import event_type

class log_observer(abstract_logic):
    __min_level = log_level.INFO
    __output = "console"
    __file_name = "system.log"

    def __init__(self, settings_file="settings.json"):
        super().__init__()
        self.__load_logging_settings(settings_file)

    def __load_logging_settings(self, settings_file: str):
        try:
            with open(settings_file, "r", encoding="utf-8") as f:
                settings = json.load(f)
                logging = settings.get("logging", {})

                min_level_str = logging.get("min_level", "INFO").upper()
                if min_level_str in log_level.__members__:
                    self.__min_level = log_level[min_level_str]

                self.__output = logging.get("output", "console")
                self.__file_name = logging.get("file_name", "system.log")

        except Exception as ex:
            self.set_exception(ex)

    def handle(self, event: str, params):
        super().handle(event, params)

        if event not in [event_type.log_debug(), event_type.log_info(), event_type.log_error()]:
            return

        level = params.get("level", log_level.INFO)
        message = params.get("message", "")
        context = params.get("context", {})

        if level.value < self.__min_level.value:
            return

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {level.name}: {message}"

        if isinstance(context, dict) and len(context) > 0:
            try:
                ctx = " | ".join([f"{k}={context[k]}" for k in context])
                log_entry += f" | {ctx}"
            except Exception:
                pass

        if self.__output == "console":
            return

        try:
            with open(self.__file_name, "a", encoding="utf-8") as f:
                f.write(log_entry + "\n")
        except Exception as ex:
            self.set_exception(ex)

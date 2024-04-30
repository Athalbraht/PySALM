import os
from typing import Protocol
from ai import Responses

from addons import read_file, fm
from conf import tex_config


class CommandTemplate(Protocol):
    def __init__(self, id: int, flg: str, kind: str, ctx: str, mode: str, loc: str, paraphrase : bool, responses : Responses, alias : str = 'NoName'):
        self.id = id
        self.paraphrase = paraphrase
        self.flg = flg
        self.kind = kind
        self.ctx = ctx
        self.mode = mode
        self.loc = loc
        if alias == "NoName":
            self.alias = ctx
        else:
            self.alias = alias
        self.calculated : bool = False
        self.payload : dict = {
            "%%LOC" : self.loc,
            "%%CAPTION%%" : "",
            "%%LABEL%%" : "",
            "%%COMMANDS%%" : "",
            "%%PREFRAME%%" : "",
            "%%POSTFRAME%%" : "",
        }
        self.responses : Responses = responses
        self.update_prompt("")

    def __repr__(self):
        return "{}:{}:{}:{}:{}".format(
            self.id,
            self.flg,
            self.kind,
            self.ctx,
            self.mode,
        )

    def get_payload(self):
        """Return result in tex format."""
        print("\t\t\t- Getting payload: {}: ".format(self.id), end="")
        try:
            if self.calculated:
                print(fm("Pass", "green"))
            else:
                raise BrokenPipeError(" Cannot return payload, not calculated yet")
        except Exception as e:
            print(fm("Fail", "red"), end="")
            print(" Cannot return payload, not calculated yet")
        else:
            return self.payload

    def execute(self):
        """Execute instructions and save to prepare payload later.

        should define self.payload & self.vars: dict
        self.vars = {
                "COMMAND" : xxx,
                "CAPTION" : YYY,
                "PAYLOAD" : ZZZ,
                ...
                }
        """
        ...

    def update_response(self, content : str):
        """Save paylod as csv entry."""
        self.responses.update_response(self.alias, content)

    def update_prompt(self, content : str):
        """Save paylod as csv entry."""
        self.responses.update_prompt(self.alias, content)

    def apply_payload(self, payload):
        if self.mode == 'global':
            mode = tex_config['ai']['mode']
        else:
            mode = self.mode

        if mode == 'static':
            if not self.responses.paraphrased(self.alias) and self.paraphrase:
                pass  # SEND TO AI
            response = self.responses.get_response(self.alias)
            if response == " ":
                self.update_response(payload)
                self.payload[tex_config["payload_alias"]] = payload
            else:
                self.payload[tex_config["payload_alias"]] = response

        elif mode == 'uniqe':
            if self.paraphrase:
                pass  # SEND TO AI
                self.responses.paraphrased(self.alias, True)
            response = self.responses.get_response(self.alias)
            self.update_response(payload)
            self.payload[tex_config["payload_alias"]] = payload


class UnsupportedCommand(CommandTemplate):
    def execute(*args, **kwargs) -> None:
        print("\t\t- Unsupported command, skipping...")
        raise Warning("Unsupported operation")
        return None


# available mode options
# - "random"       # choice randomly from database
# - "uniqe"        # always regenerate description
# - "global"       # use global setting
# - "static"       # AI support disabled, using default values
# - "paraphrase"   # paraphrase existing description

# example of reg command usage:
# register('gen', 'table', loc='pre', mode='global')

class GenCommand():
    def execute(self):
        ...

    def get_context(self):
        ...

    def get_prompt(self):
        ...

    def evaluate_prompt(self):
        ...


class FileCommand(CommandTemplate):
    def execute(self):
        payload = read_file(os.path.join(tex_config["assets_folder"], self.ctx))
        self.calculated = True
        self.apply_payload(payload)


class TableCommand(CommandTemplate):
    def execute(self):
        ...

class QueryCommand(CommandTemplate):
    def execute(self):
        ...


class StatisticCommand(CommandTemplate):
    def execute(self):
        ...




class PlotCommand(CommandTemplate):
    def execute(self):
        ...


class AICommand(CommandTemplate):
    def execute(self):
        ...

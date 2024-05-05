import os
from typing import Protocol

import tables
from addons import fm, read_file
from ai import Responses
from conf import tex_config
from plotting import plot, plot_power


class CommandTemplate(Protocol):
    def __init__(self, ai, powers, id: int, flg: str, kind: str, ctx: str, silent: bool, mode: str, loc: str, paraphrase : bool,
                 data, responses : Responses, kwargs, alias : str = 'NoName'):
        self.id = id
        self.ai = ai
        self.df = data
        self.paraphrase = paraphrase
        self.flg = flg
        self.kind = kind
        self.silent = silent
        self.ctx = ctx
        self.powers = powers
        self.mode = mode
        self.loc = loc
        self.additional_config = kwargs
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
        print("\t\t\t- Getting payload: {}: ".format(self.ctx), end="")
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

        if mode == 'static' or mode == 'safe':
            # if not self.responses.paraphrased(self.alias) and self.paraphrase:
            # pass  # SEND TO AI
            response = self.responses.get_response(self.alias)
            if response == " ":
                if self.kind == 'desc' and mode != 'safe':
                    payload = self.ai.request(payload)
                self.update_response(payload)
                self.payload[tex_config["payload_alias"]] = payload
            else:
                self.payload[tex_config["payload_alias"]] = response

        elif mode == 'uniqe':
            if self.paraphrase:
                pass  # SEND TO AI
                self.responses.paraphrased(self.alias, True)
            # response = self.responses.get_response(self.alias)
            payload = self.ai.request(payload)
            self.update_response(payload)
            self.payload[tex_config["payload_alias"]] = payload

        if self.silent:
            self.payload[tex_config["payload_alias"]] = ""
            self.mode = 'desc'
            self.flg = 'gendesc'


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


class PowerTableCommand(CommandTemplate):
    def execute(self):
        table, desc = tables.powertable(self.powers)
        self.calculated = True
        self.responses.update_desc(self.alias, desc)
        self.apply_payload(table)


class DescTableCommand(CommandTemplate):
    def execute(self):
        table, desc = tables.desctable(self.df[self.ctx])
        self.calculated = True
        self.responses.update_desc(self.alias, desc)
        self.apply_payload(table)


class ExpandTableCommand(CommandTemplate):
    def execute(self):
        table, desc = tables.expandtable(self.df, self.ctx)
        self.calculated = True
        self.responses.update_desc(self.alias, desc)
        self.apply_payload(table)


class CountTableCommand(CommandTemplate):
    def execute(self):
        table, desc = tables.counttable(self.df, self.ctx)
        self.calculated = True
        self.responses.update_desc(self.alias, desc)
        self.apply_payload(table)


class CrossTableCommand(CommandTemplate):
    def execute(self):
        table, desc = tables.desctable(self.df[self.ctx])
        self.calculated = True
        self.responses.update_desc(self.alias, desc)
        self.apply_payload(table)


class DescCommand(CommandTemplate):
    def execute(self):
        desc = self.responses.get_desc(self.ctx)
        self.calculated = True
        self.apply_payload(desc)


class CorrCommand(CommandTemplate):
    def execute(self):
        table, desc = tables.corrtab(self.ctx)
        self.calculated = True
        self.responses.update_desc(self.alias, desc)
        self.apply_payload(table)


class AutoStatCommand(CommandTemplate):
    def execute(self):
        table, desc = tables.stattab(self.ctx)
        self.calculated = True
        self.responses.update_desc(self.alias, desc)
        self.apply_payload(table)


class PowerPlotCommand(CommandTemplate):
    def execute(self):
        path, desc, caption = plot_power()
        self.calculated = True
        self.responses.update_desc(self.alias, desc)
        self.payload["%%CAPTION%%"] = caption
        self.payload["%%SCALE%%"] = "1"
        path = '/'.join(path.split('/')[-2::])
        self.payload[tex_config["payload_alias"]] = path


class PlotCommand(CommandTemplate):
    def execute(self):
        path, desc, caption = plot(self.df, self.ctx, alias=self.alias, **self.additional_config.get('plot', {}))
        self.calculated = True
        self.responses.update_desc(self.alias, desc)
        self.payload["%%CAPTION%%"] = caption
        self.payload["%%SCALE%%"] = "1"
        path = '/'.join(path.split('/')[-2::])
        self.payload[tex_config["payload_alias"]] = path


class CustomCommand(CommandTemplate):
    def execute(self):
        self.calculated = True
        self.payload[tex_config["payload_alias"]] = self.ctx


class QueryCommand(CommandTemplate):
    def execute(self):
        ...


class StatCorrCommand(CommandTemplate):
    def execute(self):
        ...


class StatTestCommand(CommandTemplate):
    def execute(self):
        ...


class AICommand(CommandTemplate):
    def execute(self):
        ...

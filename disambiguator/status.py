from enum import Enum


class Status(Enum):
    OK = 1
    WARNING = 2
    ERROR = -1
    ERROR_NO_INSTRUCTION = -2
    ERROR_NOT_INSTRUCTION = -3
    ERROR_NO_BT_LIST = -4
    ERROR_NO_BT = -5
    ERROR_PARSE_XML = -6
    ERROR_NO_INTENTS = -7
    ERROR_LLM = -8
    ERROR_NOT_PATTERN = -9
    ERROR_NOT_PARSE = -10
    ERROR_NO_STEPS = -11
    ERROR_TOO_LARGE_BT_LIST = -12
    ERROR_NO_BT_LISTS = -13


# 对应的status_info
status_info = {
    Status.OK: "",
    Status.WARNING: "Unknown warning",
    Status.ERROR: "An unknown error has occurred",
    Status.ERROR_NO_INSTRUCTION: "No user command input detected",
    Status.ERROR_NOT_INSTRUCTION: "Input language is not a control command",
    Status.ERROR_NO_BT_LIST: "BT_LIST parsing failure",
    Status.ERROR_NO_BT: "BT parsing failure",
    Status.ERROR_PARSE_XML: "XML parsing error",
    Status.ERROR_NO_INTENTS: "No Intents detected from the command",
    Status.ERROR_LLM: "Failure to invoke a large language model(LLM)",
    Status.ERROR_NOT_PATTERN: "No conforming regular expression matches user input",
    Status.ERROR_NOT_PARSE: "It doesn't parse anything",
    Status.ERROR_NO_STEPS: "Don't properly decompose instruction into steps",
    Status.ERROR_TOO_LARGE_BT_LIST: "Too many parsed BT_LIST",
    Status.ERROR_NO_BT_LISTS: "BT_LISTS parsing failure"
}

import uuid
from typing import Literal, TypedDict


class Origin(TypedDict):
    type: str


class CommandRequest(TypedDict):
    commandLine: str
    version: int
    overWorld: Literal["overWorld"]
    origin: Origin


class Header(TypedDict):
    requestID: str
    messagePurpose: str
    messageType: str
    version: int


class Packet(TypedDict):
    header: Header
    body: CommandRequest


def new_command_request(command_line: str) -> Packet:
    return {
        "header": {
            "requestId": str(uuid.uuid4()),
            "messagePurpose": "commandRequest",
            "messageType": "commandRequest",
            "version": 1,
        },
        "body": {
            "commandLine": command_line,
            "version": 1,
            "overWorld": "overWorld",
            "origin": {"type": "player"},
        },
    }

from typing import TypedDict
from typing_extensions import Annotated

from langgraph.graph import add_messages

class OverallState(TypedDict):
    messages: Annotated[list, add_messages]



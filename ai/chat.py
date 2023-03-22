import logging
from typing import Callable, Generator, Optional

from openai.api_resources.chat_completion import ChatCompletion

from .config import settings


class Conversation:
    def __init__(
        self,
        system_message: Optional[str] = None,
        temperature: float = 1.0,
        max_tokens: Optional[int] = None,
    ) -> None:
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.messages = []
        if system_message is not None:
            self.messages.append({"role": "system", "content": system_message})

    def call_chatapi(self, user_message: str) -> Generator[str, None, None]:
        self.messages.append({"role": "user", "content": user_message})
        response = ChatCompletion.create(
            api_key=settings.openai_api_key,
            model="gpt-3.5-turbo",
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            messages=self.messages,
            stream=True,
        )  # type: ignore
        for resp in response:
            yield resp["choices"][0]["delta"].get("content", "")


class ChatRunner:
    def __init__(self, verbose: bool) -> None:
        logging.basicConfig()
        self.logger = logging.getLogger(__name__)
        if verbose:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)

    def start_conversation(
        self,
        system_message: Optional[str] = None,
        temperature: float = 1.0,
        max_tokens: Optional[int] = None,
    ) -> Callable[[str], Generator[str, None, None]]:
        conversation = Conversation(
            system_message=system_message,
            temperature=temperature,
            max_tokens=max_tokens,
        )

        def chat(user_message: str) -> Generator[str, None, None]:
            response = ""
            for content in conversation.call_chatapi(user_message):
                response += content
                yield content
            conversation.messages.append({"role": "assistant", "content": response})
            self.logger.debug(conversation.messages)

        return chat

import readline  # noqa: F401
from argparse import ArgumentParser

from ai.chat import ChatRunner


def main(debug: bool) -> None:
    system_message = input("System: ")

    chat = ChatRunner(debug).start_conversation(system_message=system_message)
    while True:
        response = chat(input("User: "))
        print("Assistant: ", end="")
        for content in response:
            print(content, end="", flush=True)
        print()


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose mode")
    args = parser.parse_args()

    main(args.verbose)

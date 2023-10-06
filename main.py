import argparse
import importlib
import os
from pydoc import locate

from di import container


def get_full_path(command_string: str):
    class_name = command_string.capitalize() + "Command"
    module_path = f"commands.{class_name}.{class_name}"
    return locate(module_path)



def load_all_modules_from_dir(dirname):
    for module_name in os.listdir(dirname):
        if module_name == '__init__.py' or module_name[-3:] != '.py':
            continue

        module_path = os.path.join(dirname, module_name).replace(os.sep, '.').rstrip('.py')
        importlib.import_module(module_path)


def initialize_app():
    load_all_modules_from_dir("trainers")
    load_all_modules_from_dir("commands")


def main():
    parser = argparse.ArgumentParser(description="ML Sandbox")
    parser.add_argument("command", help="Command to run")

    args, _ = parser.parse_known_args()

    class_name = get_full_path(args.command)
    command_class = container.get(class_name)

    if not command_class:
        print(f"Unknown command: {args.command}")
        return

    # Allow the loaded command class to add its specific arguments
    command_class.arg_spec(parser)
    args = parser.parse_args()  # Parse again with full arguments
    vargs = vars(args)
    vargs.pop("command")
    # Execute the command
    result = command_class.execute(**vargs)
    print(result)


if __name__ == '__main__':
    initialize_app()
    main()

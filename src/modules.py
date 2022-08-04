import sys
import glob
import logging
from os.path import dirname, basename, isfile, join, abspath
from importlib import reload


class KrytonModules:

    imported_modules = {}
    registered_modules = {}

    def __init__(self, path):
        sys.path.append(path)
        self.modules_path = path
        self.load()

    def load(self):
        module_files = glob.glob(join(self.modules_path, "*.py"))
        for file in module_files:
            if not isfile(file) or file.endswith("__init__.py"):
                continue

            try:
                lib_name = basename(file)[:-3]
                logging.info(f"Module library load: {lib_name}")

                lib = __import__(lib_name)
                self.imported_modules[lib_name] = lib

                if hasattr(lib, "register"):
                    logging.info(f"Module library register: {lib_name}")
                    lib.register(self.registered_modules)

                    if hasattr(lib, "init"):
                        logging.info(f"Module library init: {lib_name}")
                        lib.init()

            except Exception as e:
                logging.error(e)

    def reload(self, path):
        src_path_full = abspath(path)
        src_path = abspath(dirname(path))

        if self.modules_path == src_path and src_path_full.endswith(".py"):
            try:
                lib_name = basename(src_path_full)[:-3]

                logging.info(f"Module library reload: {lib_name}")

                if lib_name in self.imported_modules:
                    lib = reload(self.imported_modules[lib_name])

                else:
                    lib = __import__(lib_name)

                if hasattr(lib, "register"):
                    logging.info(f"Module library register: {lib_name}")
                    lib.register(self.registered_modules)

                    if hasattr(lib, "init"):
                        logging.info(f"Module library init: {lib_name}")
                        lib.init()

            except Exception as e:
                logging.error(e)

    async def match_module(self, client, message):
        command = message.content.split(" ")[0]

        print("modules", self.registered_modules)

        for name, settings in sorted(self.registered_modules.items()):
            print(name, settings)
            cmd = settings.get("cmd", None)
            if not cmd:
                continue

            print(cmd, command)

            if not cmd == command:
                continue

            execute = settings.get("execute", None)
            if not execute:
                continue

            if callable(execute):
                await execute(client, message)
                return True

        return False

import importlib
import importlib.util
import inspect
import os
import pkgutil
import sys


def is_constant_class(Foo):
    for func in dir(Foo):
        if callable(getattr(Foo, func)) and not func.startswith("__"):
            return False
    return True


# Reference taken from https://stackoverflow.com/a/25562415/13268491
def import_submodules(package, recursive=True):
    """ Import all submodules of a module, recursively, including subpackages

    :param package: package (name or actual module)
    :type package: str | module
    :rtype: dict[str, types.ModuleType]
    """
    if isinstance(package, str):
        package = importlib.import_module(package)
    results = {}
    for loader, name, is_pkg in pkgutil.walk_packages(package.__path__):
        full_name = package.__name__ + "." + name
        try:
            results[full_name] = importlib.import_module(full_name)
        except Exception:
            pass
        if recursive and is_pkg:
            results.update(import_submodules(full_name))
    return results


def find_non_doc_code(obj):
    is_document_missing = False
    for key, value in inspect.getmembers(obj):
        try:
            if inspect.getsourcefile(value) == module.__file__:
                if inspect.isclass(value):
                    if is_constant_class(value):
                        continue
                    else:
                        find_non_doc_code(value)
                if not value.__doc__:
                    print('"' + inspect.getsourcefile(value) + '", line ' + str(inspect.getsourcelines(value)[-1]))
                    is_document_missing = True
        except Exception:
            pass
    return is_document_missing


if __name__ == "__main__":
    MODULE_PATH = os.path.join(os.getcwd(), "vwo/__init__.py")
    MODULE_NAME = "vwo"
    spec = importlib.util.spec_from_file_location(MODULE_NAME, MODULE_PATH)
    vwo = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = vwo
    spec.loader.exec_module(vwo)
    modules = import_submodules(vwo).values()
    is_document_missing = False
    for module in modules:
        is_document_missing |= find_non_doc_code(module)
    sys.exit(is_document_missing)

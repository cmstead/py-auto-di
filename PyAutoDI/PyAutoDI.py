from importlib import import_module
from glob import glob

from .Container import Container

def get_module_paths(path_pattern):
    return glob(path_pattern)

def load_modules(module_paths):
    return map(import_module, module_paths)

def register_module(module, container):
    module.register(container)

def load_and_register_modules(path_pattern, container):
    module_paths = get_module_paths(path_pattern)
    modules = load_modules(module_paths)
    
    for module in modules:
        register_module(module, container)

def get_new_container():
    return Container()

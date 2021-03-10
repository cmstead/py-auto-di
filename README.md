# PyAutoDI #

## What Is It? ##

## Setup ##

### Installing PyAutoDi ###

In your project, run:

```
pip install py-auto-di
```

For more information about pip, please visit the [Real Python page](https://realpython.com/what-is-pip/).

### Setting Up a Container ###

The easiest way to set up your DI container is to let it find and set up your dependencies for you:

```
from PyAutoDI import PyAutoDI

def get_new_container():
    container = PyAutoDI.get_new_container()

    return PyAutoDI.load_and_register_modules("./dependencies/**/*.py", container)

app_container = get_new_container()
```

Now you have a container with all of your dependencies loaded and ready to go!

(We'll take a look at how to write your dependencies in a moment)

If you want to register your dependencies by hand, you can do that too. Here's how you'd do it:

```
from PyAutoDI import PyAutoDI

from .dependencies.MyFirstDependency import MyFirstDependency
from .dependencies.MySecondDependency import MySecondDependency

def get_new_container():
    container = PyAutoDI.get_new_container()

    container.register(MyFirstDependency)
    container.register(MySecondDependency)

    return container

app_container = get_new_container()
```

Easy peasy.

## Building Dependencies ##

### Auto-registering Dependencies ###
If you are planning on having PyAutoDI discover and register your dependencies, they need to follow a simple convention:

```
class MyDependency:
    def __init__(self, logger):
        self.logger = logger

    def do_stuff(self, message):
        self.logger.log(message)

def register(container):
    container.register(MyDependency)
```

PyAutoDI will look for a register function to call. If it finds one, it will automatically call it, and register your dependency however you see fit. This is the easiest way to keep all of the information about your module together.

If you have an interface defined, you can register it along with your dependency. This helps when you want to define how your module works in case you need to create a hot-swappable version, or a test double. This can be especially useful for modules which have side effects you want to mitigate during testing.

```
from ..interfaces.MyDependencyInterface import MyDependencyInterface

class MyDependency(MyDependencyInterface):
    def __init__(self, logger):
        self.logger = logger

    def do_stuff(self, message):
        self.logger.log(message)

def register(container):
    container.register(MyDependency, interface=MyDependencyInterface)
```

### Hand-registered Dependencies ###

For hand-registered dependencies, you can either build your dependencies as you would for auto-registering, and call the register function yourself:

```
from PyAutoDI import PyAutoDI

from .dependencies.MyFirstDependency import MyFirstDependency

def get_new_container():
    container = PyAutoDI.get_new_container()

    MyFirstDependency.register(container)

    return container

app_container = get_new_container()
```

Or you can skip the register function, and hand-register like the following:

Dependency:

```
from ..interfaces.MyDependencyInterface import MyDependencyInterface

class MyDependency(MyDependencyInterface):
    def __init__(self, logger):
        self.logger = logger

    def do_stuff(self, message):
        self.logger.log(message)
```

Hand-registration:

```
from PyAutoDI import PyAutoDI

from .dependencies.MyDependency import MyDependency
from .interfaces.MyDependencyInterface import MyDependencyInterface

def get_new_container():
    container = PyAutoDI.get_new_container()

    container.register(MyDependency, MyDependencyInterface)

    return container

app_container = get_new_container()
```
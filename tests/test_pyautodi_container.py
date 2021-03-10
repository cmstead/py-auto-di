from PyAutoDI.PyAutoDI import get_new_container
import abc


class ComposedInterface(abc.ABC):

    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, 'get_simple_dependency') and
            callable(subclass.get_simple_dependency))


class SimpleDependency:
    def __init__(self):
        pass


class ComposedClass(ComposedInterface):
    def __init__(self, simple_dependency):
        self.simple_dependency = simple_dependency

    def get_simple_dependency(self):
        return self.simple_dependency


class ComposedClassOverride(ComposedInterface):
    def __init__(self):
        pass

    def get_simple_dependency(self):
        return ""


class ComposedNoInterface:
    pass


def test_class_can_be_registered():
    """Test class can be registered without dependencies"""
    container = get_new_container()

    container.register(SimpleDependency)

    test_instance = container.build("simple_dependency")

    assert isinstance(test_instance, SimpleDependency)


def test_can_construct_class_with_dependencies():
    """Test a class with dependencies is properly constructed"""
    container = get_new_container()

    container.register(SimpleDependency)
    container.register(ComposedClass)

    test_instance = container.build("composed_class")

    assert isinstance(test_instance, ComposedClass)
    assert isinstance(test_instance.simple_dependency, SimpleDependency)


def test_override_replaces_original_class():
    """Test that overriding a class replaces the original"""
    container = get_new_container()

    container.register(ComposedClass, interface=ComposedInterface)

    container.override("composed_class", ComposedClassOverride)

    try:
        test_instance = container.build("composed_class")

        assert isinstance(test_instance, ComposedClassOverride)
    except:
        assert False, "Failed to build override class -- cannot build"


def test_override_verifies_interface():
    """Test that when overriding a dependency, it verifies the interface"""
    container = get_new_container()
    override_failed = False

    container.register(ComposedClass, interface=ComposedInterface)

    try:
        container.override("composed_class", ComposedNoInterface)
    except:
        override_failed = True

    assert override_failed, "Override failed to throw on interface mismatch"


def test_container_can_produce_new_children():
    """Container children should contain dependency information matching parent container"""
    container = get_new_container()

    container.register(SimpleDependency)
    container.register(ComposedClass, interface=ComposedInterface)

    child_container = container.new()

    test_instance = child_container.build("composed_class")

    assert isinstance(test_instance, ComposedClass)
    assert isinstance(test_instance.simple_dependency, SimpleDependency)


def test_override_is_scoped_to_child():
    """Test that when overriding a dependency, it doesn't impact the parent container"""
    container = get_new_container()

    container.register(SimpleDependency)
    container.register(ComposedClass, interface=ComposedInterface)

    child_container = container.new()
    child_container.override("composed_class", ComposedClassOverride)

    parent_test_instance = container.build("composed_class")
    child_test_instance = child_container.build("composed_class")

    assert isinstance(
        parent_test_instance.get_simple_dependency(), SimpleDependency)
    assert child_test_instance.get_simple_dependency() == ""

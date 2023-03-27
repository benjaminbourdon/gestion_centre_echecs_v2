from gce2.application.clicomponents.menu import Menu
from gce2.exception.exception import NotInstanciatedMenuException

from abc import ABC, abstractmethod


class DynamicMenu(Menu, ABC):

    def __init__(self, app, name, upper_menu=None) -> None:
        super().__init__(app, name, upper_menu)

        selected_object = self._select_linked_object()

        if selected_object is not None:
            self._get_object_method, self._object_id = selected_object
            self._construct_dynamic_menu()
        else:
            raise NotInstanciatedMenuException

    @property
    def linked_object(self):
        return self._get_object_method(self._object_id)

    @property
    def menuitems(self):
        return super().menuitems

    @abstractmethod
    def _select_linked_object(self):
        raise NotImplementedError

    @abstractmethod
    def _construct_dynamic_menu(self):
        raise NotImplementedError

    def __str__(self) -> str:
        self._construct_dynamic_menu()
        return super().__str__()

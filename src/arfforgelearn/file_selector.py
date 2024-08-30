import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class FileChooser(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Selecciona un archivo")
        self.set_size_request(400, 200)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.selected_file = None

    def select_file(self, title="Selecciona un archivo"):
        dialog = Gtk.FileChooserDialog(
            title=title,
            parent=self,
            action=Gtk.FileChooserAction.OPEN,
        )
        dialog.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN,
            Gtk.ResponseType.OK,
        )

        filter_arff = Gtk.FileFilter()
        filter_arff.set_name("ARFF files")
        filter_arff.add_pattern("*.arff")
        dialog.add_filter(filter_arff)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.selected_file = dialog.get_filename()
        dialog.destroy()  # Cierra el diálogo inmediatamente

        while Gtk.events_pending():  # Procesa todos los eventos pendientes
            Gtk.main_iteration()

        return self.selected_file

    def save_file(self, title="Selecciona la ubicación para guardar el archivo"):
        dialog = Gtk.FileChooserDialog(
            title=title,
            parent=self,
            action=Gtk.FileChooserAction.SAVE,
        )
        dialog.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_SAVE,
            Gtk.ResponseType.OK,
        )

        filter_arff = Gtk.FileFilter()
        filter_arff.set_name("ARFF files")
        filter_arff.add_pattern("*.arff")
        dialog.add_filter(filter_arff)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.selected_file = dialog.get_filename()
            if not self.selected_file.endswith('.arff'):
                self.selected_file += '.arff'
        dialog.destroy()  # Cierra el diálogo inmediatamente

        while Gtk.events_pending():  # Procesa todos los eventos pendientes
            Gtk.main_iteration()

        return self.selected_file

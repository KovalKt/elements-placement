
import pygtk
import gtk
from hendlers import Hendlers


builder = gtk.Builder()
builder.add_from_file("gui.glade")

if __name__ == "__main__":

    builder.connect_signals(Hendlers())

    main_window = builder.get_object("window1")
    main_window.show_all()
    
    
    gtk.main()
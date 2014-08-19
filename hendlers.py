import pygtk

import gtk

import pickle
import pydot
from element import Element


builder = gtk.Builder()
builder.add_from_file("gui.glade")

el_num = 11
var_num = 2
w = 4
h = 3
graph = pydot.Dot(graph_name='Graph_mili', graph_type='digraph')

plata = [[-1]*w for x in range(h)]
adjacency_matrix = ([
    [0,1,0,0,0,0,0,0,0,0,0],
    [1,0.2,0,0,1,0,0,0,0,0],
    [0,2,0,0,1,0,0,0,0,0,0],
    [0,0,0,0,1,0,0,0,0,0,0],
    [0,0,1,1,0,0,0,0,1,0,0],
    [0,0,1,0,0,0,1,0,0,0,0],
    [0,0,0,0,0,1,0,2,0,0,0],
    [0,0,0,0,0,0,2,0,0,1,0],
    [0,0,0,0,1,0,0,0,0,1,0],
    [0,0,0,0,0,0,0,1,1,0,1],
    [0,0,0,0,0,0,0,0,0,1,0]
])

first_distance = 0
optimized_distance = 0

el_list = [Element(x) for x in range(el_num)]


class DrawingHendler():
    def __init__(self):
        
        self.area = builder.get_object("drawingarea1")
        self.area.show()
        self.drawable = self.area.window
        self.gc = self.drawable.new_gc(foreground=None, background=None, font=None,
                    function=-1, fill=-1, tile=None,
                    stipple=None, clip_mask=None, subwindow_mode=-1,
                    ts_x_origin=-1, ts_y_origin=-1, clip_x_origin=-1,
                    clip_y_origin=-1, graphics_exposures=-1,
                    line_width=-1, line_style=-1, cap_style=-1,
                    join_style=-1)


class MenuHendler():
    def __init__(self):
        pass 

    def change_el(self, index):
        global el_list
        el1, el2 = el_list[index], el_list[index+1]
        tmp_x = el1.x
        tmp_y = el1.y
        el1.x = el2.x
        el1.y = el2.y
        el2.x = tmp_x
        el2.y = tmp_y
        

    def rollback_changing(self, index):
        global el_list
        el1, el2 = el_list[index], el_list[index+1]
        tmp_x = el1.x
        tmp_y = el1.y
        el1.x = el2.x
        el1.y = el2.y
        el2.x = tmp_x
        el2.y = tmp_y


    def show_graph(self,button):
        global graph

        node_list = {}
        for i in range(1,(el_num+1)):
            node_list[i]=pydot.Node("E%s"%i)
        
        graph.add_edge(pydot.Edge(node_list.get(1), node_list.get(2)))
        graph.add_edge(pydot.Edge(node_list.get(2), node_list.get(3)))
        graph.add_edge(pydot.Edge(node_list.get(3), node_list.get(2)))
        graph.add_edge(pydot.Edge(node_list.get(4), node_list.get(5)))
        graph.add_edge(pydot.Edge(node_list.get(9), node_list.get(5)))
        graph.add_edge(pydot.Edge(node_list.get(2), node_list.get(6)))
        graph.add_edge(pydot.Edge(node_list.get(11), node_list.get(10)))
        graph.add_edge(pydot.Edge(node_list.get(9), node_list.get(10)))
        graph.add_edge(pydot.Edge(node_list.get(6), node_list.get(7)))
        graph.add_edge(pydot.Edge(node_list.get(7), node_list.get(8)))
        graph.add_edge(pydot.Edge(node_list.get(8), node_list.get(7)))
        graph.add_edge(pydot.Edge(node_list.get(10), node_list.get(8)))

        for value in node_list.itervalues():
            graph.add_node(value)

        graph.write("example1", format='png')
        img_dialog = builder.get_object("image_dialog")
        image = builder.get_object("image1")
        image.set_from_file("example1")
        res = img_dialog.run()
        if res:
            img_dialog.hide()

    def unoptimized_location(self, button):
        global el_list, plata, first_distance, optimized_distance

        index = 0
        for i in range(h):
            for j in range(w):
                if index == el_num:
                    break
                el_list[index].x = j
                el_list[index].y = i
                plata[i][j] = index
                index += 1

        first_distance = optimized_distance = self.calc_distance()

        show_dialog = builder.get_object("result")
        text_view = builder.get_object("textview1")
        label = builder.get_object("ch_label")
        label.set_text("Unoptimized location")
        buff = gtk.TextBuffer()
        good_string = ''
        
        for el in plata:
            good_string += '\t'.join(map(str, el))+"\n" 
        good_string += "Distance: " + str(first_distance)
        buff.set_text(good_string)
        text_view.set_buffer(buff)
        res = show_dialog.run()
        if res:
            show_dialog.hide()

    def calc_distance(self):
        global adjacency_matrix, el_list

        distance = 0
        for i, row in enumerate(adjacency_matrix):
            for j, el in enumerate(row):
                if el >0:
                    el1 = el_list[i]
                    el2 = el_list[j]
                    distance += abs(el2.x-el1.x)+abs(el2.y-el1.y)
        return distance/2

    def optimize_location(self, button):
        global adjacency_matrix, plata, optimized_distance

        for i in range(3):
            for j in range(len(el_list[:-1])):
                self.change_el(j)
                print "1",el_list
                new_d = self.calc_distance()
                print "nd ", new_d
                if new_d <= optimized_distance:
                    plata[el_list[j].y][el_list[j].x] = el_list[j].id
                    plata[el_list[j+1].y][el_list[j+1].x] = el_list[j+1].id
                    optimized_distance = new_d
                    print "Replace element %s with element %s" % (el_list[j].id, el_list[j+1].id)
                    for er in plata:
                        print '\t'.join(map(str, er))
                    print "New distance = %s" % optimized_distance
                else:
                    self.rollback_changing(j)
                    print "Replacing elements %s and %s don't give result" % (el_list[j].id, el_list[j+1].id)
        for er in plata:
            print '\t'.join(map(str, er))




class Hendlers(DrawingHendler,MenuHendler):
    def __init__(self):
        pass

    def onDeleteWindow(*args):
        gtk.main_quit(*args)
        return


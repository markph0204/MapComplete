# coding: utf-8


import os
import gtk
import cairo
import Image
import urllib
import cStringIO
import random
import re
from xml.dom import minidom

import gdal
from matplotlib import pyplot as plt
from geofunctions import *
from TileServers import *


TILESIZE = 256

target_tif = '../../02 FileFormatHacks/GeoTIFF_Hacker/rs.tif'

kmlpath = 'forqueta.kml'

#######################

#-23.907182,-51.192284

zoomlevel = 15
startcenter =  coordfromstring('-30.036, -51.210')
max_altitude = 500
blend_mode = 'soft_light'
servertype = 'google'
layers = 'HYBRID'
tilepath = '../Tiles/Google Tiles'


#######################


def mousemove(widget, event):
    delta = numpy.array((event.x, event.y))
    if widget.clicked_button == 1:
        widget.drag = widget.point_clicked - delta
        widget.queue_draw()
    #elif widget.clicked_button == 3:

def mousepress(widget, event):
    clickposition = numpy.array([event.x, event.y])
    widget.clicked_button = event.button
    widget.point_clicked = clickposition
    rect = widget.get_allocation()
    size = numpy.array([rect.width, rect.height])
    if event.type.value_nick=='2button-press':
        widget.pixelcenter += (clickposition - size/2) * [1,-1]
        if widget.clicked_button == 1:
            pixels = 2**widget.zoomlevel*TILESIZE
            rel_pos = widget.pixelcenter/pixels
            widget.zoomlevel += 1
            widget.pixelcenter = rel_pos * (2**widget.zoomlevel*TILESIZE)
        elif widget.clicked_button == 3:
            pixels = 2**widget.zoomlevel*TILESIZE
            rel_pos = widget.pixelcenter/pixels
            widget.zoomlevel -= 1
            widget.pixelcenter = rel_pos * (2**widget.zoomlevel*TILESIZE)


def mouserelease(widget, event):
    if not event.type.value_nick=='2button-press':
        widget.clicked_button = None
        widget.pixelcenter += (widget.drag * [1,-1])
        widget.drag = numpy.array([0,0])
        widget.point_clicked = None
        widget.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))
        widget.parent.set_title("Wait")
        widget.queue_draw()  ## deve substituir por refresh quando estiver desconectada a criação da lista de tiles e a renderização

def mousescroll(widget, event):
    zoomscale = 0.9
    if not event.direction.numerator:
        zoomscale = 1 + (1 - zoomscale)
    infoholder['graphscale'] *= zoomscale
    widget.queue_draw()


class MapCanvas(gtk.DrawingArea):
    def __init__(self, startcenter, zoomlevel):
        super(MapCanvas, self).__init__()
        self.connect("expose_event", self.expose)
        self.connect("expose_event", self.expose)
        self.connect("motion_notify_event", mousemove)
        self.connect("button_press_event", mousepress)
        self.connect("button_release_event", mouserelease)
        self.connect("scroll_event", mousescroll)
        self.add_events(gtk.gdk.EXPOSURE_MASK
                    | gtk.gdk.LEAVE_NOTIFY_MASK
                    | gtk.gdk.BUTTON_PRESS_MASK
                    | gtk.gdk.BUTTON_RELEASE_MASK
                    | gtk.gdk.POINTER_MOTION_MASK
                    | gtk.gdk.POINTER_MOTION_HINT_MASK
                    | gtk.gdk.SCROLL)

        self.clicked_button = 0
        self.point_clicked = None

        self.zoomlevel = zoomlevel
        self.pixelcenter = latlontopixels(startcenter, self.zoomlevel)
        self.drag = numpy.array([0, 0])

        self.ts = TileServer(servertype)
        self.ts.layers = layers

        self.kmldict = {'points': [], 'tracks': []}
        self.loadkmls()

        # self.demtiff = gdal.Open(target_tif)
        # self.dem_array = self.demtiff.GetRasterBand(1).ReadAsArray() ####### EXPERIMENTAR COM RasterIO() no lugar de GetRasterBand()




    def loadkmls(self):

        #https://maps.google.com.br/maps/ms?msid=200931058040775970557.0004c283a922f56c6cec5&msa=0

        #kml_source = urllib.urlretrieve('http://maps.google.com.br/maps/ms?msid=' +
                                     #'200931058040775970557.0004c283a922f56c6cec5' +
                                     #'&msa=0&output=kml', 'temp.kml')
        #kml = cStringIO.StringIO(kml_source)
        
        #kml_source = urllib.urlopen('http://mapsengine.google.com/map/kml?mid=zm9PtxcccPwY.kwDINdzN8HBc').read()
        #kml_source.seek(0)
        
        kml_source = open('continentes.kml').read()
        
        dom = minidom.parseString(kml_source)
        places = dom.getElementsByTagName('Placemark')

        # stylecolors = {}
        # styles = dom.getElementsByTagName('Style')
        # for style in styles:
        #     sib = style.getElementsByTagName('LineStyle')
        #     if sib:
        #         colorstring = sib[0].getElementsByTagName('color')[0].firstChild.data
        #         rgba_color = [int(n, 16)/255.0 for n in (colorstring[6:], colorstring[4:6], colorstring[2:4], colorstring[:2])]
        #         stylecolors[style.attributes['id'].nodeValue] = rgba_color

        for place in places:
            if place.getElementsByTagName('Point'):
                pointdict = {}
                pointdict['name'] = place.getElementsByTagName('name')[0].firstChild.data.strip()
                pointdict['coords'] = numpy.fromstring(place.getElementsByTagName('coordinates')[0].firstChild.data, sep=',')
                self.kmldict['points'].append(pointdict)

            if place.getElementsByTagName('LineString'):
                trackdict = {}
                trackdict['name'] = place.getElementsByTagName('name')[0].firstChild.data
                trackdict['color'] = (1,0.5,0,1) # stylecolors[place.getElementsByTagName('styleUrl')[0].firstChild.data.replace('#', '')]
                trackdict['coords'] = numpy.vstack([numpy.fromstring(s, sep=',')
                        for s in re.split('\s+', place.getElementsByTagName('coordinates')[0].firstChild.data) if s])
                self.kmldict['tracks'].append(trackdict)


    ### DEVE DESCONECTAR EM TRÊS EVENTOS:
        # DEFINIR A LISTA DE NOMES DAS TILES DA VIEWPORT ATUAL;
        # IR PREENCHENDO A LISTA DE TILES E DANDO REDRAW A CADA NOVA RECARREGADA;
        # CADA REDRAW DESENHA A LISTA INTEIRA, QUE COMEÇA PARCIAL E AUMENTA À MEDIDA QUE AS TILES VÃO SURGINDO
            # OPCIONALMENTE, O REDRAW PODE SER SOMENTE NA REGIÃO AFETADA (CLIP)

        #TODO: USAR MÓDULO multiprocess


    #def listviewport():
        #pixels = 2**self.zoomlevel*TILESIZE
        #x, y = self.pixelcenter
        #xi = int(x/TILESIZE)
        #yi = int((pixels-y)/TILESIZE)
        #xoff = x%TILESIZE
        #yoff = TILESIZE - y%TILESIZE
        #centercoords = self.size/2 - numpy.array([xoff, yoff])  # o nome desta variável significa realmente o que é?
        #cr.translate(*(centercoords - self.drag).astype(int))
        #toleft, totop = (centercoords/TILESIZE + 1).astype(int)
        #cols, rows = (self.size / TILESIZE + 2).astype(int)

        #for x in range(cols):
            #for y in range(rows):
                #xindex = x + xi - toleft
                #yindex = y + yi - totop
                #xpos = (x - toleft) * TILESIZE
                #ypos = (y - totop) * TILESIZE
                #cr.set_source_surface(self.ts.tile_as_surface(xindex, yindex, self.zoomlevel),
                                      #xpos, ypos)

    def expose(self, widget, event):
        cr = widget.window.cairo_create()
        rect = self.get_allocation()
        print rect
        cr.rectangle(*rect)
        cr.clip()
        self.size = numpy.array([rect.width, rect.height])


        pixels = 2**self.zoomlevel*TILESIZE
        x, y = self.pixelcenter
        print x, y
        xi = int(x/TILESIZE)
        yi = int((pixels-y)/TILESIZE)
        xoff = x%TILESIZE
        yoff = TILESIZE - y%TILESIZE
        centercoords = self.size/2 - numpy.array([xoff, yoff])  # o nome desta variável significa realmente o que é?


        ## TODO: FAZER PLOTAGEM EM "CAMADAS", COM FLAGS VALENDO TANTO PARA A PLOTAGEM QUANTO PARA A PREPARAÇÃO

        cr.save()
        cr.translate(*(centercoords - self.drag).astype(int))
        toleft, totop = (centercoords/TILESIZE + 1).astype(int)
        cols, rows = (self.size / TILESIZE + 2).astype(int)

        for x in range(cols):
            for y in range(rows):
                xindex = x + xi - toleft
                yindex = y + yi - totop
                xpos = (x - toleft) * TILESIZE
                ypos = (y - totop) * TILESIZE
                cr.set_source_surface(self.ts.tile_as_surface(xindex, yindex, self.zoomlevel),
                                      xpos, ypos)
                cr.paint()
        cr.restore()

        if self.point_clicked == None:
            blend_modes = {
            'multiply':   14,
            'overlay':    16,
            'soft_light': 22,
            'hsl_hue':    25,
            'hsl_color':  27}

            halfsize = self.size/2

            topleft = pixelstolatlon(self.pixelcenter - halfsize, self.zoomlevel)
            bottomright = pixelstolatlon(self.pixelcenter + halfsize, self.zoomlevel)

            # left_origin, pixel_width, _, top_origin, __, pixel_height = self.demtiff.GetGeoTransform()

            # left = int(round((topleft[0] - left_origin)/pixel_width))
            # right = int(round((bottomright[0] - left_origin)/pixel_width))
            # top = int(round((topleft[1] - top_origin)/pixel_height))
            # bot = int(round((bottomright[1] - top_origin)/pixel_height))

            #print right-left
            #print top, bot
            #exit()

            # sub = self.dem_array[bot:top, left:right].astype(float)
            # cmap = plt.cm.gist_earth
            # if True:
            #     imstring = cStringIO.StringIO()
            #     Image.fromarray(cmap(sub/sub.max(), bytes=True)).save(imstring, 'PNG')
            #     imstring.seek(0)
            # else:
            #     dpi = 100.0
            #     w, h = rect.width/dpi, rect.height/dpi
            #     fig = plt.figure(figsize=(w,h), dpi=dpi)
            #     #fig.figimage(sub, cmap=plt.cm.gist_earth) #, vmin=5, vmax=300)
            #     plt.subplots_adjust(left=0.0, right=1.0, bottom=0.0, top=1.0)
            #     plt.contourf(sub, cmap=cmap, levels=numpy.arange(0,1000,100))
            #     plt.savefig('temp.png')

            # demsurface = cairo.ImageSurface.create_from_png(imstring)

            # cr.save()
            # hscale = self.size[0]/float(demsurface.get_width())
            # vscale = self.size[1]/float(demsurface.get_height())
            # cr.scale(hscale, vscale)
            # cr.set_source_surface(demsurface, 0, 0)
            # cr.set_operator(blend_modes[blend_mode])
            # cr.paint_with_alpha(0.9)
            # cr.restore()


            cr.translate(*(centercoords - self.drag).astype(int))


            kmloff = numpy.array([xoff, yoff])*[1,-1] - self.pixelcenter
            cr.set_line_join(cairo.LINE_JOIN_ROUND)

            # plotar trilhas
            for trilha in self.kmldict['tracks']:
                firstpoint = True
                for coord in trilha['coords']:
                    x, y = latlontopixels(coord[0:2], self.zoomlevel) + kmloff
                    if firstpoint:
                        cr.move_to(x,-y)
                        firstpoint = False
                    else:
                        cr.line_to(x,-y)
                cr.set_source_rgba(*trilha['color'])
                cr.set_line_width(2)
                cr.stroke()

            # plotar pontos
            cr.set_source_rgb(1,1,1)
            cr.set_font_size(15)
            for ponto in self.kmldict['points']:
                if ponto['name'] != 'topleft' and ponto['name'] != 'bottomright':
                    coord = ponto['coords']
                    x, y = latlontopixels(coord[0:2], self.zoomlevel) + kmloff
                    cr.new_sub_path()
                    cr.arc(x, -y, 3, 0, 2*pi)
                    cr.rel_move_to(5,0)
                    cr.show_text(ponto['name'])
            cr.set_source_rgb(0,1,1)
            cr.fill_preserve()
            cr.set_source_rgb(0,0,0)
            cr.set_line_width(2)
            cr.stroke()


        self.parent.set_title("Ready")
        self.window.set_cursor(None)



window = gtk.Window()
window.connect("destroy", gtk.main_quit)

accelgroup = gtk.AccelGroup()
key, modifier = gtk.accelerator_parse('Escape')
accelgroup.connect_group(key, modifier, gtk.ACCEL_VISIBLE, gtk.main_quit)
window.add_accel_group(accelgroup)
canvas = MapCanvas(startcenter, zoomlevel)

class FullscreenToggler(object):
    def __init__(self, window, keysym=gtk.keysyms.F11):
        self.window = window
        self.keysym = keysym
        self.window_is_fullscreen = False
        self.window.connect_object('window-state-event',
                                   FullscreenToggler.on_window_state_change,
                                   self)

    def on_window_state_change(self, event):
        self.window_is_fullscreen = bool(gtk.gdk.WINDOW_STATE_FULLSCREEN & event.new_window_state)

    def toggle(self, event):
        if event.keyval == self.keysym:
            if self.window_is_fullscreen:
                self.window.unfullscreen()
            else:
                self.window.fullscreen()

toggler = FullscreenToggler(window)
window.connect_object('key-press-event', FullscreenToggler.toggle, toggler)

windowed = True
if windowed:
    window.resize(500,500)
    window.set_position(gtk.WIN_POS_CENTER)
else:
    window.maximize()

window.add(canvas)
window.show_all()
gtk.main()



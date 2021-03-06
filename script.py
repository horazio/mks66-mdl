import mdl
from display import *
from matrix import *
from draw import *

def run(filename):
    """
    This function runs an mdl script
    """
    p = mdl.parseFile(filename)

    if p:
        (commands, symbols) = p
    else:
        print "Parsing failed."
        return

    view = [0,
            0,
            1]
    ambient = [50,
               50,
               50]
    light = [[0.5,
              0.75,
              1],
             [255,
              255,
              255]]

    color = [0, 0, 0]
    tmp = new_matrix()
    ident( tmp )

    stack = [ [x[:] for x in tmp] ]
    screen = new_screen()
    zbuffer = new_zbuffer()
    tmp = []
    step_3d = 100
    consts = ''
    polygons = []
    edges = []
    symbols['.white'] = ['constants',
                         {'red': [0.2, 0.5, 0.5],
                          'green': [0.2, 0.5, 0.5],
                          'blue': [0.2, 0.5, 0.5]}]


    for command in commands:
        op = command['op']

        if op == 'push':
            stack.append( [x[:] for x in stack[-1]] )

        elif op == 'pop':
            stack.pop()

        elif op == 'sphere':
            #print 'SPHERE\t' + str(args)
            if (command['constants'] == None):
                reflect = '.white'
            else:
                reflect = command['constants']

            args = command['args']
            add_sphere(polygons,
                       float(args[0]), float(args[1]), float(args[2]),
                       float(args[3]), step_3d)
            matrix_mult(stack[-1], polygons)
            draw_polygons( polygons, screen, zbuffer, view, ambient, light, symbols, reflect)
            polygons = []

        elif op == 'torus':
            #print 'TORUS\t' + str(args)
            if (command['constants'] == None):
                reflect = '.white'
            else:
                reflect = command['constants']

            args = command['args']
            add_torus(polygons,
                      float(args[0]), float(args[1]), float(args[2]),
                      float(args[3]), float(args[4]), step_3d)
            matrix_mult(stack[-1], polygons)
            draw_polygons( polygons, screen, zbuffer, view, ambient, light, symbols, reflect)
            polygons = []

        elif op == 'box':
            #print 'BOX\t' + str(args)
            if (command['constants'] == None):
                reflect = '.white'
            else:
                reflect = command['constants']

            args = command['args']
            add_box(polygons,
                    float(args[0]), float(args[1]), float(args[2]),
                    float(args[3]), float(args[4]), float(args[5]))
            matrix_mult(stack[-1], polygons)
            draw_polygons( polygons, screen, zbuffer, view, ambient, light, symbols, reflect)
            polygons = []

        elif op == 'line':
            args = command['args']
            add_edge( edges,
                      float(args[0]), float(args[1]), float(args[2]),
                      float(args[3]), float(args[4]), float(args[5]) )
            matrix_mult(stack[-1], edges)
            draw_lines(edges, screen, zbuffer, color)
            edges = []

        elif op == 'scale':
            #print 'SCALE\t' + str(args)

            args = command['args']
            t = make_scale(float(args[0]), float(args[1]), float(args[2]))
            matrix_mult(stack[-1], t)
            stack[-1] = [x[:] for x in t]

        elif op == 'move':
            #print 'MOVE\t' + str(args)

            args = command['args']
            t = make_translate(float(args[0]), float(args[1]), float(args[2]))
            matrix_mult(stack[-1], t)
            stack[-1] = [x[:] for x in t]

        elif op == 'rotate':
            #print 'ROTATE\t' + str(args)

            args = command['args']

            theta = float(args[1]) * (math.pi / 180)

            if args[0] == 'x':
                t = make_rotX(theta)
            elif args[0] == 'y':
                t = make_rotY(theta)
            else:
                t = make_rotZ(theta)
            matrix_mult(stack[-1], t)
            stack[-1] = [x[:] for x in t]

        elif op == 'clear':
            clear_screen(screen)
            clear_zbuffer(zbuffer)

        elif op == 'display' or op == 'save':

            args = command['args']
            #clear_screen(screen)
            args = command['args']
            if op == 'display':
                display(screen)
            else:
                save_extension(screen, args[0])

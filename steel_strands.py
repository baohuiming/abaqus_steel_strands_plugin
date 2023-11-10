from abaqus import *
from abaqusConstants import *
import matplotlib.pyplot as plt
# from abaqus import YES, NO, getWarningReply, getInput
import section
import regionToolset
import displayGroupMdbToolset as dgm
import part
import material
import assembly
import step
import interaction
import load
import mesh
import optimization
import job
import sketch
import visualization
import xyPlot
import displayGroupOdbToolset as dgo
import connectorBehavior

def run(*args, **kwargs):
    
    sketch_XY = kwargs['name_skxy'].split('|')
    sketch_XZ = kwargs['name_skxz'].split('|')
    model_name = kwargs['name_model']
    invert_xy = kwargs['logic_invert_xy']
    invert_xz = kwargs['logic_invert_xz']
    eps = kwargs['num_eps']
    aos_xy = 0 if invert_xy else 1
    aos_xz = 0 if invert_xz else 1

    c1 = get_sketch_coords(*sketch_XY, axis_of_symmetry=aos_xy)
    c2 = get_sketch_coords(*sketch_XZ, axis_of_symmetry=aos_xz)
    plt.plot([c[0] for c in c1], [c[1] for c in c1], 'r-', label="X-Y")
    plt.plot([c[0] for c in c2], [c[1] for c in c2], 'b-', label="X-Z")
    plt.legend()
    plt.title("Close the window to continue")
    plt.show()
    
    part_name = getInput("Please input the part name of steel strands: ")
    if part_name == '':
        raise Exception("Part name is empty")
    elif part_name is None:
        return 1

    x_points = []
    for c in c1:
        x_points.append(c[0])
    for c in c2:
        # only add the point if it is not in x_points (by eps)
        if not any([abs(c[0]-x)<eps for x in x_points]):
            x_points.append(c[0])
    x_points = sorted(x_points)

    xyz_points = []
    for x in x_points:
        y = None
        z = None
        # if x is in c1, get the y value
        for c in c1:
            if abs(c[0]-x)<eps:
                y = c[1]
                break
        # if x is in c2, get the z value
        for c in c2:
            if abs(c[0]-x)<eps:
                z = c[1]
                break
        # if x is not in c1, use interpolation
        if y is None:
            for i in range(len(c1)-1):
                if c1[i][0] <= x <= c1[i+1][0]:
                    y = c1[i][1] + (c1[i+1][1]-c1[i][1])/(c1[i+1][0]-c1[i][0])*(x-c1[i][0])
                    break
        # if x is not in c2, use interpolation
        if z is None:
            for i in range(len(c2)-1):
                if c2[i][0] <= x <= c2[i+1][0]:
                    z = c2[i][1] + (c2[i+1][1]-c2[i][1])/(c2[i+1][0]-c2[i][0])*(x-c2[i][0])
                    break
        # if x is still not in c1, use extrapolation
        if y is None:
            if x < c1[0][0]:
                x1,y1 = c1[0]
                x2,y2 = c1[1]
                y = y1 + (y2-y1)/(x2-x1)*(x-x1)
            else:
                x1,y1 = c1[-2]
                x2,y2 = c1[-1]
                y = y1 + (y2-y1)/(x2-x1)*(x-x1)
        # if x is still not in c2, use extrapolation
        if z is None:
            if x < c2[0][0]:
                x1,z1 = c2[0]
                x2,z2 = c2[1]
                z = z1 + (z2-z1)/(x2-x1)*(x-x1)
            else:
                x1,z1 = c2[-2]
                x2,z2 = c2[-1]
                z = z1 + (z2-z1)/(x2-x1)*(x-x1)

        xyz_points.append((x,y,z))

    print 'xyz_points: ', xyz_points
    plt.plot([c[0] for c in xyz_points], [c[1] for c in xyz_points], 'r-', label="X-Y")
    plt.plot([c[0] for c in xyz_points], [c[2] for c in xyz_points], 'b-', label="X-Z")
    plt.legend()
    plt.title("Close the window to continue")
    plt.show()

    # open a confirm dialog
    reply = getWarningReply(message='Is the sketch correct?', buttons=(YES,NO))
    if reply == NO:
        return 1
    
    # create a new part
    p = mdb.models[model_name].Part(name=part_name, dimensionality=THREE_D, 
        type=DEFORMABLE_BODY)
    p.ReferencePoint(point=(0.0, 0.0, 0.0))
    p = mdb.models[model_name].parts[part_name]
    p.WirePolyLine(points=xyz_points, mergeType=MERGE, 
        meshable=ON)
    session.viewports['Viewport: 1'].setValues(displayedObject=p)

    



def get_sketch_coords(model_name, sketch_name, axis_of_symmetry=1):
    import section
    import regionToolset
    import displayGroupMdbToolset as dgm
    import part
    import material
    import assembly
    import step
    import interaction
    import load
    import mesh
    import optimization
    import job
    import sketch
    import visualization
    import xyPlot
    import displayGroupOdbToolset as dgo
    import connectorBehavior
    from dxf2abq import importdxf
    s1 = mdb.models[model_name].sketches[sketch_name]
    coords = []
    for g in s1.geometry.items():
        # print g[1].curveType
        if str(g[1].curveType) not in ["ARC","LINE"]:
            raise Exception('Only ARC and LINE are supported, unexpected curve type: %s' % g[1].curveType)
        vs = g[1].getVertices()
        vs = [v.coords for v in vs]
        if str(g[1].curveType) == "LINE":
            start, end = vs
            # print start, end
        else: # ARC
            start, end, center = vs
            # calculate the radius
            radius = ((start[0]-center[0])**2 + (start[1]-center[1])**2)**0.5
            # get middle point of chord coords
            middle = ((start[0]+end[0])/2, (start[1]+end[1])/2)
            # get the vector
            vector = (middle[0]-center[0], middle[1]-center[1])
            # normalize
            d_vector = ((middle[0]-center[0])**2 + (middle[1]-center[1])**2)**0.5
            vector = (vector[0]/d_vector, vector[1]/d_vector)
            # get middle point of arc: vector * radius + center
            middle_arc = (vector[0]*radius + center[0], vector[1]*radius + center[1])

            coords.append(middle_arc)

            # print start, end, center, radius, middle_arc

        if start not in coords:
            coords.append(start)
        if end not in coords:
            coords.append(end)

    # sort by x
    coords = sorted(coords, key=lambda p: p[0])

    # calculate geometry center
    x = sum([c[0] for c in coords])/len(coords)
    y = sum([c[1] for c in coords])/len(coords)

    # print 'center: ', x, y

    line_center = min(coords, key=lambda p: abs(p[1-axis_of_symmetry]-x))[axis_of_symmetry]

    # diff
    if axis_of_symmetry == 1: 
        # y-axis symmetry: The curves are symmetrically distributed on both sides of x=0
        coords = [(c[0]-x, c[1]-line_center) for c in coords]
    else:
        coords = [(c[0]-line_center, c[1]-y) for c in coords]
    print 'coords: '
    for c in coords:
        print c[0], c[1]
    
    return coords
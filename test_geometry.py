import asyncio

from pyserver.geometry import geometry_creation as geo_make
from pyserver.server import start_server
import pyserver.noodle_objects as nooobs
from pyserver.core import Server

# 42 vertices for sphere
vertices = [[-0.000000, -0.500000, -0.000000], [0.361804, -0.223610, 0.262863],
            [-0.138194, -0.223610, 0.425325],  [-0.447213, -0.223608, -0.000000],
            [-0.138194, -0.223610, -0.425325], [0.361804, -0.223610, -0.262863],
            [0.138194, 0.223610, 0.425325],    [-0.361804, 0.223610, 0.262863],
            [-0.361804, 0.223610, -0.262863],  [0.138194, 0.223610, -0.425325],
            [0.447213, 0.223608, -0.000000],   [-0.000000, 0.500000, -0.000000],
            [-0.081228, -0.425327, 0.249998],  [0.212661, -0.425327, 0.154506],
            [0.131434, -0.262869, 0.404506],   [0.425324, -0.262868, -0.000000],
            [0.212661, -0.425327, -0.154506],  [-0.262865, -0.425326, -0.000000],
            [-0.344095, -0.262868, 0.249998],  [-0.081228, -0.425327, -0.249998],
            [-0.344095, -0.262868, -0.249998], [0.131434, -0.262869, -0.404506],
            [0.475529, 0.000000, 0.154506],    [0.475529, 0.000000, -0.154506],
            [-0.000000, 0.000000, 0.500000],   [0.293893, 0.000000, 0.404508],
            [-0.475529, 0.000000, 0.154506],   [-0.293893, 0.000000, 0.404508],
            [-0.293893, 0.000000, -0.404508],  [-0.475529, 0.000000, -0.154506],
            [0.293893, 0.000000, -0.404508],   [-0.000000, 0.000000, -0.500000],
            [0.344095, 0.262868, 0.249998],    [-0.131434, 0.262869, 0.404506],
            [-0.425324, 0.262868, -0.000000],  [-0.131434, 0.262869, -0.404506],
            [0.344095, 0.262868, -0.249998],   [0.081228, 0.425327, 0.249998],
            [0.262865, 0.425326, -0.000000],   [-0.212661, 0.425327, 0.154506],
            [-0.212661, 0.425327, -0.154506],  [0.081228, 0.425327, -0.249998]]

indices =  [[0, 13, 12],  [1, 13, 15],  [0, 12, 17],  [0, 17, 19],
            [0, 19, 16],  [1, 15, 22],  [2, 14, 24],  [3, 18, 26],
            [4, 20, 28],  [5, 21, 30],  [1, 22, 25],  [2, 24, 27],
            [3, 26, 29],  [4, 28, 31],  [5, 30, 23],  [6, 32, 37],
            [7, 33, 39],  [8, 34, 40],  [9, 35, 41],  [10, 36, 38],
            [38, 41, 11], [38, 36, 41], [36, 9, 41],  [41, 40, 11],
            [41, 35, 40], [35, 8, 40],  [40, 39, 11], [40, 34, 39],
            [34, 7, 39],  [39, 37, 11], [39, 33, 37], [33, 6, 37],
            [37, 38, 11], [37, 32, 38], [32, 10, 38], [23, 36, 10],
            [23, 30, 36], [30, 9, 36],  [31, 35, 9],  [31, 28, 35],
            [28, 8, 35],  [29, 34, 8],  [29, 26, 34], [26, 7, 34],
            [27, 33, 7],  [27, 24, 33], [24, 6, 33],  [25, 32, 6],
            [25, 22, 32], [22, 10, 32], [30, 31, 9],  [30, 21, 31],
            [21, 4, 31],  [28, 29, 8],  [28, 20, 29], [20, 3, 29],
            [26, 27, 7],  [26, 18, 27], [18, 2, 27],  [24, 25, 6],
            [24, 14, 25], [14, 1, 25],  [22, 23, 10], [22, 15, 23],
            [15, 5, 23],  [16, 21, 5],  [16, 19, 21], [19, 4, 21],
            [19, 20, 4],  [19, 17, 20], [17, 3, 20],  [17, 18, 3],
            [17, 12, 18], [12, 2, 18],  [15, 16, 5],  [15, 13, 16],
            [13, 0, 16],  [12, 14, 2],  [12, 13, 14], [13, 1, 14]]

colors = [[255, 255, 255, 255]] * 42


def create_sphere(server: Server, *args):
    
    # Set up creater object
    name = "Test Sphere"
 
    material = server.create_component(nooobs.Material, name="Test Material")

    patches = []
    patch_info = nooobs.GeometryPatchInput(
        vertices = vertices, 
        indices = indices, 
        index_type = "TRIANGLES",
        material = material.id,
        colors = colors
    )
    patches.append(geo_make.create_geometry_patch(server, "Sphere", patch_info))

    sphere = server.create_component(nooobs.Geometry, name=name, patches=patches)

    # Test Delete
    server.delete_component(sphere)


# Using new_point_plot just so it gets called in test client
methods = {
    "new_point_plot": create_sphere
}

starting_state = {
    nooobs.Method: {
        nooobs.IDGroup(0, 0): nooobs.Method(id=(0,0), name="new_point_plot", arg_doc=[])
    }
}

def main():
    asyncio.run(start_server(50000, methods, starting_state))

if __name__ == "__main__":
    main()


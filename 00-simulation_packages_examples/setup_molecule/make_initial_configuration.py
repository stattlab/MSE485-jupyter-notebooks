import lammpsio
import gsd,gsd.hoomd
import numpy as np

positions = np.array([
 [0.0, 0.0, 0],
 [0.0, 0.0, 1],
 [0.0, 0.0, 2],
 [0.0, 0.0, 3],
 [0.0, 0.0, 4],
 [0.0, 0.0, 5],
 [0.0, 0.0, 6],
[0.0, 0.0, 7]
])

types = [0,0,0,0,0,0,0,0]
bonds = np.array([[0,1],[1,2],[2,3],[3,4],[4,5],[5,6],[6,7]])
bond_types = [0,0,0,0,0,0,0]

angles = np.array([
                   [0,1,2],[1,2,3],[2,3,4],
                   [3,4,5],[4,5,6],[5,6,7]])

angles_types = [0,0,0,0,0,0]


frame = gsd.hoomd.Frame()
frame.configuration.box = [20,20,20,0,0,0]
frame.particles.N = len(positions)
frame.particles.position=positions
frame.particles.typeid=types
frame.particles.types = ["A"]

frame.bonds.N = len(bonds)

frame.bonds.types = ["AA"]
frame.bonds.group = bonds
frame.bonds.typeid = bond_types


frame.angles.N = len(angles)

frame.angles.types = ['AAA']
frame.angles.group = angles
frame.angles.typeid = angles_types


trajectory = gsd.hoomd.open('init.gsd','w')
trajectory.append(frame)

snapshot, type_map = lammpsio.Snapshot.from_hoomd_gsd(frame)

lammpsio.DataFile.create(
    filename="init.data", snapshot=snapshot, atom_style="molecular"
)
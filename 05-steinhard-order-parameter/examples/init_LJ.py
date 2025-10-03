import gsd,gsd.hoomd
import numpy as np
import hoomd
import freud


kT= 1.00
a = np.sqrt(2)*1.208

fcc = freud.data.UnitCell.fcc()
box, positions = fcc.generate_system(10)

frame = gsd.hoomd.Frame()
frame.configuration.box = [box.Lx*a,box.Ly*a,box.Lz*a,0,0,0]

frame.particles.N = len(positions)

frame.particles.position = positions*a
frame.particles.types = ["A"]


density = len(positions)/(a**3*box.Lx*box.Ly*box.Lz)

cell = hoomd.md.nlist.Cell(buffer=0.4)

lj = hoomd.md.pair.LJ(nlist=cell,default_r_cut=3.0)
lj.mode='shift'
lj.params[("A", "A")] = dict(sigma=1.0, epsilon=1.0)
integrator = hoomd.md.Integrator(dt=0.005)

integrator.forces= [lj]

# Setup simulation state and initial configuration
simulation = hoomd.Simulation(device=hoomd.device.auto_select(),seed=42)
simulation.operations.integrator = integrator
simulation.create_state_from_snapshot(frame)

# Velocities
simulation.state.thermalize_particle_momenta(filter=hoomd.filter.All(), kT=kT)

# Equilibration
nvt = hoomd.md.methods.ConstantVolume(filter=hoomd.filter.All(),
                                        thermostat=hoomd.md.methods.thermostats.MTTK(kT=kT,tau=0.5))

integrator.methods = [nvt]
simulation.run(10_000)

hoomd.write.GSD.write(state=simulation.state, filename='equi_liquid.gsd', mode='wb')



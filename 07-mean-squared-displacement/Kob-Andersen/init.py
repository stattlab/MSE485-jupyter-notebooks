import gsd,gsd.hoomd
import numpy as np
import hoomd
import freud


kT= 1.0

fraction_B = 0.2

# non-ideal mixing
sigma_AA = 1
sigma_AB = 0.8*sigma_AA
sigma_BB = 0.88*sigma_AA

epsilon_AA = 1
epsilon_AB = 1.5*epsilon_AA
epsilon_BB = 0.5*epsilon_AA


a = np.sqrt(2)*1.055

fcc = freud.data.UnitCell.fcc()
box, positions = fcc.generate_system(6)

frame = gsd.hoomd.Frame()
frame.configuration.box = [box.Lx*a,box.Ly*a,box.Lz*a,0,0,0]

frame.particles.N = len(positions)

frame.particles.position = positions*a
frame.particles.types = ["A","B"]

types = np.zeros(frame.particles.N)
index = np.arange(frame.particles.N)
b_types = np.random.choice(index, int(np.round(frame.particles.N*fraction_B)), replace=False)
frame.particles.typeid = types
frame.particles.typeid[b_types]=1

density = len(positions)/(a**3*box.Lx*box.Ly*box.Lz)

cell = hoomd.md.nlist.Cell(buffer=0.4)

lj = hoomd.md.pair.LJ(nlist=cell,default_r_cut=3.0)
lj.mode='shift'
lj.params[("A", "A")] = dict(sigma=sigma_AA, epsilon=epsilon_AA)
lj.params[("A", "B")] = dict(sigma=sigma_AB, epsilon=epsilon_AB)
lj.params[("B", "B")] = dict(sigma=sigma_BB, epsilon=epsilon_BB)

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

hoomd.write.GSD.write(state=simulation.state, filename='KA_liquid.gsd', mode='wb')



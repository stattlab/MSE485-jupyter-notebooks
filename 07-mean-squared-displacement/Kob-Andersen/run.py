import gsd,gsd.hoomd
import numpy as np
import hoomd
import freud
import sys

kT= float(sys.argv[1])

fraction_B = 0.2

sigma_AA = 1
sigma_AB = 0.8*sigma_AA
sigma_BB = 0.88*sigma_AA

epsilon_AA = 1
epsilon_AB = 1.5*epsilon_AA
epsilon_BB = 0.5*epsilon_AA


cell = hoomd.md.nlist.Cell(buffer=0.4)

lj = hoomd.md.pair.LJ(nlist=cell,default_r_cut=2.5*sigma_AB)
lj.mode='shift'
lj.params[("A", "A")] = dict(sigma=sigma_AA, epsilon=epsilon_AA)
lj.r_cut[("A","A")] = sigma_AA*2**(1/6)
lj.params[("A", "B")] = dict(sigma=sigma_AB, epsilon=epsilon_AB)
lj.params[("B", "B")] = dict(sigma=sigma_BB, epsilon=epsilon_BB)
lj.r_cut[("B","B")] = sigma_BB*2**(1/6)

integrator = hoomd.md.Integrator(dt=0.005)

integrator.forces= [lj]

# Setup simulation state and initial configuration
simulation = hoomd.Simulation(device=hoomd.device.auto_select(),seed=42)
simulation.operations.integrator = integrator
simulation.create_state_from_gsd('KA_liquid.gsd')

# Velocities
simulation.state.thermalize_particle_momenta(filter=hoomd.filter.All(), kT=kT)

#Equilibration
simulation.run(100_000)

# Write trajectory
gsd = hoomd.write.GSD(mode='wb',trigger=hoomd.trigger.Periodic(100),
                      filename='KA_kT_%1.2f.gsd'%kT,
                      dynamic=['property','momentum'])

simulation.operations.writers.append(gsd)

# Measurnment
nvt = hoomd.md.methods.ConstantVolume(filter=hoomd.filter.All(),
                                        thermostat=hoomd.md.methods.thermostats.MTTK(kT=kT,tau=0.2))

integrator.methods = [nvt]
simulation.run(10_000_000_000)



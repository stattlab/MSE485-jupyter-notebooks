import gsd,gsd.hoomd
import numpy as np
import hoomd
import freud

kT = 0.1
cell = hoomd.md.nlist.Cell(buffer=0.4)

lj = hoomd.md.pair.LJ(nlist=cell,default_r_cut=3.0)
lj.mode='shift'
lj.params[("A", "A")] = dict(sigma=1.0, epsilon=1.0)
integrator = hoomd.md.Integrator(dt=0.005)

integrator.forces= [lj]

# Setup simulation state and initial configuration
simulation = hoomd.Simulation(device=hoomd.device.auto_select(),seed=42)
simulation.operations.integrator = integrator
simulation.create_state_from_gsd('equi_liquid.gsd')

# Velocities
simulation.state.thermalize_particle_momenta(filter=hoomd.filter.All(), kT=kT)

# Equilibration
nvt = hoomd.md.methods.ConstantVolume(filter=hoomd.filter.All(),
                                        thermostat=hoomd.md.methods.thermostats.MTTK(kT=kT,tau=0.5))

# Write trajectory
gsd = hoomd.write.GSD(mode='wb',trigger=hoomd.trigger.Periodic(500),
                      filename='run_liquid_%1.2f_%1.2f_short.gsd'%(0.8,kT),
                      dynamic=['property','momentum'])

simulation.operations.writers.append(gsd)

thermodynamic_properties = hoomd.md.compute.ThermodynamicQuantities(
    filter=hoomd.filter.All()
)

simulation.operations.computes.append(thermodynamic_properties)
logger = hoomd.logging.Logger(categories=['scalar'])
logger.add(simulation, quantities=['timestep'])
logger.add(thermodynamic_properties,quantities=['kinetic_temperature','pressure','kinetic_energy','potential_energy'])

table = hoomd.write.Table(trigger=hoomd.trigger.Periodic(period=500), logger=logger)
simulation.operations.writers.append(table)

integrator.methods = [nvt]


simulation.run(200_000)



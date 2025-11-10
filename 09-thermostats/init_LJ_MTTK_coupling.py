import gsd,gsd.hoomd
import numpy as np
import hoomd
import freud


kT = 1.5
a = np.sqrt(2)*1.3
thermostat_type = 'MTTK'
coupling = 500

fcc = freud.data.UnitCell.fcc()
box, positions = fcc.generate_system(5)

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
simulation.state.thermalize_particle_momenta(filter=hoomd.filter.All(), kT=0.01)


# Equilibration
#nve = hoomd.md.methods.ConstantVolume(filter=hoomd.filter.All())
#integrator.methods = [nve]


# Write trajectory

thermostat= hoomd.md.methods.thermostats.MTTK(kT=kT,
    tau=simulation.operations.integrator.dt * coupling)


gsd = hoomd.write.GSD(mode='wb',trigger=hoomd.trigger.Periodic(100),
                      filename='run_liquid_%s_%f_%1.2f_%1.2f.gsd'%(thermostat_type,coupling,density,kT),
                      dynamic=['property','momentum'])

simulation.operations.writers.append(gsd)


nvt = hoomd.md.methods.ConstantVolume(filter=hoomd.filter.All(),
                                        thermostat=thermostat)
integrator.methods = [nvt]

file = open('run_liquid_%s_%f_%1.2f_%1.2f.log'%(thermostat_type,coupling,density,kT), mode="w", newline="\n")
thermodynamic_properties = hoomd.md.compute.ThermodynamicQuantities(
    filter=hoomd.filter.All()
)
simulation.operations.computes.append(thermodynamic_properties)

logger = hoomd.logging.Logger(categories=["scalar","string"])
logger.add(simulation, quantities=["timestep"])
logger.add(thermodynamic_properties,quantities=['kinetic_temperature','pressure','potential_energy','kinetic_energy'])

table = hoomd.write.Table(trigger=hoomd.trigger.Periodic(period=1), logger=logger,output=file)
simulation.operations.writers.append(table)

simulation.run(50_000,write_at_start=True)

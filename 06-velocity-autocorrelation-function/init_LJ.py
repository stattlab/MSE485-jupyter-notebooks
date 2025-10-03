import gsd,gsd.hoomd
import numpy as np
import hoomd
import freud


kT= 1.5
a = np.sqrt(2)*2.0


fcc = freud.data.UnitCell.fcc()
box, positions = fcc.generate_system(5)

frame = gsd.hoomd.Frame()
frame.configuration.box = [box.Lx*a,box.Ly*a,box.Lz*a,0,0,0]

frame.particles.N = len(positions)

frame.particles.position = positions*a
frame.particles.types = ["A"]

output = gsd.hoomd.open('init_fcc.gsd',mode='w')
output.append(frame)
output.flush()

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
simulation.create_state_from_gsd('init_fcc.gsd')

# Velocities
simulation.state.thermalize_particle_momenta(filter=hoomd.filter.All(), kT=kT)

# Write trajectory
gsd = hoomd.write.GSD(mode='wb',trigger=hoomd.trigger.Periodic(1),
                      filename='run_liquid_MTTK_%1.2f_%1.2f.gsd'%(density,kT),
                      dynamic=['property','momentum'])

simulation.operations.writers.append(gsd)

# Equilibration
#nve = hoomd.md.methods.ConstantVolume(filter=hoomd.filter.All())
#integrator.methods = [nve]

#npt = hoomd.md.methods.ConstantPressure(filter=hoomd.filter.All()
#                                        , S=0, tauS=1, couple='none',
#                                        thermostat=hoomd.md.methods.thermostats.MTTK(kT=kT,tau=0.5))

nvt = hoomd.md.methods.ConstantVolume(filter=hoomd.filter.All(),
                                        thermostat= hoomd.md.methods.thermostats.MTTK(kT=1.5,
    tau=simulation.operations.integrator.dt * 100)
)

#langevin = hoomd.md.methods.Langevin(filter=hoomd.filter.All(), kT=1.5)
#integrator.methods = [langevin]

integrator.methods = [nvt]

#brownian = hoomd.md.methods.Brownian(filter=hoomd.filter.All(), kT=1.5)
#integrator.methods = [brownian]

simulation.run(10_000)

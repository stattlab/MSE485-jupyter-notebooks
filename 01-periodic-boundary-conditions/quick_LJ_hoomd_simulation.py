import hoomd
import gsd, gsd.hoomd

cell = hoomd.md.nlist.Cell(buffer=0.4)

lj = hoomd.md.pair.LJ(nlist=cell,default_r_cut=3.0)
lj.mode='shift'
lj.params[("A", "A")] = dict(sigma=1.0, epsilon=1.0)


integrator = hoomd.md.Integrator(dt=0.005)
integrator.forces= [lj]

# Setup simulation state and initial configuration
simulation = hoomd.Simulation(device=hoomd.device.auto_select(),seed=42)
simulation.operations.integrator = integrator

# Make initial snapshot

frame = gsd.hoomd.Frame()
frame.particles.N = 10
frame.particles.position = [[-4.5,0,0],
                            [0,0,0],
                            [4.5,1,1],
                            [2,3,-4],
                            [1,1,1],
                            [-4,3,2],
                            [-2,0,0],
                            [2,3,-3],
                            [-1,1,0],
                            [0,2,4]]
frame.configuration.box = [10,10,10,0,0,0]
frame.particles.types=['A']

simulation.create_state_from_snapshot(frame)


# Velocities
simulation.state.thermalize_particle_momenta(filter=hoomd.filter.All(), kT=1.0)

# Write trajectory
gsd = hoomd.write.GSD(mode='wb',trigger=hoomd.trigger.Periodic(10),
                      filename='LJ_nve.gsd',
                      dynamic=['property','momentum'])

simulation.operations.writers.append(gsd)

# Equilibration
nve = hoomd.md.methods.ConstantVolume(filter=hoomd.filter.All())
integrator.methods = [nve]

simulation.run(1_000)

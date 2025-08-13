import hoomd

cell = hoomd.md.nlist.Cell(buffer=0.4)

lj = hoomd.md.pair.LJ(nlist=cell,default_r_cut=3.0)
lj.mode='shift'
lj.params[("A", "A")] = dict(sigma=1.0, epsilon=1.0)

harmonic_bond = hoomd.md.bond.Harmonic()
harmonic_bond.params["AA"] = dict(k=1000.0,r0=1.0)

harmonic_angle = hoomd.md.angle.Harmonic()
harmonic_angle.params["AAA"] = dict(k=20.0,t0=3.14)

integrator = hoomd.md.Integrator(dt=0.005)
integrator.forces= [lj,harmonic_bond,harmonic_angle]

# Setup simulation state and initial configuration
simulation = hoomd.Simulation(device=hoomd.device.auto_select(),seed=42)
simulation.operations.integrator = integrator
simulation.create_state_from_gsd('init.gsd')

# Velocities
simulation.state.thermalize_particle_momenta(filter=hoomd.filter.All(), kT=1.5)

# Write trajectory
gsd = hoomd.write.GSD(mode='wb',trigger=hoomd.trigger.Periodic(1),
                      filename='run_hoomd.gsd',
                      dynamic=['property','momentum'])

simulation.operations.writers.append(gsd)

# Equilibration
nve = hoomd.md.methods.ConstantVolume(filter=hoomd.filter.All())
integrator.methods = [nve]

simulation.run(1_000)

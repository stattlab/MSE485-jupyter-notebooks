import numpy as np
import freud
import glob
import gsd, gsd.hoomd


trajectory = gsd.hoomd.open('run_liquid_0.80_0.10_short.gsd','r')
trajectory_out = gsd.hoomd.open('run_liquid_0.80_0.10_short_q64.gsd','w')

for frame in trajectory:
    points=frame.particles.position
    box = frame.configuration.box

    q6 = freud.order.Steinhardt(l=6,average=True)
    q6.compute(system=(box,points),neighbors={"num_neighbors": 12})
    q6 = q6.particle_order

    q4 = freud.order.Steinhardt(l=4,average=True)
    q4.compute(system=(box,points),neighbors={"num_neighbors": 12})
    q4 = q4.particle_order

    frame.log["particles/q6"]=q6
    frame.log["particles/q4"]=q4
    trajectory_out.append(frame)




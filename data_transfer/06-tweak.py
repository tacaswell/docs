import databroker
import bluesky as bs
import bluesky.plans as bp
from bluesky.examples import motor, det
import portable_mds.sqlite.mds
import matplotlib.pyplot as plt
plt.ion()

dRE = bs.RunEngine({})

pdms = portable_mds.sqlite.mds.MDS({'directory': '/tmp/pmds', 'timezone': 'US/Central'})
db = databroker.Broker(pdms, None)

dRE.subscribe('all', pdms.insert)

uid, = dRE(bp.tweak(det, 'det', motor, .1))

tbl = db.get_table(db[uid])
x, y = tbl.motor, tbl.det

fig, ax = plt.subplots()
ax.plot(x, y, marker='o')

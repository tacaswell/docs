import bluesky as bs
import bluesky.plans as bp
import bluesky.callbacks as bc
from bluesky.examples import motor, det
from bluesky.utils import install_qt_kicker

import matplotlib.pyplot as plt

install_qt_kicker()
plt.ion()

det.exposure_time = .1

dRE = bs.RunEngine({'REtype': 'demonstration'})


dRE(bp.scan([det], motor, -5, 5, 111),
    [bc.LiveTable([motor, det]), bc.LivePlot('det', 'motor')])

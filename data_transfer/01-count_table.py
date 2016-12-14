import bluesky as bs
import bluesky.plans as bp
import bluesky.callbacks as bc
from bluesky.examples import motor

dRE = bs.RunEngine({})


dRE(bp.count([motor], num=5), bc.LiveTable([motor]))

import bluesky as bs
import bluesky.plans as bp
import bluesky.plan_tools as bpt
import bluesky.callbacks as bc
import bluesky.utils as bu
import matplotlib.pyplot as plt

from bluesky.examples import motor1, motor2, det1, det2, det4

plt.ion()

det4.exposure_time = .5

bu.install_qt_kicker()

dRE = bs.RunEngine({'REtype': 'demonstration'})


def raster_plan():
    plan = bp.outer_product_scan([det1, det2, det4], motor1, -3, 3, 5,
                                 motor2, -5, 5, 7, True)

    yield from plan


def make_callbacks():
    fig, ax = plt.subplots()

    return [bc.LiveTable([motor1, motor2, det4, det1, det2]),
            bc.LiveRaster((5, 7), 'det4', xlabel='motor1',
                          ylabel='motor2', ax=ax)]

bpt.plot_raster_path(
    raster_plan(),
    x_motor='motor1', y_motor='motor2',
    probe_size=.3)


dRE(raster_plan(), make_callbacks())

import matplotlib.pyplot as plt
import numpy as np
import lmfit
import bluesky.plans as bp
import bluesky.callbacks as bc
import bluesky.utils as bu
from bluesky.examples import motor, SynGauss
from bluesky import RunEngine
plt.ion()
bu.install_qt_kicker()

noisy_det = SynGauss('noisy_det', motor, 'motor', center=0, Imax=100,
                     noise='poisson', sigma=1)

RE = RunEngine({})


def errorbar(lmfit_result, param_name):
    # width of 95% conf interfal:
    ci = lmfit_result.conf_interval()
    return ci[param_name][-2][1] - ci[param_name][1][1]


def gaussian(x, A, sigma, x0):
    return A * np.exp(-(x - x0)**2 / (2 * sigma**2))


model = lmfit.Model(gaussian)
guess = {'A': 10,
         'x0': 1,
         'sigma': lmfit.Parameter('sigma', 3, min=0)}


def scan_gaussian(detectors, motor, start, stop, num, *, ax=None,
                  err_thresh=0.03):

    if ax is None:
        ax = plt.gca()
    main_detector = detectors[0]
    main_motor_field, *_ = motor.describe()
    lf = bc.LiveFit(model, main_detector.name, {'x': main_motor_field}, guess)
    lfp = bc.LiveFitPlot(lf, color='r', ax=ax)
    lp = bc.LivePlot(main_detector, main_motor_field,
                     linestyle='none', marker='o', ax=ax)

    @bp.subs_decorator([lfp, lp])
    @bp.stage_decorator(list(detectors) + [motor])
    @bp.run_decorator()
    def plan():
        while True:
            for step in np.linspace(start, stop, num):
                yield from bp.abs_set(motor, step, wait=True)
                yield from bp.trigger_and_read(list(detectors) + [motor])
                yield from bp.checkpoint()

            err = errorbar(lf.result, 'sigma')
            if err < err_thresh:
                break

    yield from plan()


RE(scan_gaussian([noisy_det], motor, -5, 5, 100, ax=plt.gca()))

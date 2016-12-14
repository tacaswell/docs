import path
import os
import bluesky as bs
import bluesky.plans as bp
import bluesky.callbacks as bc
import csv
from bluesky.examples import motor, det
from bluesky.utils import install_qt_kicker

import matplotlib.pyplot as plt

install_qt_kicker()
plt.ion()

dRE = bs.RunEngine({})

det.exposure_time = .1


class CSVWriter(bc.CallbackBase):
    def __init__(self, fields, fname_format, fpath):
        self._path = path.Path(fpath)
        os.makedirs(self._path, exist_ok=True)
        self._fname_fomat = fname_format
        self._fields = fields
        self._writer = None
        self._fout = None

    def close(self):
        if self._fout is not None:
            self._fout.close()
        self._fout = None
        self._writer = None

    def start(self, doc):
        self.close()

        fname = self._path / self._fname_fomat.format(**doc)

        self._fout = open(fname, 'xt')
        self._writer = csv.writer(self._fout)

    def descriptor(self, doc):
        if self._writer is not None:
            self._writer.writerow(self._fields)

    def event(self, doc):
        data = doc['data']
        if self._writer is not None:
            self._writer.writerow(data[k] for k in self._fields)

    def stop(self, doc):
        self.close()


def create_callbacks():
    return [bc.LiveTable([motor, det]), bc.LivePlot('det', 'motor')]


csv_writer = CSVWriter(('motor', 'det'),
                       '{uid:.6s}_{scan_id:04d}_{user}.csv',
                       '/tmp/export_demo')

dRE.subscribe('all', csv_writer)
dRE(bp.scan([det], motor, -5, 5, 111), create_callbacks(), user='tcaswell')

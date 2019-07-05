=================
 Device Registry
=================

.. contents::
   :local:

Branches and Pull requests
==========================


Abstract
========

We need a programmatic way to ask what `ophyd.Device` instances are available
and what category of device they are.  This is important for building the
next level of UI on top of the current system.

As deployed at NSLS-II ``ophyd`` devices are instantiated in IPython
startup profiles and the beamline staff / users have to just know what
their names are.  While this mostly works, it does leave some key
use-cases awkward to work with (such as ``%wa``).  We have had several
generations of namespace-scraping (such as
`ophyd.utils.instances_from_namespace`,
`ophyd.utils.ducks_from_namespace`, and the ``_ophyd_labels_`` effort)
based efforts to try and address this.  Going forward we will want to
use ophyd/bluesky in a non-IPython context and to construct the set of
instantiated devices in a more structured way (such as ``happi`` which
is in use at LCLS).

This object will not be a `ophyd.Device`, but an oracle for
retrieving them by name, category, or general query.



Detailed description
====================



Implementation
==============

- must not be done in ``__init__`` of Device, must be opt-in
- a singleton 'BeamlineDevice' object is too heavy-weight
- should be reasonable to construct ad-hoc or programtically from a
  database
- should support rich queries + common short cuts
  - "give me all of the instance which are of type EpicsMotor"
  - "give me all of the instance which are sub-classes of EpicsMotor"
  - "give me the motor called 'theta'"
  - "give me all of the motors in the goiniometer"
  - "give me all of the AreaDetectors"
  - "give me all of the QuadEMs"
  - "give me all of the prosillica cameras"
  - "give me everything on stand XYZ"
  - "give me all of the things that can obstruct the beam"
  - "give me every positioner on the beamline"
  - "give me the set of motors the users are allowed to move in beamline mode X"
  - "give me the detectors involved in beamline mode X"
  - "give me the baseline devices"
- how to handle nesting for queries?
  - the right answers for the above may or may not map 1:1 with
    'natural' ophyd objects
- does the state to answer those questions live on the ophyd objects
  or in the registry?
  - if it lives on the ohpydobj, then


Backward compatibility
======================

None, new opt-in feature

Alternatives
============

 - status quo

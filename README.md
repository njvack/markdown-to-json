# HTML/Markdown to Brain Imaging Data Structure (BIDS) JSON converter

Hand-writing JSON is a pain in the ass. Unfortunately, the [Brain Imaging Data Structure](http://bids.neuroimaging.io/) specifies the main experiment description be written in JSON.

This tool provides a way to a convert a subset of HTML into JSON, such that it's easy to write the description file in markdown, convert it to HTML, and output BIDS-compliant JSON. The converter uses headings as JSON keys, and nests following content. Lists are supported and converted to arrays.

## Example:

```
# Name

studyforrest

# Description

This dataset contains versatile brain imaging data for natural auditory
stimulation and real­-life cognition. It includes high­-resolution functional
magnetic resonance (fMRI) data from 20 participants recorded at high field
strength (7 Tesla) during prolonged stimulation with an auditory feature film
('Forrest Gump'). In addition, a comprehensive set of auxiliary data (T1w,
T2w, DTI, susceptibility-weighted image, angiography) as well as measurements
to assess technical and physiological noise components have been acquired.

Participants were also scanned with a musical genre stimulation paradigm...

# License

PDDL

# Authors

* Michael Hanke
* Florian J. Baumgartner
* Pierre Ibe
* ...

# How to Acknowledge

Please follow good scientific practice by citing the most appropriate
publication(s) describing the aspects of this datasets that were used in a
study.

# Version History

## 1

* Initial Release (22 Jan 2014)

## 2

* Physiological data fixes and additions (Feb 20 2014)
* physiological data for all participants in original sampling rate
  (physio_pristine.txt.gz) was added
* physiological data for sub008 run005 was updated to strip leading data
  samples prior to the fixes MR
* trigger signal. Thanks to Christine Guo for the report
* trigger log for first MR trigger (only) was offset by one data sample
  (5­ - 10ms)

```
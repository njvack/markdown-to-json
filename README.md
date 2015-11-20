# HTML/Markdown to Brain Imaging Data Structure (BIDS) JSON converter

Hand-writing JSON is a pain in the ass. Unfortunately, the [Brain Imaging Data Structure](http://bids.neuroimaging.io/) specifies the main experiment description be written in JSON.

This tool provides a way to a convert a subset of HTML into JSON, such that it's easy to write the description file in markdown, convert it to HTML, and output BIDS-compliant JSON. The converter uses headings as JSON keys, and nests following content. Lists are supported and converted to arrays.

## Example:

```
# Name

Test Study

# Description

This dataset contains structural, functional, and diffusion-weighted images
for a large population of people. There are a lot of files here.

During the functional scan, participants performed a numeric 4-back task.

# License

PDDL

# Authors

* Nathan J. Vack
* Tim Berners-Lee
* ...

# How to Acknowledge

Please follow good scientific practice by citing the most appropriate
publication(s) describing the aspects of this datasets that were used in a
study.

# Version History

## 1

Initial Release (2014-11-20)

## 2

* Imaging additions (2014-12-06)
* Added T1-weighted structural images for new participants
* Added fMRI images for new
  participants
* Updated study description

```

should translate to:

```
{
    "Name": "Test Study",
    "Description": "This dataset contains structural, functional, and diffusion-weighted images for a large population of people. There are a lot of files here.\n\nDuring the functional scan, participants performed a numeric 4-back task.",
    "License": "PDDL",
    "Authors": [
        "Nathan J. Vack",
        "Tim Berners-Lee",
        "..."
    ],
    "HowToAcknowledge": "Please follow good scientific practice by citing the most appropriate publication(s) describing the aspects of this datasets that were used in a study.",
    "VersionHistory": {
        "1": "Initial Release (2014-11-20)",
        "2": [
            "Imaging additions (2014-12-06)",
            "Added T1-weighted structural imag",
            "Added fMRI images for new participants",
            "Updated study description"
        ]
    }
}
```
# Changelog

## 2.1.1 - 2024-05-09

### Added

- Lists with blank values will parse to something instead of blowing up.

### Removed

- No longer supports python 3.6 or 3.7

## 2.0.0 - 2023-06-04

### Added

- Convenience exports, markdown_to_json.dictify and markdown_to_json.jsonify

### Fixed

- Can handle missing H1
- Can handle unicode
- Updated vendorized libraries

### Changed

- Supports more datastructures without throwing errors. May be lossy.
- Returns standard library OrderedDict instead of vendorized one.

### Removed

- No longer supports python 2.

## 1.1.0 - 2023-06

### Fixed

- MR processed

## [1.0.0] - 2015-12-03

### Added

- Initial release
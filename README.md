# Markdown to JSON converter

## Description

A simple tool to convert Markdown (technically CommonMark) data into JSON. It uses headings as JSON keys, and the stuff following headings as values. Lists are turned into arrays. Higher heading values yield nested JSON keys.

## Why the hell would I want to do this?

Sometimes, you need to write JSON. Writing it by hand is a pain. It's a fiddly format and there are strings to escape and commas and it looks bad and you'll have validation errors and yuck. You could build a custom tool to write your particular JSON, but that's a bunch of work. You could use some JSON-specific editor, but they tend to be pretty neckbeard. Sometimes, you maybe just want to open a text editor and pump out a little nested data structure in a human-readable way.

This lets you do that. Markdown is easy.


## Example:

The markdown:

```
# Description

This is an example file

# Authors

* Nate Vack
* Someone Else

# Versions

## Version 1

Here's something about Version 1; I said "Hooray!"

## Version 2

Here's something about Version 2
```

will translate to the JSON:

```
{
  "Description": "This is an example file",
  "Authors": ["Nate Vack", "Someone Else"],
  "Versions": {
    "Version 1": "Here's something about Version 1; I said \"Hooray!\"",
    "Version 2": "Here's something about Version 2"
  }
}
```


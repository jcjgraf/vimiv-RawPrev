## Vimiv RawPrev
> [vimiv](https://github.com/karlch/vimiv-qt) plugin for RAW images support

vimiv RawPrev enables support for RAW images by extracting the embedded thumbnail from the RAW image.

### Supported Formats
The following RAW formats are currently supported:

| **Format**   | **Extension** | **Dependency**                           |
| :---         | :---:         | :---                                     |
| Canon Raw 2  | `.cr2`        | [dcraw](https://www.dechifro.org/dcraw/) |
| Canon Raw 3  | `.cr3`        | [exiftool](https://exiftool.org/)        |
| Fujifilm RAF | `.raf`        | [dcraw](https://www.dechifro.org/dcraw/) |

### Installation
- Depending on the RAW file format, different dependencies are required. Please see the list above and install the required dependencies.
- Clone this project into `$XDG_DATA_HOME/vimiv/plugins/`
- Activate vimiv RawPrev by adding `rawprev =` to the `PLUGINS` section of `$XDG_CONFIG_HOME/vimiv/vimiv.conf`.

### Usage
Everything is done automatically, simply enjoy viewing your RAW images.

### Contribute
If you would like to add support for a new RAW file format feel free to open a PR with the appropriate additions. In case you do not know how to implement it, you are also welcome to open an issue and submit an adequate sample file.

### Similar Plugins
- The [imageformats](https://karlch.github.io/vimiv-qt/documentation/configuration/plugins.html#imageformats) enables support for RAW images too. However, it is based on [qtraw](https://gitlab.com/mardy/qtraw) which seems to be broken currently.

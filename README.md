## Vimiv RawPrev
> [vimiv](https://github.com/karlch/vimiv-qt) plugin for RAW images support

Vimiv RawPrev enables support for RAW images by extracting the jpeg thumbnail embedded in RAW images.

### Installation
* Depending on the desired format, different dependencies are required. Please see the list below.
- This plugin is currently based on `dcraw` which needs to be installed.
- Clone this project into `$XDG_DATA_HOME/vimiv/plugins/`
- Activate Vimiv RawPrev by adding `rawprev =` to the `PLUGINS` section of `$XDG_CONFIG_HOME/vimiv/vimiv.conf`.

### Usage
Everything is done automatically, simply enjoy viewing your RAW images.

### Supported Formats
The following RAW formats are currently supported:

| **Format**  | **Extension** | **Dependancy**                           |
| :---        | :---:         | :---                                     |
| Canon Raw 2 | `.cr2`        | [dcraw](https://www.dechifro.org/dcraw/) |
| Canon Raw 3 | `.cr3`        | [exiftool](https://exiftool.org/)        |

### Contribute
If you would like support for a new RAW format feel free to open a PR with the appropriate additions. In case you do not know how this is implemented, you are also very welcome to open an issue and submit an adequate sample file.

Let me also know if you detect some inconsistencies with the type detection. I.e. a non-raw file is being detected as a raw or vice-versa.

### Similar Plugins
- The [imageformats](https://karlch.github.io/vimiv-qt/documentation/configuration/plugins.html#imageformats) enables support for RAW images too. However, it is based on [qtraw](https://gitlab.com/mardy/qtraw) which seems to be broken currently.

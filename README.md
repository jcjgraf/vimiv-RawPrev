## Vimiv RawPrev
> [vimiv-qt](https://raw.github.com/karlch/vimiv-qt) plugin for RAW images support

**This plugin does not yet work with the current version of vimiv, we are working on a suitable integration**

Vimiv RawPrev enables support for RAW images by extracting the jpeg thumbnail embedded in RAW images.

### Installation
- This plugin is currently based on `dcraw` which needs to be installed.
- Clone this project into `$XDG_DATA_HOME/vimiv/plugins/`
- Activate Vimiv Importer by adding `rawprev =` to the `PLUGINS` section of `$XDG_CONFIG_HOME/vimiv/vimiv.conf`.

### Usage
Everything is done automatically, simply enjoy viewing your RAW images.

### Similar Plugins
- The [imageformats](https://karlch.github.io/vimiv-qt/documentation/configuration/plugins.html#imageformats) enables support for RAW images too. However, it is based on [qtraw](https://gitlab.com/mardy/qtraw) which seems to be broken currently.

### Note
This plugin is currently just a proof of concept and there are many open todos...

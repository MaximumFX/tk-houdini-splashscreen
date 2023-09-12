[![Python 2.6 2.7 3.7](https://img.shields.io/badge/python-2.6%20%7C%202.7%20%7C%203.7-blue.svg)](https://www.python.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/maximumfx/tk-houdini-splashscreen?include_prereleases)
[![GitHub issues](https://img.shields.io/github/issues/maximumfx/tk-houdini-splashscreen)](https://github.com/maximumfx/tk-houdini-splashscreen/issues)
# tk-houdini-splashscreen

`tk-houdini-splashscreen` is a Shotgun Toolkit app to customize the Splash screen to the Project billboard.

## Installation

Add the `tk-houdini-splashscreen` app to the tk-desktop engine.

Add the following code the `before_app_launch` hook of `tk-multi-launchapp`:
```python
splash = self.parent.engine.apps.get('tk-houdini-splashscreen')
if splash is not None:
    splash.create_splash(app_path, app_args, version)
else:
    print('Something went wrong while initializing tk-houdini-splashscreen')
```

## Configuration

| Type     | Key                      | Description                                                                          | Default value                       |
|----------|--------------------------|--------------------------------------------------------------------------------------|-------------------------------------|
| str      | `oiiotool`               | Path to oiiotool binary. If blank, the hoiiotool included with Houdini will be used. |                                     |
| template | `splash_screen_template` | Template for the Splash Screen file.                                                 | `editorial/houdini_splash_file.jpg` |

## License

[MIT](https://choosealicense.com/licenses/mit/)

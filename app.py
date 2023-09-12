# MIT License

# Copyright (c) 2023 MaximumFX

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sgtk


class TkHoudiniSplashScreen(sgtk.platform.Application):
    """
    A Shotgun Toolkit app to customize the Houdini splash screens to the project billboard.
    """

    def init_app(self):
        """
        Initialize the app.
        """
        print('Started Splash Screen app')

    def create_splash(self, app_path, app_args, version):
        """
        Create the splash screen for each DCC

        :param app_path: (str) The path of the application executable
        :param app_args: (str) Any arguments the application may require
        :param version: (str) version of the application being run if set in the
            "versions" settings of the Launcher instance, otherwise None

        """
        self.logger.info('Setting up splash screen for Houdini version {}'.format(version))

        app_payload = self.import_module("app")
        splashscreen = app_payload.splashscreen.Splashscreen(self)

        splashscreen.create(app_path, version)

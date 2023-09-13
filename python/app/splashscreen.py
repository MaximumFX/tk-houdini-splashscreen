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

import os
import os.path
import subprocess
import sys
import time

if sys.version_info >= (3, 0):
    from urllib.parse import urlparse
    from urllib.request import urlretrieve
if (3, 0) > sys.version_info >= (2, 5):
    from urlparse import urlparse
    from urllib import urlretrieve

class Splashscreen:
    def __init__(self, app, parent=None):
        self.app = app
        self.logger = app.logger

    def create(self, app_path, version):
        current_engine = self.app.engine
        sg = current_engine.shotgun
        current_context = current_engine.context

        # Get data from ShotGrid
        project = sg.find_one(
            'Project',
            [['id', 'is', current_context.project.get('id')]],
            ['billboard', 'name']
        )

        # Check if project has billboard
        if project.get('billboard') is None:
            return

        billboard_url = project.get('billboard').get('url')

        # TODO check default value
        splash_file = self.app.get_template("splash_screen_template").apply_fields({})
        directory, filename = os.path.split(splash_file)
        filename, extension = os.path.splitext(filename)
        f, ext = os.path.splitext(urlparse(billboard_url).path)
        tmp_splash_file = os.path.join(directory, filename + '_tmp' + ext)
        tmp_splash_png = os.path.join(directory, filename + '_tmp.png')

        self.logger.debug('Splash file path: {}'.format(splash_file))

        c_oiiotool = self.app.get_setting("oiiotool")
        if c_oiiotool is not '' and os.path.exists(c_oiiotool):
            oiiotool = c_oiiotool
        else:
            oiiotool = os.path.join(os.path.dirname(app_path), 'hoiiotool.exe')

        render_splash = True
        # Check if exists and image source is the same
        if os.path.exists(splash_file):
            info = subprocess.Popen(
                [oiiotool, '--info', '-v', splash_file],
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            info_out, info_err = info.communicate()
            info_data = info_out.decode("utf-8").split('\n')
            for data in info_data:
                if "ImageDescription" in data:
                    if urlparse(billboard_url).path in data:
                        render_splash = False

            info.wait()

        if render_splash:
            self.logger.debug('Creating new splash file.')
            self.__create_splash(oiiotool, '800x415', 'white', 312, '+445+172', billboard_url, tmp_splash_file,
                                 tmp_splash_png, splash_file, project.get('name'), version)
        else:
            self.logger.debug('Splash file exists, skipping creation.')

        try:
            self.logger.debug('Setting splash file and message.')
            os.environ["HOUDINI_SPLASH_FILE"] = splash_file
            houdini = os.path.splitext(os.path.split(app_path)[1])[0]
            houdini_version = ''
            if 'core' in houdini:
                houdini_version = 'Core'
            elif 'fx' in houdini:
                houdini_version = 'FX'
            os.environ["HOUDINI_SPLASH_MESSAGE"] = 'Houdini {type} {version}\n{project}'\
                .format(type=houdini_version, version=version, project=project.get('name'))

        except Exception as error:
            self.logger.error("Something went wrong %s..." % str(error))

    def __create_splash(self, oiiotool, resolution, logo_type, logo_width, logo_position, image_url, tmp_splash_file,
                        tmp_splash_png, splash_file, project_name, version):
        logo = os.path.join(self.app.disk_location, 'resources', 'logos', 'Houdini_{}_color.png'.format(logo_type))

        try:
            # Download file
            urlretrieve(image_url, tmp_splash_file)

            # Add alpha and resize
            process_bg = subprocess.Popen([oiiotool, tmp_splash_file, '--ch', 'R,G,B,A=1.0', '--resize', resolution,
                                           '-o', tmp_splash_png])
            process_bg.wait()

            # Add logo
            cmd = [oiiotool,
                   logo, '--resize', '{}x0'.format(logo_width), '--origin', logo_position,
                   tmp_splash_png, '--over',
                   ]

            # Add text
            if "19.5" in version:
                cmd.extend(['--text:x=443:y=265:size=28:font=Arial', project_name])

            # Set output
            cmd.extend([
                '--caption', urlparse(image_url).path,
                '--ch', 'R,G,B',
                '-o', splash_file
            ])

            process = subprocess.Popen(
                cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            stdout, stderr = process.communicate()
            self.logger.debug(stdout.decode("utf-8"))

            if stderr:
                err = stderr.decode("utf-8")
                if 'WARNING' in err:
                    self.logger.warning(err)
                else:
                    self.logger.error(err)
                    raise Exception(err)

            process.wait()

            os.remove(tmp_splash_file)
            os.remove(tmp_splash_png)

            return True
        except Exception as error:
            self.logger.error("An error occurred while saving the billboard image. {}".format(error))
            return False

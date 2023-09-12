import os
import shutil
import subprocess

try:
    import urlparse
except ImportError:
    from urllib.parse import urlparse

dir = os.path.dirname(__file__)


def execute(app_path, app_args, version, engine_name, **kwargs):
    """
    The execute functon of the hook will be called prior to starting the required application

    :param app_path: (str) The path of the application executable
    :param app_args: (str) Any arguments the application may require
    :param version: (str) version of the application being run if set in the
        "versions" settings of the Launcher instance, otherwise None
    :param engine_name (str) The name of the engine associated with the
        software about to be launched.

    """
    if engine_name == 'tk-houdini':

        # Get data from ShotGrid
        billboard = {
            'url': 'https://sg-media-ireland.s3-accelerate.amazonaws.com/88d8cd8231473ee111ba3a49ac87c08dc704e4c1/2dbb6248bc6c95a31ebd8d37d8056b7f168f0eac/bpvjzk0QXbJPV4wVwrHuYiq1TbP.jpg?response-content-disposition=filename%3D%22bpvjzk0QXbJPV4wVwrHuYiq1TbP.jpg%22&x-amz-meta-user-id=1512&x-amz-meta-user-type=HumanUser&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIAYJG6Z4JIZZ2276FL%2F20230620%2Feu-west-1%2Fs3%2Faws4_request&X-Amz-Date=20230620T083819Z&X-Amz-SignedHeaders=host&X-Amz-Expires=900&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEEkaCXVzLWVhc3QtMSJGMEQCIAh7f8TvaivJp0a%2BuyU4u0nTIxNEsUwFBuPm8XnHTAnZAiBPx4C%2FgENgKUODCpXq1ctLe46fpzWJeWsyLkzFdc4BySqhAgih%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8BEAAaDDU2OTU1MDQzMDgwMSIMFhfD%2BRZT%2B8xJPaEFKvUBuJEkpVS5aaQyjq3%2FgzwsgUqOLmxpguswCargqkMG7qiGa99MkwSWqLKB2X6qbW9lQxxrwyQ7em50SGqaunQ4ElqiXVpIkFi5QoELHqYkR7N%2FdeCCTOC9bH%2F6y39LKwNK2AtTx7x3Or%2FzuQQ1PcQO0Xls%2Bs0VkWCWuIt3M2VeJHWKVrA%2Fr6eCXJhQrgcNakPljQDCQONRk%2BxgdpmYc9RFeGYpxVmYkKjkseUT3h9xPNpRNqIN1Ez%2BXt77Jg%2BfkRnJPbKOw4tK5NyMOhCgIMiZViO7yU5yDQgJLtC%2BVnTZ0wNhvkeId4NtsAaXfRerdOE3AfQ4HHMwrLzFpAY6ngG6kJ3kyzu8jRm1vcZJe1Gp22FVb%2BHZQbj3ovHHwcsINmK%2BnpWg8kJTGpGmuvBghaei%2BZ%2Fg6PUy1QPpk7Fgej8xvVp%2B35MD0%2BbXEMZwku3aJ%2FSaLchdCKXi1i0z21tWrN8FI7NaAb%2B4bCiPjZI7xsW3K5r%2FNPW0qYHv9fvQSPLVaY6pF6UmBJX6AEM2hNOHfRFyMCPgk48At5v3BaN6Dw%3D%3D&X-Amz-Signature=4d8f9858e65685dba19cc2280b073ba433a06fe8d220fb8ca9017762b23091e4'}
        # TODO check if has billboard

        project_name = 'Pipeline Testproject'

        splash_file = os.path.join(dir, 'houdini_splash_file.png')
        directory, filename = os.path.split(splash_file)
        filename, extension = os.path.splitext(filename)
        f, ext = os.path.splitext(urlparse(billboard.get("url")).path)
        tmp_splash_file = os.path.join(directory, filename + '_tmp' + ext)
        tmp_splash_png = os.path.join(directory, filename + '_tmp.png')

        # TODO check if exists/matches

        oiiotool = os.path.join(os.path.dirname(app_path), 'hoiiotool.exe')

        logo_type = 'white'
        logo = os.path.join(dir, '..', 'resources', 'Houdini_{}'.format(logo_type), 'Houdini_{}_color.png'.format(logo_type))

        try:
            # if sys.version_info[0] == 3:
            #     import urllib.request
            #     urllib.request.urlretrieve(billboard.get('url'), tmp_splash_file)
            # else:
            #     import urllib
            #     urllib.urlretrieve(billboard.get('url'), tmp_splash_file)
            shutil.copyfile(os.path.join(dir, '..', 'resources', 'billboard.jpg'), tmp_splash_file)

            subprocess.Popen([oiiotool, tmp_splash_file, '--ch', 'R,G,B,A=1.0', '-o', tmp_splash_png])

            cmd = [oiiotool,
                   logo, '--resize', '312x0', '--origin', '+445+172',
                   tmp_splash_png, '--resize', '800x450', '--over',
                   ]

            if "19.5" in app_path:
                cmd.extend(['--text:x=445:y=200:size=40', project_name])
            cmd.extend(['-o', splash_file])

            process = subprocess.Popen(
                cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            stdout, stderr = process.communicate()
            print(stdout.decode("utf-8"))

            if stderr:
                print(stderr.decode("utf-8"))
                raise Exception(stderr.decode("utf-8"))

            # os.remove(tmp_splash_file)
            # os.remove(tmp_splash_png)
        except Exception as error:
            print("An error occurred while saving the billboard image. {}".format(error))
            return

        try:
            os.environ["HOUDINI_SPLASH_FILE"] = splash_file

        except Exception as error:
            print("Something went wrong %s..." % str(error))


execute(r"C:\Program Files\Side Effects Software\Houdini 19.0.720\bin\happrentice.exe", '', '', 'tk-houdini')

import uuid
from datetime import datetime
from pathlib import Path
from os import walk, urandom
from platform import system as get_os_type  # module to check the platform
import subprocess


class FileList:

    @classmethod
    def execute(cls, *args):
        if args:
            print(datetime.now(), args)
        else:

            get_uuid = uuid.uuid4()
            get_name = 'TestName_' + str(int(datetime.now().timestamp()))
            print(datetime.now(), 'The test was started')
            print(datetime.now(), "GUID: %s Name: %s " % (get_uuid, get_name))
            prep = cls.prep()
            if prep is True:
                cls.execute('The timestamp is devisible by 2')
                cls.execute('Going to the [run] stage')
                cls.run()
                cls.execute('Going to the [clean_up] stage')
                cls.clean_up()
                cls.execute('The test was ended')
            elif prep is False:
                cls.execute('The timestamp is not devisible by 2, interrupting the test')
                # cls.execute('Going to the [clean_up] stage')
                # cls.clean_up()
                cls.execute('The test was ended')

    @classmethod
    def prep(cls):
        the_timestamp = int(datetime.now().timestamp())
        # home_directory = None
        timestamp_division = the_timestamp % 2
        cls.execute('The test timestamp since UNIX epoch = %s' % the_timestamp)
        if timestamp_division == 0:

            return True
        else:

            return False

    @classmethod
    def run(cls):
        try:
            home_directory = str(Path.home())
            cls.execute('The home directory is %s' % home_directory)
            _, _, list_of_target_files = next(walk(home_directory))  # Getting names of target directory's files
            cls.execute('Files in HOME directory are: %s' % list_of_target_files)

        except:
            cls.execute('ERROR cannot list HOME directory')

    @classmethod
    def clean_up(cls):
        pass


class RandomFile:
    os_type = get_os_type()
    path_to_ps = "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe"

    @classmethod
    def execute(cls, *args):
        if args:
            print(datetime.now(), args)
        else:

            get_uuid = uuid.uuid4()
            get_name = 'TestName_' + str(int(datetime.now().timestamp()))
            print(datetime.now(), 'The test was started')
            print(datetime.now(), "GUID: %s Name: %s " % (get_uuid, get_name))
            prep = cls.prep()
            if prep is True:
                cls.execute('Memory more that 1 Gb --> Going to the [run] stage')
                cls.run()
                cls.execute('Going to the [clean_up] stage')
                cls.clean_up()
                cls.execute('The test was ended')
            elif prep is False:
                cls.execute('The RAM is less then 1 Gb')
                # cls.execute('Going to the [clean_up] stage')
                # cls.clean_up()
                cls.execute('The test was ended')

    @classmethod
    def prep(cls):
        # os_type = get_os_type()  # detecting of the OS
        cls.execute('The OS is %s' % RandomFile.os_type)
        if RandomFile.os_type == 'Linux':
            cls.execute('Checking RAM...')
            try:

                out = subprocess.check_output(['cat',
                                               '/proc/meminfo']).decode("utf-8").split('MemFree:')[1].strip().split(' ')[0]
                cls.execute('Free physical RAM: %s' % out)

                if int(out) < 1048576:

                    return False
                elif int(out) >= 1048576:
                    return True
                else:
                    cls.execute('ERROR wrong RAM output: %s' % out)
                    return False

            except subprocess.CalledProcessError as error_message:
                cls.execute('ERROR while RAM calculation. System output: %s' % error_message)

        elif RandomFile.os_type == 'Windows':
            cls.execute('Checking RAM...')
            try:
                output = subprocess.check_output(
                    [RandomFile.path_to_ps, 'Get-CIMInstance Win32_OperatingSystem | Select FreePhysicalMemory'])
                out = output.decode("utf-8").split('-')[-1].strip()
                cls.execute('Free physical RAM: %s' % out)
                if int(out) < 1048576:

                    return False
                elif int(out) >= 1048576:
                    return True
                else:
                    cls.execute('ERROR wrong RAM output: %s' % out)
                    return False
            except subprocess.CalledProcessError as error_message:
                cls.execute('ERROR while RAM calculation. System output: %s' % error_message)
                return False

    @classmethod
    def run(cls):

        if RandomFile.os_type == 'Linux':

            home = str(Path.home()) + '/'
            cls.execute('Home directory is: %s' % home)
            path_to_random_file = home + 'random_file'
            cls.execute('Path to the random content file is: %s' % path_to_random_file)
            cls.execute('Start writing to the file')
            try:
                with open(path_to_random_file, 'wb') as random_input_file:
                    random_input_file.write(urandom(1048576))
                cls.execute('The file was written successfully')
            except:
                cls.execute('ERROR The file was not written successfully')

        elif RandomFile.os_type == 'Windows':

            home = str(Path.home()) + '\\'
            cls.execute('Home directory is: %s' % home)
            path_to_random_file = home + 'random_file'
            cls.execute('Path to the random content file is: %s' % path_to_random_file)
            cls.execute('Start writing to the file')
            try:
                with open(path_to_random_file, 'wb') as random_input_file:
                    random_input_file.write(urandom(1048576))
                cls.execute('The file was written successfully')
            except:
                cls.execute('ERROR The file was not written successfully')


    @classmethod
    def clean_up(cls):

        if RandomFile.os_type == 'Linux':
            path_to_random_file = str(Path.home()) + '/' + 'random_file'
            try:
                delete_output = subprocess.check_output(['rm', path_to_random_file])
                cls.execute('The file deleted successfully. System Output: %s' % delete_output)
            except subprocess.CalledProcessError as error_message:

                cls.execute('The file was not deleted successfully. System Output: %s' % error_message)

        elif RandomFile.os_type == 'Windows':
            path_to_random_file = str(Path.home()) + '\\' + 'random_file'

            try:
                delete_output = subprocess.check_output([RandomFile.path_to_ps, 'Remove-Item ' + path_to_random_file])
                cls.execute('The file deleted successfully. System Output: %s' % delete_output)
            except subprocess.CalledProcessError as error_message:
                cls.execute('The file was not deleted successfully. System Output: %s' % error_message)

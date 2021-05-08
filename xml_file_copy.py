from platform import system as get_os_type  # module to check the platform
import xml.etree.ElementTree as xml_Parse          # module to parse XML
import subprocess                           # module to execute OS commands
import sys
from pathlib import Path                    # module to check a file existence


os_type = get_os_type()  # detecting of the OS

source_XML_file = sys.argv[1]          # Input path to an XML file i.e. '/home/user/Documents/qa_test_xml.xml'

try:
    xml_root = xml_Parse.parse(source_XML_file).getroot()  # Parsing an XML
    for child in xml_root:
        source_path = child.attrib['source_path']                            # Getting a source path from the XML

        destination_path = child.attrib['destination_path']                  # Getting a destination path from the XML

        file_name = child.attrib['file_name']                                # Getting a file name

        if os_type == 'Linux' and ':\\' not in source_path:

            if source_path.endswith('/'):                                    # The below 'if' statement will add '/' if
                pass                                                         # the path ends with something different
            else:                                                            # then '/'
                source_path = source_path.strip() + '/'
            if destination_path.endswith('/'):
                pass
            else:
                destination_path = destination_path.strip() + '/'             # Constructing a command for the Linux OS
            copy_command_Linux = 'cp ' + \
                                 source_path + \
                                 file_name + \
                                 ' ' + \
                                 destination_path + \
                                 file_name
            subprocess.check_output(copy_command_Linux, shell=True)  # Executing the command
            the_file = Path(destination_path + file_name)                        # Check if the file was transferred
            if the_file.is_file():
                print('The file was transferred successfully')
            else:
                print('The file was NOT transferred successfully, '
                      'please run the application again with root credentials')

        elif os_type == 'Windows' and ':\\' in source_path:  # if the string could be a windows

            path_to_ps = "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe"
            if source_path.endswith('\\'):                                   # The below 'if' statement will add '\' if
                pass                                                         # the path ends with something different.
            else:                                                            # then '\' will be added
                source_path = source_path.strip() + '\\'
            if destination_path.endswith('\\'):
                pass
            else:
                destination_path = destination_path.strip() + '\\'          # Constructing a command for the Windows OS
            copy_command_Windows = 'Copy-Item "' + \
                                   source_path + \
                                   file_name + \
                                   '" -Destination "' + \
                                   destination_path + '"'
            subprocess.call([path_to_ps, copy_command_Windows])              # Executing the command
            the_file = Path(destination_path + file_name)  # Check if the file was transferred
            if the_file.is_file():
                print('The file was transferred successfully')
            else:
                print('The file was NOT transferred successfully, '
                      'please run the application again with Admin credentials')

        elif os_type != 'Windows' and os_type != 'Linux':
            print('You are using the unknown OS, '
                  'please run the script as the Administrator on the Windows OS'
                  'or as the root account on the Linux')

except xml_Parse.ParseError:                                                        # If malformed XML - error message

    print('The XML is invalid please try another XML file')

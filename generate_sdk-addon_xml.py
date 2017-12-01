import xml.etree.cElementTree as ET
import os
import re
import hashlib

filename = "leia_sdk-addon_test.xml"
leia_license_ref = "leia-sdk-license"
supproted_apis = [23, 24, 25, 26, 27]
files = [ f for f in os.listdir(".") if os.path.isfile(f)]
libs = ["com.leia.android.lights"]


def get_max_reviesion(list_file_name):
    """analyse the addon zip file name,
    get the revision number
    """
    revision = 0
    file = ""
    sha1 = hashlib.sha1()
    for filename in list_file_name:
        if filename.startswith('leia_sdk-addon_') and "zip" in filename:
            r = re.findall(r'\d+', filename)
            n = int(r[0])
            if n > revision:
                revision = n
                file = filename
    if not file:
        return
    with open(file, 'rb') as f:
        while True:
            data = f.read(65536)
            if not data:
                break
            sha1.update(data)
    file_size  = os.path.getsize(file)

    return (revision, file, file_size, sha1.hexdigest())


def build_xml(save_as_filename, supproted_apis, revision, arch_file_name, arch_file_size, arch_sha1, list_libs):
    root = ET.Element("sdk:sdk-addon", {'xmlns:xsi': "http://www.w3.org/2001/XMLSchema-instance",
                                        'xmlns:sdk': "http://schemas.android.com/sdk/android/addon/{}".format(len(supproted_apis))
                                        })
    sdk_license = ET.SubElement(root, 'sdk:license', {'id': leia_license_ref, 'type': "text"})
    sdk_license.text = "LEia Inc SDK EULA"

    for api in supproted_apis:
        sdk_addon = ET.SubElement(root, "sdk:add-on")
        ET.SubElement(sdk_addon, "sdk:vendor-id").text = "leia"
        ET.SubElement(sdk_addon, "sdk:vendor-display").text = "Leia Inc."
        ET.SubElement(sdk_addon, "sdk:name-id").text = "leia-api-{}".format(api)
        ET.SubElement(sdk_addon, "sdk:name-display").text = "Leia APIs for Android {}".format(api)
        ET.SubElement(sdk_addon, "sdk:description").text = "Leia Services Add-on"
        ET.SubElement(sdk_addon, "sdk:api-level").text = "{}".format(api)
        ET.SubElement(sdk_addon, "sdk:revision").text = "{}".format(revision)
        ET.SubElement(sdk_addon, "sdk:uses-license", {'ref': leia_license_ref})
        sdk_libs = ET.SubElement(sdk_addon, "sdk:libs")
        for lib in list_libs:
            ET.SubElement(sdk_libs, "sdk:name").text = lib
        sdk_archives = ET.SubElement(sdk_addon, "sdk:archive")
        sdk_archive = ET.SubElement(sdk_archives, "sdk:archive", {'os': "any", 'arch': "any"})
        ET.SubElement(sdk_archive, "sdk:size").text = "{}".format(arch_file_size)
        ET.SubElement(sdk_archive, "sdk:checksum").text = "{}".format(arch_sha1)
        ET.SubElement(sdk_archive, "sdk:url").text = "{}".format(arch_file_name)

    tree = ET.ElementTree(root)
    tree.write(save_as_filename)



revision, fname, fsize, fsha1 = get_max_reviesion(files)
build_xml("leia_sdk-addon_test.xml", supproted_apis, revision, fname, fsize, fsha1, libs)


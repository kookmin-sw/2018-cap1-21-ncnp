import os,json,sys,shutil
from django.conf import settings

from tensorflow_model import testing_bc_static
from tensorflow_model import testing_mc_static
from pefile_viewer import peview

def run_static_testing(upload_file_obj):

    IDA_ROOT = os.path.join(settings.PROJECT_DIR,'ida')
    FEATURE_ROOT = os.path.join(settings.PROJECT_DIR,'make_feature')

    upload_file_path = os.path.join(settings.MEDIA_ROOT, upload_file_obj.upload_file.name)
    file_name = os.path.splitext(upload_file_obj.upload_file.name)[0]

    idb_folder_path = os.path.join(IDA_ROOT, 'idb')
    idb_file_path = os.path.join(idb_folder_path,file_name+'.i64')
    fops_folder_path = os.path.join(IDA_ROOT,'fops')
    fops_file_path = os.path.join(fops_folder_path,file_name+'.fops')
    cmd_run_ida_fops = 'python ' + IDA_ROOT + os.sep + 'make_idb_fops.py ' + upload_file_path
    os.system(cmd_run_ida_fops)

    fh_fops_folder_path = os.path.join(FEATURE_ROOT,'fh_fops')
    fh_fops_file_path = os.path.join(fh_fops_folder_path,file_name+'.fhfops')
    cmd_fh_fops = 'python ' + FEATURE_ROOT + os.sep + 'make_fh_fops.py ' + fops_file_path
    os.system(cmd_fh_fops)

    result_bc = testing_bc_static.run(fh_fops_file_path)
    result_mc = testing_mc_static.run(fh_fops_file_path)

    # remove temp file
    os.remove(fops_file_path)
    os.remove(idb_file_path)

    return result_bc, result_mc


def run_pefile_viewer(upload_file_obj):
    upload_file_path = os.path.join(settings.MEDIA_ROOT, upload_file_obj.upload_file.name)
    peviewer = peview.Peview(upload_file_path)
    total_report = dict()

    # hash_info
    hash_report = dict()
    hashes = peviewer.get_hash()
    hash_report['md5'] = hashes[0]
    hash_report['sha1'] = hashes[1]
    hash_report['sha256'] = hashes[2]
    hash_report['imp_hash'] = hashes[3]
    total_report['hash'] = hash_report

    # packer_info
    packer_report = list()
    packer_info = peviewer.get_packer_info()
    if not len(packer_info) == 0:
        for packer in packer_info:
            packer_report.append(packer)
        total_report['packer_info'] = packer_report

    # section_number
    section_num = peviewer.get_section_number()
    total_report['section_num'] = section_num

    # section_nfo
    section_report = list()
    section_info = peviewer.get_sections_info()
    if not len(section_info) == 0:
        for section in section_info:
            section_report.append(section)
        total_report['section_info'] = section_report

    # compile_time
    total_report['compile_time'] = peviewer.get_compile_time()

    # resource_info
    resource_report = list()
    resource_info = peviewer.get_resources_info()
    if not len(resource_info) == 0:
        for resource in resource_info:
            resource_report.append(resource)
        total_report['resource_info'] = resource_report

    # import_function
    import_func_report = list()
    import_func_info = peviewer.get_import_function()
    if not len(import_func_info) == 0:
        for import_func in import_func_info:
            import_func_report.append(import_func.decode('ascii'))
        total_report['import_function'] = import_func_report

    # mutex_info
    mutex_report = list()
    mutex_info = peviewer.get_mutex_info()
    if not len(mutex_info) == 0:
        for mutex in mutex_info:
            mutex_report.append(mutex)
        total_report['mutex_info'] = mutex_report

    # api_alert_info
    api_alert_report = list()
    api_alert_info = peviewer.get_api_alert_info()
    if not len(api_alert_info) == 0:
        for api_alert in api_alert_info:
            api_alert_report.append(api_alert)
        total_report['api_alert_info'] = api_alert_report

    # anti_debug
    anti_debug_report = list()
    anti_debug_info = peviewer.get_anti_debug()
    if not len(anti_debug_info) == 0:
        for anti_debug in anti_debug_info:
            anti_debug_report.append(anti_debug)
        total_report['anti_debug'] = anti_debug_report

    # anti_vm
    anti_vm_report = list()
    anti_vm_info = peviewer.get_anti_vm()
    if not len(anti_vm_info) == 0:
        for anti_vm in anti_vm_info:
            anti_vm_report.append(anti_vm)
        total_report['anti_vm'] = anti_vm_report

    return total_report
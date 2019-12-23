import re
import json
log = open("Task-00008020-000D08323E50003A.log","r")
json_file = open("Task-00008020-000D08323E50003A.json", "w")
task_array = []
regex = r'L:\s-\sexist[\s\S]*?(Device\sis\sAvailable).*'
matches = re.finditer(regex, log.read())
for match in matches:
  task_name = re.search(r'BLE\w{2}\d{3}', match.group())
  if task_name:
    task_result = re.search(r'TEST_SESSION_END[|](.*)[|]', match.group())
    task_time_virt = re.search(r'virtual.*:[\s\S]*total.*:\s?(\d{2}:\d{2}:\d{2}.\d{3})', match.group())
    task_time = re.search(r'real.*:[\s\S]*total.*:\s?(\d{2}:\d{2}:\d{2}.\d{3})', match.group())
    task_manifest = re.search(r'.*manifest\sfile\spath.*BLE.*(manifest.*.json)', match.group())
    task_os = re.search(r'os\s*:\s(.*)', match.group())
    task_os_ver = re.search(r'osVersion\s*:\s(.*)', match.group())
    task_location = re.search(r'location\s*:\s(.*)', match.group())
    task_device = re.search(r'deviceId\s*:\s(.*)', match.group())
    task_model = re.search(r'model\s*:\s(.*)', match.group())
    task_perf_rep = re.search(r'Perfecto\sreport:\s(.*)', match.group())
    task_dict = {}
    task_dict['TestName'] = task_name.group()
    task_dict['Result'] = task_result.group(1)
    task_dict['VirtualRunTime'] = task_time_virt.group(1)
    task_dict['RealRunTime'] = task_time.group(1)
    if task_result.group(1) == 'CRASHED':
      task_dict['Cause'] = []
      task_cause = re.finditer(r'.*[|]?\n*ERROR\n*[:]?[|]?.*', match.group())
      for cause_match in task_cause:
        task_dict['Cause'].append(cause_match.group())
    if task_perf_rep:
      task_dict['PerfectoReport'] = task_perf_rep.group(1)
    task_dict['Manifest'] = task_manifest.group(1)
    task_dict['OS'] = task_os.group(1)
    task_dict['OS_Version'] = task_os_ver.group(1)
    task_dict['Location'] = task_location.group(1)
    task_dict['DeviceID'] = task_device.group(1)
    task_dict['Model'] = task_model.group(1)
    task_array.append(task_dict)
json.dump(task_array, json_file, indent=4, sort_keys=False)
log.close()
json_file.close()
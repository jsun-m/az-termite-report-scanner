import json

with open('data.json', 'r') as f:
  data = f.readlines()

r = []
unique_report_types = set()
report_type_count = {}
for line in data:
  d = json.loads(line)
  if len(d) < 4:
    continue

  report_type = d[3]
  if report_type not in unique_report_types:
    unique_report_types.add(report_type)
    continue
  
  report_type_count[report_type] = report_type_count.get(report_type, 0) + 1
  if report_type == 'WIR':
    continue
  
  
  r.append(d)

print(report_type_count)
print(len(r), "/", report_type_count['PCT'] + report_type_count['WIR'])
with open('cleaned_data.json', 'w') as f:
  json.dump(r, f, indent=4)
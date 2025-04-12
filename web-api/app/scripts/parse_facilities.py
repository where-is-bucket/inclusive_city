import json

data = []

with open('./app/scripts/enriched_places_with_place_id.json', 'r', encoding='utf-8') as f:
     data = json.load(f)

unique_values = set()

for item in data:
    lun_descriptions = item.get("lun_description", [])

    if lun_descriptions is None:
        continue

    for description in lun_descriptions:

        values = description.get("values", [])

        if values is None: 
            continue

        for value in values:
            unique_values.add(value)
        

unique_values_list = sorted(unique_values)


with open('./app/scripts/parsed_lun_facilities.json', 'x', encoding='utf-8') as output:
    for value in unique_values_list:
        output.write(value)
        output.write('\n')
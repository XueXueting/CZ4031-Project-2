import re


def process_schemas(raw_schemas):
    processed_schemas = []
    for i in range(len(raw_schemas)):
        processed_schemas.append(raw_schemas[i][0])
    return processed_schemas


def process_qep(raw_qep):
    result_dict = {'Join': {}, 'Scan': BiDict({})}
    for i in range(len(raw_qep)):
        qep_item = raw_qep[i][0]
        print(qep_item)
        split_item = qep_item.split('->  ')
        if i == 0:
            item_details = split_item[0]
        elif split_item[0].isspace():
            item_details = split_item[1]
        else:
            continue

        if item_details.find('Join') != -1:
            # item is a 'Join' process'
            substring_index = item_details.find('Join')
            join_type = item_details[:substring_index + len('Join')]
            join_condition = raw_qep[i+1][0].split('Cond: ')[1]
            result_dict['Join'][join_condition] = join_type
        elif item_details.find('Scan') != -1:
            # item is a 'Scan' process
            item_details_list = re.split(' on |  \(', item_details)
            scan_type = item_details_list[0]
            scan_table = item_details_list[1]
            # substring_index = item_details.find('Scan')
            # scan_type = item_details[:substring_index + len('Scan')]
            result_dict['Scan'][scan_table] = scan_type
        else:
            continue
    return result_dict


# def create_graphical_qep(raw_qep):



class BiDict(dict):
    def __init__(self, *args, **kwargs):
        super(BiDict, self).__init__(*args, **kwargs)
        self.inverse = {}
        for key, value in self.items():
            self.inverse.setdefault(value,[]).append(key)

    def __setitem__(self, key, value):
        if key in self:
            self.inverse[self[key]].remove(key)
        super(BiDict, self).__setitem__(key, value)
        self.inverse.setdefault(value, []).append(key)

    def __delitem__(self, key):
        self.inverse.setdefault(self[key], []).remove(key)
        if self[key] in self.inverse and not self.inverse[self[key]]:
            del self.inverse[self[key]]
        super(BiDict, self).__delitem__(key)

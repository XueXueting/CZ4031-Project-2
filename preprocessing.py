import re
import graphviz
from anytree import Node, RenderTree
from anytree.exporter import UniqueDotExporter


def process_schemas(raw_schemas):
    processed_schemas = []
    for i in range(len(raw_schemas)):
        processed_schemas.append(raw_schemas[i][0])
    return processed_schemas


def process_qep(raw_qep):
    result_dict = {'Join': {}, 'Scan': BiDict({})}
    for i in range(len(raw_qep)):
        qep_item = raw_qep[i][0]
        split_item = qep_item.split('->  ')
        if i == 0:
            item_details = split_item[0]
        elif split_item[0].isspace():
            item_details = split_item[1]
        else:
            continue

        if item_details.find('Join') != -1:
            # item is some 'Join' process'
            substring_index = item_details.find('Join')
            join_type = item_details[:substring_index + len('Join')]
            join_condition = raw_qep[i + 1][0].split('Cond: ')[1]
            result_dict['Join'][join_condition] = join_type
        elif item_details.find('Nested Loop') != -1:
            # item is a 'Nested Loop Join' process
            # find condition of nested loop join in next line
            next_qep_item = raw_qep[i+1][0]
            if next_qep_item.find('Join Filter') != -1:
                join_condition = next_qep_item.split(': ')[1]
                result_dict['Join'][join_condition] = 'Nested Loop Join'
            else:
                continue
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


def create_graphical_qep(raw_qep):
    intermediate_qep = []
    num_items = len(raw_qep)
    for i in range(num_items):
        item = raw_qep[i][0]
        if i == 0 or ('->' in item):
            intermediate_qep.append(item.split('->  '))

    num_query_components = len(intermediate_qep)
    cur_index = 0
    root_node = None
    previous_node = None
    current_component_name = ""
    next_component_name = ""
    previous_indent_length = 0
    while cur_index < num_query_components:
        if cur_index == 0:
            root_name = intermediate_qep[cur_index][0].split('  (')[0]
            root_node = Node(root_name, indent=0)
            previous_node = root_node
            cur_index += 1
            continue
        elif cur_index == num_query_components-1:
            current_indent_length = len(intermediate_qep[cur_index][0])
            current_component_name = intermediate_qep[cur_index][1].split('  (')[0]
            if current_indent_length < previous_indent_length:
                # current component is a sibling of an ancestor of previous node
                # search for sibling node
                temp = root_node
                while len(temp.children) > 0:
                    if temp.children[0].indent == current_indent_length:
                        sibling_node = Node(current_component_name, parent=temp, indent=current_indent_length)
                        break
                    else:
                        temp = temp.children[0]
                        continue
                break
            else:
                new_node = Node(current_component_name, parent=previous_node, indent=current_indent_length)
                break

        else:
            current_indent_length = len(intermediate_qep[cur_index][0])
            next_indent_length = len(intermediate_qep[cur_index + 1][0])
            current_component_name = intermediate_qep[cur_index][1].split('  (')[0]

            if current_indent_length < previous_indent_length:
                # current component is a sibling of an ancestor of previous node
                # search for sibling node
                temp = root_node
                while len(temp.children) > 0:
                    if temp.children[0].indent == current_indent_length:
                        sibling_node = Node(current_component_name, parent=temp, indent=current_indent_length)
                        break
                    else:
                        temp = temp.children[0]
                        continue
                previous_node = sibling_node
                previous_indent_length = current_indent_length
                cur_index += 1
                continue

            if next_indent_length == current_indent_length:
                # next component is the left sibling of current
                next_component_name = intermediate_qep[cur_index + 1][1].split('  (')[0]
                left_node = Node(next_component_name, parent=previous_node, indent=next_indent_length)
                right_node = Node(current_component_name, parent=previous_node, indent=current_indent_length)
                previous_node = left_node
                previous_indent_length = current_indent_length
                cur_index += 2
                continue
            else:
                # next component is a child of current
                new_node = Node(current_component_name, parent=previous_node, indent=current_indent_length)
                previous_node = new_node
                previous_indent_length = current_indent_length
                cur_index += 1
                continue
    try:
        UniqueDotExporter(root_node,
                          edgeattrfunc=lambda node, child: "dir=none").to_picture('graphical_qep.png')
    except Exception as e:
        print('Tree too large to be converted into png!')


class BiDict(dict):
    def __init__(self, *args, **kwargs):
        super(BiDict, self).__init__(*args, **kwargs)
        self.inverse = {}
        for key, value in self.items():
            self.inverse.setdefault(value, []).append(key)

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

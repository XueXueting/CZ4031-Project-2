import string
from string import punctuation


class Annotation:
    def __init__(self, operation, algorithm, target_clause, term_index):
        self.operation = operation
        self.algorithm = algorithm
        self.target_clauses = [target_clause]
        self.term_index = term_index

    def add_target(self, target_clause):
        self.target_clauses.append(target_clause)

    def construct_annotation_string(self):
        if self.operation == 'Join':
            # Join operation displays condition of the join
            target_line = 'Condition: ' + self.target_clauses[0]
        else:
            # Scan operation displays relevant tables using the same algorithm
            target_line = 'Tables: ' + self.target_clauses[0]
            for i in range(1, len(self.target_clauses)):
                target_line += (', ' + self.target_clauses[i])
        annotation_string = "Type of operation: " + self.operation + \
                            "\nImplementation: " + self.algorithm + \
                            "\n" + target_line
        return annotation_string


def generate_annotations(sql_query, processed_qep):
    annotations = []
    sql_comparison_operator_list = ['=', '!=', '<>', '>', '<', '>=', '<=']
    operator_replace_dict = {'=': ' = ',
                             '!=': ' <> ',
                             '<>': ' <> ',
                             '>': ' > ',
                             '<': ' < ',
                             '>=': ' >= ',
                             '<=': ' <= '}
    query_terms_list = sql_query.split()
    # remove commas from each term
    query_terms_list = [term.replace(',', '') for term in query_terms_list]
    scan_flag = 0
    join_flag = 0
    for term_index in range(len(query_terms_list)):
        term = query_terms_list[term_index]
        if 'from' == term.lower() or 'join' == term.lower():
            scan_flag = 1
            join_flag = 0
        elif 'where' == term.lower() or 'on' == term.lower():
            scan_flag = 0
            join_flag = 1
        elif 'group' == term.lower() or 'order' == term.lower():
            scan_flag = 0
            join_flag = 0
        if scan_flag:
            # match term with respective table in processed_qep
            scan_algorithm = [val for key, val in processed_qep['Scan'].items() if term.strip(punctuation).lower() in key and len(term) > 1]
            scan_keys = [key for key, val in processed_qep['Scan'].items() if term.strip(punctuation).lower() in key and len(term) > 1]
            if len(scan_algorithm) == 0:
                continue
            else:
                scan_algorithm = scan_algorithm[0]
            new_annotation = Annotation('Scan', scan_algorithm, scan_keys[0], term_index)
            for other_table in processed_qep['Scan'].inverse.get(scan_algorithm):
                if other_table != scan_keys[0]:
                    new_annotation.add_target(other_table)
                    scan_keys.append(other_table)
            for key in set(scan_keys):
                del processed_qep['Scan'][key]
            if processed_qep['Scan'].inverse.get(scan_algorithm) is not None:
                for other_table in processed_qep['Scan'].inverse.get(scan_algorithm):
                    del processed_qep['Scan'][other_table]
            annotations.append(new_annotation)
        elif join_flag:
            # match term with respective join condition in processed_qep
            # check valid join condition across two tables
            count_accessors = term.count('.')
            if any(operator in term for operator in sql_comparison_operator_list) and count_accessors == 0:
                # standalone comparison operator as a term, concatenate with previous and next term
                term = query_terms_list[term_index-1] + term + query_terms_list[term_index+1]
                count_accessors = term.count('.')
            if any(operator in term for operator in sql_comparison_operator_list) and count_accessors >= 2:
                term = replace_all(term, operator_replace_dict)
                join_algorithm = [val for key, val in processed_qep['Join'].items() if term.lower() in key]
                if len(join_algorithm) == 0:
                    # check if accessors are from different tables
                    split_term = term.split('.')
                    if split_term[0][-1] != split_term[1][-1]:
                        join_algorithm.append('Nested Loop Join')
                    else:
                        # same table accessor, continue next iteration
                        continue
                new_annotation = Annotation('Join', join_algorithm[0], term, term_index)
                annotations.append(new_annotation)
            else:
                continue
    return annotations


def replace_all(text, dic):
    for i, j in dic.items():
        text = text.replace(i, j)
    return text






import re
import sys

BLOCK_START = "BLOCK_START"
BLOCK_END = "BLOCK_END"
BLOCK_ELSE = "BLOCK_ELSE"
VARIABLE = "VARIABLE"
LIST_ITEM = "LIST_ITEM"
DICT_ITEM = 'DICT_ITEM'
TEXT = "TEXT"


class ResultingHTML(object):
    """This class holds the resulting HTML output in the form of a string"""

    def __init__(self, value=""):
        self.value = value

    def update_output(self, html_text):
        html_text = str(html_text)
        self.value = self.value + html_text
        self.value = self.value.replace('\n', '')
        self.value = self.value.replace('\t', '')


# область видимости
class Scope(object):
    """Stores user defined variables and their values.
    For loops get their own scope, that way rendering template_text
    doesn't modify the original dictionary of variables passed in """

    def __init__(self, parent, dictionary):
        self.parent = parent
        self.dictionary = dictionary

    def add(self, input):
        self.dictionary.update(input)

    def fetch(self, input_key):
        try:
            value = self.dictionary[input_key]
        except:
            value = self.parent.fetch(input_key)
        return value


# сравнивание с стандартными типами токенов
def determine_type(token):
    """Determines Type of Node.  Can be either TEXT, VARIABLE,
    BLOCK_START, BLOCK_END or BLOCK ELSE """
    if re.match("{{(\w+)\[(\d+)\]}}", token):
        return LIST_ITEM
    elif re.match("{{(\w+)\[(\w+)\]}}", token):
        return DICT_ITEM
    elif re.match("{{.*?}}", token):
        return VARIABLE
    elif re.match("{%.*?%}", token):
        if re.match("{%\s*?end\s*%}", token):
            return BLOCK_END
        elif re.match("{%\s*?else\s*%}", token):
            return BLOCK_ELSE
        else:
            return BLOCK_START
    else:
        return TEXT


# разбиение html шаблона на список по блокам
def tokenize(template_text):
    """Takes the raw template, and breaks it into tokens in the form of tuples."""

    TOKENIZED = re.compile(r"({{.*?}}|{%.*?%})")
    template_list = TOKENIZED.split(template_text)
    template_with_type = []
    for tok in template_list:
        token_type = determine_type(tok)
        if token_type == VARIABLE or token_type == BLOCK_END or token_type == BLOCK_START:
            token_value = tok[2:-2]
        else:
            token_value = tok
        token_data = (token_type, token_value)
        template_with_type.append(token_data)
    return template_with_type


# выдает дерево канторовича ast дерево
def get_ast(input_t):
    """Wrapper function, which grabs only the AST output
    from the final return of parse()"""

    return parse(input_t)[0]


# парсит даннве из токенозированного списка в ast дерево(дерево канторовича) и получает ast дерево
def parse(input_token_list):
    """Creates an AST out of the tokenized template"""

    output_token_list = []  # выходной список ast дерево(дерево канторовича)
    while True:
        item, input_token_list = input_token_list[0], input_token_list[1:]

        if (item[0] != BLOCK_START and item[0] != BLOCK_END and item[0] != BLOCK_ELSE):
            output_token_list.append(item)
            if len(input_token_list) == 0:
                break

        if item[0] == BLOCK_START:
            if re.match("\s*?if", item[1]):
                sub_output, input_token_list = parse(input_token_list)
                res = sub_output[:-1]
                alt = sub_output[-1]
                new_to_append = [res, alt]
                new_to_append.insert(0, item)
                output_token_list.append(new_to_append)
            else:
                sub_output, input_token_list = parse(input_token_list)
                sub_output.insert(0, item)
                output_token_list.append(sub_output)
            if len(input_token_list) == 0:
                break

        if item[0] == BLOCK_ELSE:
            sub_output, input_token_list = parse(input_token_list)
            output_token_list.append(sub_output)
            return output_token_list, input_token_list

        if item[0] == BLOCK_END:
            return output_token_list, input_token_list

    return output_token_list, input_token_list


def process_template(parsed_template, context):
    """This is the outter function which evaluates the inputed AST and returns
    the resulting HTML page."""

    my_HTML = ResultingHTML()
    eval_main(parsed_template, context, my_HTML)
    return my_HTML.value


def eval_main(parsed_template, context, my_HTML):
    for item in parsed_template:
        if type(item) is list:
            evaluate_logic(item, context, my_HTML)
        elif type(item) is tuple:
            evaluate_node(item, context, my_HTML)


def evaluate_node(node, context, my_HTML):
    if node[0] == TEXT:
        return my_HTML.update_output(node[1])
    if node[0] == VARIABLE:
        var_value = context.fetch(node[1])
        my_HTML.update_output(var_value)
        return None
    if node[0] == LIST_ITEM:
        open_bracket_index = node[1].index("[")
        close_bracket_index = node[1].index("]")
        element_index = int(node[1][open_bracket_index+1:close_bracket_index])
        var_list = context.fetch(node[1][2:open_bracket_index])
        list_var_value = var_list[element_index]
        my_HTML.update_output(list_var_value)
        return None
    if node[0] == DICT_ITEM:
        item = node[1][2:-2]
        open_bracket_index = item.index("[")
        close_bracket_index = item.index("]")
        key = item[open_bracket_index+1:close_bracket_index]
        var_dict = context.fetch(item[:open_bracket_index])
        value = var_dict[key]
        my_HTML.update_output(value)
        return None

def evaluate_logic(list_input, context, my_HTML):
    if bool((re.search("for\s.*?\sin", list_input[0][1]))):
        do_for_loop(list_input, context, my_HTML)
    if bool((re.match(".?if", list_input[0][1]))):
        do_conditional(list_input, context, my_HTML)


def do_for_loop(list_input, context, my_HTML):
    head, rest = list_input[0], list_input[1:]
    item_var, list_var = re.search("for\s(.*)\sin\s(\S+)", head[1]).groups()
    for item_value in context.fetch(list_var):
        inner_context = Scope(context, {'%s' % item_var: item_value})
        eval_main(rest, inner_context, my_HTML)


def evaluate_condition(condition, context):
    match = re.match("\s*(if|while)\s(.*)", condition, re.DOTALL)
    statement = match.group(2)
    cond_match = re.match("\w+", statement)
    cond = cond_match.group(0)
    a = context.fetch(cond)
    local = {cond: a}
    # exec("%s = %d" %(cond,a))
    return eval(statement, local)


def do_conditional(list_input, context, my_HTML):
    head, consequence, alternate = list_input[0], list_input[1], list_input[2]
    condition = head[1]
    condition_value = evaluate_condition(condition, context)
    if condition_value:
        return eval_main(consequence, context, my_HTML)
    else:
        return eval_main(alternate, context, my_HTML)


# функция рендерит контекст в html
def render(file, dictionary):
    """The black box function that a another programer could use.
    Takes in file name and dictionary"""
    outter_context = Scope(None, dictionary)
    with open(file, "r") as f:
        template = f.read()
    return process_template(get_ast(tokenize(template)), outter_context)

#print(determine_type('{{item["id"]}}'))

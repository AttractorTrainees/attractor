import operator
import os
import re
from settings import TEMPLATES_DIR, STATIC_URL, HOSTDOMAIN, database
from ast import literal_eval


class TemplateEngineError(Exception):
    def __init__(self, value):
        self.__value = value

    def __str__(self):
        return self.__value


VARIABLE = 'VAR'
TEXT = 'TEXT'

OPEN = 'OPEN'
CLOSE = 'CLOSE'
STATIC = 'STATIC'
EXTEND = 'EXTEND'
ROOT = 'ROOT'
BLOCK = 'BLOCK'
ENDBLOCK = 'ENDBLOCK'

VAR_TOKEN_START = '{{'
VAR_TOKEN_END = '}}'
BLOCK_TOKEN_START = '{%'
BLOCK_TOKEN_END = '%}'

WHITESPACE = re.compile('\s+')
TOKEN_REXEP = re.compile(r"(%s.*?%s|%s.*?%s)" % (
    VAR_TOKEN_START,
    VAR_TOKEN_END,
    BLOCK_TOKEN_START,
    BLOCK_TOKEN_END
))


# vir class--start#

class LexTokenize(object):
    """Класс предназначен для разбиения шаблона на токенизированный список по лексемам"""

    def __init__(self, template=None):
        self.__frag_list = None
        if template != None:
            self.parse_html(template)

    # сравнивает фрагмент с правилом токена

    def determine_type(self, fragment):
        if re.match("{{.*?}}", fragment):
            return VARIABLE
        elif re.match("{%.*?%}", fragment):
            if re.match("{%\s*?(endfor|endif)\s*%}", fragment):
                return CLOSE
            elif re.match("{%\s*?static\s*\'(.*\/.*|.*)\'\s*%}", fragment):
                return STATIC
            elif re.match(r"{%\s*block\s+(\w+)\s*%}", fragment):
                return BLOCK
            elif re.match(r"{%\s*?(endblock)\s*%}", fragment):
                return ENDBLOCK
            elif re.match("{%\s*?extend\s*\'(.*\/.*|.*)\'\s*%}", fragment):
                return EXTEND
            else:
                return OPEN
        else:
            return TEXT

    # удаляет лишние символы в шаблоне
    def trim_html(self, html):
        html = re.sub('[\r\n]', '', html)
        html = re.sub('[\ \t]{2,}', ' ', html)
        html = re.sub('<!--.*?-->', '', html)
        html = re.sub('\{\%[\s]{1,}', '{%', html)
        html = re.sub('[\s]{1,}\%\}', '%}', html)
        return html

    # удаляет лишние элементы во фрагментированном списке
    def trim_frag_list(self, frag_list):
        trim_list = []
        for fragment in frag_list:
            fragment = fragment.strip()
            if fragment != '':
                trim_list.append(fragment)
        return trim_list

    # создает список фрагментов
    def fragmentation(self, template):
        template = self.trim_html(template)
        fragment_list = TOKEN_REXEP.split(template)
        if fragment_list:
            fragment_list = self.trim_frag_list(fragment_list)
        return fragment_list

    # токенизирует фрагментированный список
    def tokenization(self, fragment_list):
        token_fragment_list = []
        for fragment in fragment_list:
            token_type = self.determine_type(fragment)
            if token_type == TEXT:
                token_value = fragment
            else:
                token_value = fragment[2:-2]
            token_data = (token_type, token_value)
            token_fragment_list.append(token_data)
        return token_fragment_list

    def parse_html(self, template):
        frag_list = self.fragmentation(template)
        token_frag_list = self.tokenization(frag_list)
        self.__frag_list = token_frag_list

    def get_frag_list(self):
        return self.__frag_list


class TemplateEngine(object):
    @classmethod
    def read_tempate_file(self, filename):
        template = None
        with open(os.path.join(TEMPLATES_DIR, filename), "r", encoding="utf-8") as file:
            template = file.read()
        return template

    @classmethod
    def find_extend(self, token_list):
        parent_html = None
        for index, frag in enumerate(token_list):
            if frag[0] == EXTEND:
                parent_html = re.match("extend\s*\'(.*\/.*|.*)\'", frag[1]).groups()[0]
                token_list = token_list[index + 1:]
            if re.match(r"block\s+(?P<name>\w+)", frag[1]) and parent_html:
                token_list = token_list[index - 1:]
                break

        return parent_html, token_list

    @classmethod
    def load_blocks(self, parents, children):
        i = 0
        for index, (parent_type, parent_content) in enumerate(parents):
            if parent_type == BLOCK:
                for cindex, (child_type, child_content) in enumerate(children):
                    if child_type == BLOCK:
                        if child_content == parent_content:
                            for i, (t, c) in enumerate(children[cindex:]):
                                if t == ENDBLOCK:
                                    parents[index:index + 1] = children[cindex:cindex + i]
                                    break

        return parents

    @classmethod
    def render_template(self, filename, context):
        template = self.read_tempate_file(filename)
        frag_list = LexTokenize(template).get_frag_list()
        parent_html, frag_list = self.find_extend(frag_list)

        if parent_html:
            parent_template = self.read_tempate_file(parent_html)
            parent_list = LexTokenize(parent_template).get_frag_list()
            parent_list = self.load_blocks(parent_list, frag_list)
            frag_list = parent_list
        root=ASTree(frag_list).get_root()
        html =root.render(context)
        return html


class ASTree(object):
    def __init__(self, tokenlist):
        self.tokenlist = tokenlist
        self.tree_root = None
        self.blocks = {}
        if tokenlist:
            self.tree_root = self.createAST()

    # для создания узла дерева
    def createNode(self, fragment):
        fragtype = fragment[0]
        content = fragment[1]
        node = None
        if fragtype == VARIABLE:
            node = Variable(content, fragtype)
        elif fragtype == OPEN:
            if re.match(r"for\s+?(.+)\s+in\s+?(.+)", content):
                node = For(content, fragtype)
            elif re.match(r"if\s+(.+)", content):
                node = If(content, fragtype)
            elif re.match(r"else", content):
                node = Else(content, fragtype)
        elif fragtype == BLOCK:
            node = Block(content, OPEN)
        elif fragtype == ENDBLOCK:
            node = End(content, CLOSE)
        elif fragtype == CLOSE:
            node = End(content, fragtype)
        elif fragtype == STATIC:
            node = Static(content, fragtype)
        else:
            node = Text(content, fragtype)
        return node

    def get_root(self):
        return self.tree_root

    def createAST(self):
        if len(self.tokenlist) == 0:
            return None
        stack = []
        tokens = self.tokenlist.copy()
        root = Node(token=ROOT, content=ROOT)
        current = root
        for frag in tokens:
            node = self.createNode(frag)
            ab = current

            if current.get_token() == OPEN or current.get_token() == CLOSE:
                if current.get_token() == OPEN:
                    if current.get_scope_type() != 'else':
                        stack.append(current)
                    else:
                        current.set_nextinscope(End('endif'))
                    current.set_child(node)
                    current = current.child
                elif current.get_token() == CLOSE:
                    if len(stack) == 0:
                        raise TemplateEngineError('Engine error:нет элемента закрытия блока')
                    current = stack.pop()
                    current.set_nextinscope(node)
                    current = current.nextinscope
            else:
                current.nextinscope = node
                current = node
        return root


class Node(object):
    def __init__(self, content=None, token=None):
        self.token = token
        self.content = content
        self.nextinscope = None

    def render(self, context):
        html = ''
        if self.nextinscope:
            html += self.nextinscope.render(context)
        return html

    def set_nextinscope(self, node):
        self.nextinscope = node

    def get_token(self):
        return self.token

    def get_scope_type(self):  # обязательно должен присутствовать
        pass


class ScopeNode(Node):
    def __init__(self, content=None, token=None):
        super().__init__(content, token)
        self.child = None

    def set_child(self, node):
        self.child = node

    def get_scope_type(self):
        name = re.match(r'^(?P<type>\w+)\s*\w*', self.content).group('type')
        return name


class Block(ScopeNode):
    def get_block_name(self):
        name = re.match(r"block\s+(?P<name>\w+)", self.content).group('name')
        return name

    def render(self, context):
        html = ""
        if self.child:
            html += self.child.render(context)
        if self.nextinscope:
            html += self.nextinscope.render(context)
        return html


class For(ScopeNode):
    def render(self, context):
        html = self.compilation(context)
        if self.nextinscope:
            html += self.nextinscope.render(context)
        return html

    def evaluate(self, context, node_item):
        values = node_item.split('.')
        item = None
        if len(values) == 1:
            item = context.get(node_item)
        elif len(values) > 1:
            item = context.get(values[0])
            for val in values[1:]:
                item = getattr(item, val)
        return item

    def compilation(self, context):
        item, forlist = re.match("for\s(.*)\sin\s(\S+)", self.content).groups()
        forlisteval = self.evaluate(context, forlist)
        html = ""
        for value in forlisteval:
            context[item] = value
            if self.child:
                html += self.child.render(context)
        context.pop(item)
        return html


class If(ScopeNode):
    def evaluate(self, context, node_item):
        item = None
        try:
            rob = literal_eval(node_item)
            item = rob
        except (KeyError, ValueError):
            values = node_item.split('.')
            if len(values) == 1:
                item = context.get(node_item)
            elif len(values) > 1:
                item = context.get(values[0])
                for val in values[1:]:
                    item = getattr(item, val)
        return item

    def render(self, context):
        html = ''
        result = self.compilation(context)
        if result:
            if self.child:
                html += self.child.render(context)
        else:
            current = self.child
            while True:
                if current == None or type(current) == Else:
                    break
                current = current.nextinscope
            if current != None:
                html += current.render(context, True)
            else:
                html += ''
        if self.nextinscope:
            html += self.nextinscope.render(context)
        return html

    def compilation(self, context):
        group = re.match(r'if\s+(.+\S?)\s+(>=|!=|<=|==|>|<|in|not in|)\s+(.+\S?)$', self.content).groups()
        left_operand = self.evaluate(context, group[0])
        right_operand = self.evaluate(context, group[2])
        eval_str = re.match(r'if\s+(.+)$', self.content).groups()[0]
        eval_dict = {group[0]: left_operand, group[2]: right_operand}
        result = eval(eval_str, eval_dict)
        return result


class Else(ScopeNode):
    def render(self, context, val=False):
        html = ''
        if val:
            html += self.child.render(context)
        if self.nextinscope:
            html += self.nextinscope.render(context)
        return html


class Text(Node):
    def render(self, context):
        html = self.content
        if self.nextinscope:
            html += self.nextinscope.render(context)
        return html

    def compilation(self, context):
        return self.content


class Variable(Node):
    def evaluate(self, context, node_item):
        values = node_item.split('.')
        item = None
        if len(values) == 1:
            item = context.get(node_item)
        elif len(values) > 1:
            item = context.get(values[0])
            for val in values[1:]:
                item = getattr(item, val)
        return item

    def compilation(self, context):
        value = self.evaluate(context, self.content)
        if value == None:
            return None
        else:
            if type(value) != str:
                value = str(value)
            return value

    def render(self, context):
        html = self.compilation(context)
        if self.nextinscope:
            html += self.nextinscope.render(context)
        return html


class Static(Node):
    def get_path(self):
        path = re.match(r"static\s*'(?P<path>.*\/.*|.*)'", self.content).group('path')
        return path

    def compilation(self, context):
        url = '%s/%s/%s' % (HOSTDOMAIN, STATIC_URL, self.get_path())
        return url

    def render(self, context):
        html = self.compilation(context)
        if self.nextinscope:
            html += self.nextinscope.render(context)
        return html


class End(Node):
    def get_close_type(self):
        type = re.match(r"end(?P<type>\w+)", self.content).group('type')
        return type

    def render(self, context):
        return ''
if __name__=='__main__':
    print(TemplateEngine.render_template('test1.html',{}))
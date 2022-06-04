#!/usr/bin/python3
# @author : guchim
# © 2020
# updated july 8 2021
# updated june 4 2022
import copy
import re
from sys import argv
from more_itertools import peekable


tokenType = dict(
    open_brace="{",
    close_brace="}",
    open_parenthesis="\\(",
    close_parenthesis="\\)",
    semi_colon=";",
    int_keyword="int",
    return_="return",
    integer_literal="\\d+",
    negation="-",
    bitwise_complement="~",
    addition="\\+",
    multiplication="\\*",
    division="/",
    logical_and='&&',
    logical_or='\\|\\|',
    equal='==',
    not_equal='!=',
    less_than_equal='<=',
    less_than='<',
    greater_than_or_equal='>=',
    greater_then='>',
    logical_negation="!",
    assignment='=',
    if_='if',
    else_='else',
    colon=":",
    question_mark="\\?",
    for_keyword="for",
    while_keyword="while",
    do_keyword="do",
    break_keyword="break",
    continue_keyword="continue",
    identifier="[a-zA-Z]\\w*",
    mod="%",
    comma=",",
)
clause_label_number = 0
clause_end_number = 0
clause_false_branch_label = 0
clause_post_conditional_number = 0
clause_while_start_number = 0
clause_while_end_number = 0
clause_for_start_number = 0
clause_for_end_number = 0
clause_for_post_expression_number = 0


class Token:
    def __init__(self, value, token_type):
        self.value = value
        self.token_type = token_type


re_pattern = ''
for item in tokenType.items():
    re_pattern += f'{item[1]}|'
re_pattern = re_pattern[:-1]

# text = """
# int main() {
#     return 1 + 2;
# }
# """


def create_tokens(script):
    string_tokens = re.findall(re_pattern, script)

    def map_token_to_type(token):
        for item in tokenType.items():
            if re.match(item[1], token):
                return Token(token, item[1])

    tokens = []
    for token in string_tokens:
        tokens.append(map_token_to_type(token))

    return tokens


# for t in create_tokens(text):
#     print(t.value, t.token_type)

class Node:
    def __init__(self):
        self.left = None
        self.right = None


class ProgramNode:
    def __init__(self):
        self.top_level_items = []


class FunctionNode:
    def __init__(self, name):
        self.name = name
        self.variables = []
        self.stack_size = []
        self.statements = []


class ConstantNode:
    def __init__(self, value):
        self.value = value


class UnaryOperatorNode:
    def __init__(self, name):
        self.left = None
        self.name = name


class BinaryOperatorNode:
    def __init__(self, name):
        self.right = None
        self.left = None
        self.name = name


class ReturnNode:
    def __init__(self, name):
        self.left = None
        self.name = name


class DeclarationNode:
    def __init__(self, name):
        self.name = name


class VariableNode:
    def __init__(self, name):
        self.name = name


class AssignNode:
    def __init__(self, name):
        self.left = None
        self.right = None
        self.name = name


class IfNode:
    def __init__(self):
        self.true_branch = None
        self.false_branch = None
        self.condition = None


class ConditionalNode:
    def __init__(self):
        self.true_branch = None
        self.false_branch = None
        self.condition = None


class CompoundNode:
    def __init__(self):
        self.statements = []


class NullNode:
    pass


class ForNode:
    def __init__(self):
        self.initial_expression = None
        self.condition = None
        self.post_expression = None
        self.body = None


class ForDeclarationNode:
    def __init__(self):
        self.initial_expression = None
        self.condition = None
        self.post_expression = None
        self.body = None


class WhileNode:
    def __init__(self):
        self.condition = None
        self.body = None


class DoWhileNode:
    def __init__(self):
        self.body = None
        self.condition = None


class BreakNode:
    pass


class ContinueNode:
    pass


class FunctionCallNode:
    def __init__(self):
        self.name = None
        self.args = []


def parse_program(tokens):
    tree = ProgramNode()
    top_level_item = parse_top_level_item(tokens)
    tree.top_level_items.append(top_level_item)

    try:
        next_token = tokens.peek()
    except:
        return tree

    while next_token.token_type == tokenType['int_keyword']:
        top_level_item = parse_top_level_item(tokens)
        tree.top_level_items.append(top_level_item)
        try:
            next_token = tokens.peek()
        except:
            return tree

    return tree


def parse_top_level_item(tokens):
    intKeywordToken = next(tokens)
    if intKeywordToken.token_type != tokenType['int_keyword']:
        raise 'int keyword expected'

    idToken = next(tokens)
    if idToken.token_type != tokenType['identifier']:
        raise 'id expected'

    nextToken = tokens.peek()

    if nextToken.token_type == tokenType['open_parenthesis']:
        tokens.prepend(idToken)
        tokens.prepend(intKeywordToken)
        node = parse_function(tokens)
    else:
        tokens.prepend(idToken)
        tokens.prepend(intKeywordToken)
        node = parse_declaration(tokens)

    return node


def parse_function(tokens):
    type_keyword = next(tokens)

    if type_keyword.token_type != tokenType['int_keyword']:
        raise "type expected"

    function_identifier = next(tokens)
    if function_identifier.token_type != tokenType['identifier']:
        raise "identifier expected"

    node = FunctionNode(function_identifier.value)

    open_parenthesis = next(tokens)
    if open_parenthesis.token_type != tokenType['open_parenthesis']:
        raise "( expected"

    next_token = tokens.peek()

    if next_token.token_type != tokenType['close_parenthesis']:
        token = next(tokens)
        if token.token_type != tokenType['int_keyword']:
            raise "int keyword expected"
        token = next(tokens)
        node.variables.append(token.value)
        next_token = tokens.peek()

        while next_token.token_type != tokenType['close_parenthesis']:
            token = next(tokens)
            if token.token_type != tokenType['comma']:
                raise ",  expected"
            token = next(tokens)
            if token.token_type != tokenType['int_keyword']:
                raise "int keyword expected"
            token = next(tokens)
            node.variables.append(token.value)
            next_token = tokens.peek()

    close_parenthesis = next(tokens)
    if close_parenthesis.token_type != tokenType['close_parenthesis']:
        raise ") expected"

    next_token = next(tokens)

    if next_token.token_type == tokenType['semi_colon']:
        return NullNode()

    if next_token.token_type != tokenType['open_brace']:
        raise "{ expected"

    next_token = tokens.peek()
    node.statements = []

    while next_token.token_type != tokenType['close_brace']:
        node.statements.append(parse_block_item(tokens))
        next_token = tokens.peek()

    close_brace_token = next(tokens)
    if close_brace_token.token_type != tokenType['close_brace']:
        raise "} expected"

    return node


def parse_function_call(tokens):
    token = next(tokens)
    if token.token_type != tokenType['identifier']:
        raise 'Identifier expected'
    node = FunctionCallNode()
    node.name = token.value

    open_parenthesis = next(tokens)
    if open_parenthesis.token_type != tokenType['open_parenthesis']:
        raise "( expected"

    next_token = tokens.peek()

    if next_token.token_type != tokenType['close_parenthesis']:
        param = parse_expression(tokens)
        node.args.append(param)

        next_token = tokens.peek()
        while next_token.token_type != tokenType['close_parenthesis']:
            token = next(tokens)
            if token.token_type != tokenType['comma']:
                raise ",  expected"
            param = parse_expression(tokens)
            node.args.append(param)
            next_token = tokens.peek()

    close_parenthesis = next(tokens)
    if close_parenthesis.token_type != tokenType['close_parenthesis']:
        raise ") expected"

    return node


def parse_statement(tokens):
    next_token = tokens.peek()
    if next_token.token_type == tokenType['return_']:
        token = next(tokens)
        node = ReturnNode(token.value)

        node.left = parse_option_expression(tokens)

        token = next(tokens)
        if token.token_type != tokenType['semi_colon']:
            raise "; expected after returnKeyword"
        return node

    elif next_token.token_type == tokenType['if_']:
        node = IfNode()
        next(tokens)
        token = next(tokens)
        if token.token_type != tokenType['open_parenthesis']:
            raise '( expected'

        node.condition = parse_expression(tokens)

        token = next(tokens)
        if token.token_type != tokenType['close_parenthesis']:
            raise ') expected'

        true_branch = parse_statement(tokens)

        node.true_branch = true_branch

        next_token = tokens.peek()
        if next_token.token_type == tokenType['else_']:
            next(tokens)
            node.false_branch = parse_statement(tokens)
        return node

    elif next_token.token_type == tokenType['open_brace']:
        node = parse_compound_block(tokens)
        return node

    elif next_token.token_type == tokenType['for_keyword']:
        for_token = next(tokens)
        parenthesis_token = next(tokens)
        next_token = tokens.peek()
        if next_token.token_type == tokenType['int_keyword']:
            tokens.prepend(parenthesis_token)
            tokens.prepend(for_token)
            node = parse_for_declaration(tokens)
            return node
        tokens.prepend(parenthesis_token)
        tokens.prepend(for_token)
        next_token = tokens.peek()

    if next_token.token_type == tokenType['for_keyword']:
        node = parse_for(tokens)

    elif next_token.token_type == tokenType['while_keyword']:
        node = parse_while(tokens)

    elif next_token.token_type == tokenType['do_keyword']:
        node = parse_do_while(tokens)

    elif next_token.token_type == tokenType['break_keyword']:
        node = parse_break(tokens)

    elif next_token.token_type == tokenType['continue_keyword']:
        node = parse_continue(tokens)

    else:
        node = parse_option_expression(tokens)

        token = next(tokens)
        if token.token_type != tokenType['semi_colon']:
            raise "; expected after assignment"

    return node


def parse_for(tokens):
    node = ForNode()
    token = next(tokens)
    if token.token_type != tokenType['for_keyword']:
        raise "for expected"
    token = next(tokens)
    if token.token_type != tokenType['open_parenthesis']:
        raise "( expected"

    node.initial_expression = parse_option_expression(tokens)

    token = next(tokens)
    if token.token_type != tokenType['semi_colon']:
        raise "; expected after assignment"

    node.condition = parse_option_expression(tokens)
    token = next(tokens)
    if token.token_type != tokenType['semi_colon']:
        raise "; expected after expression"

    node.post_expression = parse_option_expression(tokens)

    token = next(tokens)
    if token.token_type != tokenType['close_parenthesis']:
        raise ") expected"

    node.body = parse_statement(tokens)

    return node


def parse_for_declaration(tokens):
    node = ForDeclarationNode()
    token = next(tokens)
    if token.token_type != tokenType['for_keyword']:
        raise "for expected"
    token = next(tokens)
    if token.token_type != tokenType['open_parenthesis']:
        raise "( expected"

    node.initial_expression = parse_declaration(tokens)
    node.condition = parse_option_expression(tokens)

    token = next(tokens)
    if token.token_type != tokenType['semi_colon']:
        raise "; expected after expression"

    node.post_expression = parse_option_expression(tokens)

    token = next(tokens)
    if token.token_type != tokenType['close_parenthesis']:
        raise ") expected"

    node.body = parse_statement(tokens)

    return node


def parse_while(tokens):
    node = WhileNode()
    token = next(tokens)
    if token.token_type != tokenType['while_keyword']:
        raise "while expected"
    token = next(tokens)
    if token.token_type != tokenType['open_parenthesis']:
        raise "( expected"

    node.condition = parse_expression(tokens)

    token = next(tokens)
    if token.token_type != tokenType['close_parenthesis']:
        raise ") expected"

    node.body = parse_statement(tokens)

    return node


def parse_do_while(tokens):
    node = DoWhileNode()
    token = next(tokens)

    if token.token_type != tokenType['do_keyword']:
        raise "do expected"

    node.body = parse_statement(tokens)

    token = next(tokens)
    if token.token_type != tokenType['while_keyword']:
        raise "while expected"

    node.condition = parse_expression(tokens)

    return node


def parse_break(tokens):
    token = next(tokens)
    if token.token_type != tokenType['break_keyword']:
        raise "break expected"

    node = BreakNode()

    token = next(tokens)
    if token.token_type != tokenType['semi_colon']:
        raise "; expected after break"

    return node


def parse_continue(tokens):
    token = next(tokens)
    if token.token_type != tokenType['continue_keyword']:
        raise "continue expected"

    node = ContinueNode()

    token = next(tokens)
    if token.token_type != tokenType['semi_colon']:
        raise "; expected after continue"

    return node


def parse_compound_block(tokens):
    node = CompoundNode()

    open_brace_token = next(tokens)
    if open_brace_token.token_type != tokenType['open_brace']:
        raise "{ expected"

    next_token = tokens.peek()
    node.statements = []

    while next_token.token_type != tokenType['close_brace']:
        node.statements.append(parse_block_item(tokens))
        next_token = tokens.peek()

    close_brace_token = next(tokens)
    if close_brace_token.token_type != tokenType['close_brace']:
        raise "} expected"

    return node


def parse_block_item(tokens):
    next_token = tokens.peek()
    if next_token.token_type == tokenType['int_keyword']:
        node = parse_declaration(tokens)
    else:
        node = parse_statement(tokens)

    return node


def parse_declaration(tokens):
    next_token = tokens.peek()
    if next_token.token_type == tokenType['int_keyword']:
        d_type = next(tokens)
        v_name = next(tokens)
        node = DeclarationNode(v_name.value)
        next_token = tokens.peek()
        if next_token.token_type == tokenType['assignment']:
            token = next(tokens)
            node.left = parse_expression(tokens)

        token = next(tokens)
        if token.token_type != tokenType['semi_colon']:
            raise "; expected after int"
    else:
        raise 'wrong declaraion'

    return node


def parse_option_expression(tokens):
    next_token = tokens.peek()
    if next_token.token_type == tokenType['semi_colon'] or next_token.token_type == tokenType['close_parenthesis']:
        return NullNode()
    else:
        return parse_expression(tokens)


def parse_expression(tokens):
    identifier = next(tokens)
    next_token = tokens.peek()
    if identifier.token_type == tokenType['identifier'] and next_token.token_type == tokenType['assignment']:
        node = AssignNode(identifier.value)
        next(tokens)
        node.left = parse_expression(tokens)
        return node
    else:
        tokens.prepend(identifier)
        node = parse_conditional_expression(tokens)

    return node


def parse_conditional_expression(tokens):
    node = parse_logical_or_expression(tokens)
    next_token = tokens.peek()

    if next_token.token_type == tokenType['question_mark']:
        next(tokens)
        conditional_node = ConditionalNode()
        conditional_node.condition = node
        node = conditional_node
        node.true_branch = parse_expression(tokens)
        token = next(tokens)
        if token.token_type != tokenType['colon']:
            raise ': expected'
        node.false_branch = parse_conditional_expression(tokens)

    return node


def parse_logical_or_expression(tokens):
    term = parse_logical_and_expression(tokens)
    next_token = tokens.peek()

    while next_token.token_type == tokenType['logical_or']:
        op = next(tokens).token_type
        nextTerm = parse_logical_and_expression(tokens)
        term = parse_binary_operator(op, term, nextTerm)
        next_token = tokens.peek()

    return term


def parse_logical_and_expression(tokens):
    term = parse_equality_expression(tokens)
    nextToken = tokens.peek()

    while nextToken.token_type == tokenType['logical_and']:
        op = next(tokens).token_type
        nextTerm = parse_equality_expression(tokens)
        term = parse_binary_operator(op, term, nextTerm)
        nextToken = tokens.peek()
    return term


def parse_equality_expression(tokens):
    term = parse_relational_expression(tokens)
    next_token = tokens.peek()

    while next_token.token_type == tokenType['equal'] or next_token.token_type == tokenType['not_equal']:
        op = next(tokens).token_type
        nextTerm = parse_relational_expression(tokens)
        term = parse_binary_operator(op, term, nextTerm)
        next_token = tokens.peek()
    return term


def parse_relational_expression(tokens):
    term = parse_additive_expression(tokens)
    next_token = tokens.peek()

    while (next_token.token_type == tokenType['less_than'] or next_token.token_type == tokenType['less_than_equal'] or
           next_token.token_type == tokenType['greater_then'] or next_token.token_type == tokenType['greater_than_or_equal']):

        op = next(tokens).token_type
        nextTerm = parse_additive_expression(tokens)
        term = parse_binary_operator(op, term, nextTerm)
        next_token = tokens.peek()
    return term


def parse_additive_expression(tokens):
    term = parse_term(tokens)
    next_token = tokens.peek()

    while next_token.token_type == tokenType['addition'] or next_token.token_type == tokenType['negation'] or next_token.token_type == tokenType['mod']:
        op = next(tokens).token_type
        next_term = parse_term(tokens)
        term = parse_binary_operator(op, term, next_term)
        next_token = tokens.peek()
    return term


def parse_binary_operator(op, term, next_term):
    node = BinaryOperatorNode(op)
    node.left = term
    node.right = next_term
    return node


def parse_unary_operator(op, term):
    node = UnaryOperatorNode(op.token_type)
    node.left = term
    return node


def parseIntegerLiteral(literal):
    node = ConstantNode(literal.value)
    return node


def parse_term(tokens):
    term = parse_factor(tokens)
    nextToken = tokens.peek()

    while nextToken.token_type == tokenType['multiplication'] or nextToken.token_type == tokenType['division']:
        op = next(tokens).token_type
        nextTerm = parse_factor(tokens)
        term = parse_binary_operator(op, term, nextTerm)
        nextToken = tokens.peek()

    return term


def parse_factor(tokens):
    token = next(tokens)
    next_token = tokens.peek()
    if token.token_type == tokenType['open_parenthesis']:
        exp = parse_expression(tokens)
        if next(tokens).token_type != tokenType['close_parenthesis']:
            raise ') expected'
        return exp
    elif token.token_type == tokenType['identifier'] and next_token.token_type == tokenType['open_parenthesis']:
        tokens.prepend(token)
        node = parse_function_call(tokens)
        return node
    elif is_unary_operator(token):
        factor = parse_factor(tokens)
        return parse_unary_operator(token, factor)
    elif token.token_type == tokenType['integer_literal']:
        return parseIntegerLiteral(token)
    elif token.token_type == tokenType['identifier']:
        return parse_variable(token)
    else:
        raise 'Unrecognized Error'


def parse_variable(variable):
    node = VariableNode(variable.value)
    return node


def is_unary_operator(token):
    return token.token_type == tokenType['negation'] or token.token_type == tokenType['bitwise_complement'] or token.token_type == tokenType['logical_negation']


def is_binary_operator(token):
    return token.token_type == tokenType['addition'] or token.token_type == tokenType['multiplication'] or token.token_type == tokenType['division'] or token.token_type == tokenType['mod']


def parse_tokens(tokens):
    tree = parse_program(tokens)
    return tree


def create_clause_label():
    global clause_label_number
    result = f"clause_{clause_label_number}"
    clause_label_number += 1
    return result


def create_end_label():
    global clause_end_number
    result = f"end_{clause_end_number}"
    clause_end_number += 1
    return result


def create_false_branch_label():
    global clause_false_branch_label
    result = f"false_branch_{clause_false_branch_label}"
    clause_false_branch_label += 1
    return result


def create_post_conditional_number():
    global clause_post_conditional_number
    result = f"post_conditional_{clause_post_conditional_number}"
    clause_post_conditional_number += 1
    return result


def create_clause_while_start_number():
    global clause_while_start_number
    result = f"while_start_{clause_while_start_number}"
    clause_while_start_number += 1
    return result


def create_clause_while_end_number():
    global clause_while_end_number
    result = f"while_end_{clause_while_end_number}"
    clause_while_end_number += 1
    return result


def create_clause_for_start_number():
    global clause_for_start_number
    result = f"for_start_{clause_for_start_number}"
    clause_for_start_number += 1
    return result


def create_clause_for_end_number():
    global clause_for_end_number
    result = f"for_end_{clause_for_end_number}"
    clause_for_end_number += 1
    return result


def create_clause_for_post_expression_number():
    global clause_for_post_expression_number
    result = f"for_post_expression_{clause_for_post_expression_number}"
    clause_for_post_expression_number += 1
    return result


class Labels:
    def __init__(self, start_label, end_label, post_expression_label):
        self.start_label = start_label
        self.end_label = end_label
        self.post_expression_label = post_expression_label


class Context:
    def __init__(self, variables_data, labels, stack_index, current_scope, function_name):
        self.variables_data = variables_data
        self.labels = labels
        self.stack_index = stack_index
        self.current_scope = current_scope
        self.function_name = function_name
        self.global_variables = {}


def generate(tree):
    context = Context({}, Labels(None, None, None), 0, None, None)

    result = ''
    result += process_node(tree, result, context)
    result += '\n'
    return result


def process_node(node, result, context):
    if isinstance(node, ProgramNode):
        result += '    .globl	_main\n'
        for statement in node.top_level_items:
            result = process_node(statement, result, context)

        result += '.section	data\n'
        for variable_name in context.global_variables:
            result += f"    .globl _{variable_name}\n"
            result += f"    .p2align 4\n"
            result += f"_{variable_name}:\n"
            result += f"    .long {context.global_variables[variable_name]}\n"

    elif isinstance(node, FunctionNode):
        result = process_function(node, result, context)
    elif isinstance(node, DeclarationNode):
        result = generate_declaration(node, result, context)
    else:
        result = process_expression(node, result, context)

    return result


def generate_declaration(node, result, context):

    if context.stack_index == 0:
        context.variables_data[node.name] = f"_{node.name}(%rip)"
        if hasattr(node, 'left'):
            context.global_variables[node.name] = node.left.value
        else:
            if node.name not in context.global_variables:
                context.global_variables[node.name] = 0

    elif context.current_scope is None:
        context.variables_data[node.name] = f"{context.stack_index}(%rbp)"
        context.stack_index = context.stack_index - 8
    else:
        context.current_scope[node.name] = f"{context.stack_index}(%rbp)"
        context.stack_index = context.stack_index - 8

    result += f"#Declaration start\n"
    result += f"    push %rax\n"

    if hasattr(node, 'left'):
        result = process_expression(node.left, result, context)
        result += f"    movq %rax, {context.stack_index + 8}(%rbp)\n\n"

    result += f"#Declaration end\n"

    return result


def process_function(node, result, context):

    new_context = copy.deepcopy(context)

    function_name = node.name

    new_context.function_name = function_name

    result += f"_{function_name}:\n"
    result += f"    push %rbp\n"
    result += f"    movq %rsp, %rbp\n"
    result += f"    movq $0, %rax\n\n"

    variables = node.variables
    if len(variables) > 0:
        new_context.variables_data[variables[0]] = "%rdi"
    if len(variables) > 1:
        new_context.variables_data[variables[1]] = "%rsi"
    if len(variables) > 2:
        new_context.variables_data[variables[2]] = "%rdx"

    new_context.stack_index = -8

    for statement in node.statements:
        if isinstance(statement, DeclarationNode):
            result = generate_declaration(
                statement, result, new_context)

        else:
            result, new_context = generate_statement(
                statement, result,  new_context)

    result += f"\nend_label_{new_context.function_name}:\n"
    result += f"    movq %rbp, %rsp\n"
    result += f"    pop %rbp\n"
    result += f"    ret\n"

    return result


def generate_block(block, result, context):
    new_context = copy.deepcopy(context)
    new_context.current_scope = {}

    for statement in block.statements:
        if isinstance(statement,   DeclarationNode):
            result = generate_declaration(
                statement, result, new_context)
        else:
            new_variables_data = new_context.variables_data | new_context.current_scope
            new_context.variables_data = new_variables_data
            result, new_context = generate_statement(
                statement, result, new_context)

    bytes_to_deallocate = 8 * len(new_context.current_scope)
    result += f"    add ${bytes_to_deallocate}, %rsp\n"
    return result, context


def generate_statement(block, result, context):
    if isinstance(block, NullNode):
        return result, context
    if isinstance(block, WhileNode):
        while_start_label = create_clause_while_start_number()
        while_end_label = create_clause_while_end_number()

        previous_start_label = context.labels.start_label
        previous_end_label = context.labels.end_label
        previous_post_expression_label = context.labels.post_expression_label

        context.labels.start_label = while_start_label
        context.labels.end_label = while_end_label
        context.labels.post_expression_label = while_start_label

        result += f"\n#While condition start\n\n"

        result += f"{while_start_label}:\n"
        result = process_expression(block.condition, result, context)
        result += f"    cmp $0, %rax\n"
        result += f"    je {while_end_label}\n"
        result += f"\n#While condition end\n\n"

        result += f"\n#While body start\n\n"
        result, context = generate_statement(block.body, result, context)

        result += f"    jmp {while_start_label}\n"
        result += f"{while_end_label}:\n"
        result += f"\n#While body end\n\n"

        context.labels.start_label = previous_start_label
        context.labels.end_label = previous_end_label
        context.labels.post_expression_label = previous_post_expression_label

        return result, context
    if isinstance(block, DoWhileNode):
        while_start_label = create_clause_while_start_number()
        while_end_label = create_clause_while_end_number()

        previous_start_label = context.labels.start_label
        previous_end_label = context.labels.end_label
        previous_post_expression_label = context.labels.post_expression_label

        context.labels.start_label = while_start_label
        context.labels.end_label = while_end_label
        context.labels.post_expression_label = while_start_label

        result += f"{while_start_label}:\n"
        result, context = generate_statement(block.body, result, context)

        result = process_expression(block.condition, result, context)
        result += f"    cmp $0, %rax\n"
        result += f"    jne {while_start_label}\n"

        context.labels.start_label = previous_start_label
        context.labels.end_label = previous_end_label
        context.labels.post_expression_label = previous_post_expression_label

        return result, context

    if isinstance(block, ForNode):
        for_start_label = create_clause_for_start_number()
        for_end_label = create_clause_for_end_number()
        for_post_expression_label = create_clause_for_post_expression_number()

        previous_start_label = context.labels.start_label
        previous_end_label = context.labels.end_label
        previous_for_post_expression_label = context.labels.post_expression_label

        context.labels.start_label = for_start_label
        context.labels.end_label = for_end_label
        context.labels.post_expression_label = for_post_expression_label

        result += '\n'
        result = process_expression(block.initial_expression, result, context)
        result += f"\n{for_start_label}:\n"

        if isinstance(block.condition, NullNode):
            result += f"    movq $1, %rax\n"
        else:
            result = process_expression(block.condition, result, context)

        result += f"    cmp $0, %rax\n"
        result += f"    je {for_end_label}\n\n"

        result, context = generate_statement(block.body, result, context)
        result += '\n'

        result += f"{for_post_expression_label}: "
        result = process_expression(block.post_expression, result, context)
        result += f"    jmp {for_start_label}\n"

        result += f"{for_end_label}:\n\n"

        context.labels.start_label = previous_start_label
        context.labels.end_label = previous_end_label
        context.labels.post_expression_label = previous_for_post_expression_label

        return result, context

    if isinstance(block, ForDeclarationNode):
        new_context = copy.deepcopy(context)
        new_context.current_scope = {}
        for_start_label = create_clause_for_start_number()
        for_end_label = create_clause_for_end_number()
        for_post_expression_label = create_clause_for_post_expression_number()

        previous_start_label = new_context.labels.start_label
        previous_end_label = new_context.labels.end_label
        previous_for_post_expression_label = new_context.labels.post_expression_label

        new_context.labels.start_label = for_start_label
        new_context.labels.end_label = for_end_label
        new_context.labels.post_expression_label = for_post_expression_label

        result += '\n'
        result = generate_declaration(
            block.initial_expression, result, new_context)
        result += f"\n#For condition start\n"

        new_variables_data = new_context.variables_data | new_context.current_scope
        new_context.variables_data = new_variables_data

        result += f"\n{for_start_label}:\n"

        if isinstance(block.condition, NullNode):
            result += f"    movq $1, %rax\n"
        else:
            result = process_expression(block.condition, result, new_context)

        result += f"    cmp $0, %rax\n"
        result += f"    je {for_end_label}\n\n"
        result += f"#For condition end\n"

        result += f"\n#For body start\n"
        result, new_context = generate_statement(
            block.body, result, new_context)
        result += '\n'

        result += f"#For body end\n"

        result += f"\n#For post_expression start\n"
        result += f"{for_post_expression_label}:\n"
        result = process_expression(block.post_expression, result, new_context)
        result += f"    jmp {for_start_label}\n"
        result += f"#For post_expression end\n"

        result += f"{for_end_label}:\n\n"

        bytes_to_deallocate = 8 * len(new_context.current_scope)
        result += f"    add ${bytes_to_deallocate}, %rsp\n"

        new_context.labels.start_label = previous_start_label
        new_context.labels.end_label = previous_end_label
        new_context.labels.post_expression_label = previous_for_post_expression_label

        return result, context
    if isinstance(block, CompoundNode):
        result, context = generate_block(
            block, result, context)
    elif isinstance(block, IfNode):
        result += "\n#If condition  start\n\n"

        result = process_expression(block.condition, result, context)
        result += f"    cmp $0, %rax\n"
        false_branch_label = create_false_branch_label()
        post_conditional__label = create_post_conditional_number()
        result += f"    je {false_branch_label}\n"
        result += "\n#If true branch  start\n\n"
        result, context = generate_statement(
            block.true_branch, result, context)
        result += f"    jmp {post_conditional__label}\n"
        result += f"{false_branch_label}:\n"

        if block.false_branch is not None:
            result += "\n#If false branch  start\n\n"
            result, context = generate_statement(
                block.false_branch, result, context)

        result += f"{post_conditional__label}:\n"
    else:
        result = process_expression(block, result,  context)

    return result, context


def process_expression(node, result, context):
    if isinstance(node, ConstantNode):
        result += f"    movq ${node.value}, %rax\n"
    elif isinstance(node, FunctionCallNode):
        args = node.args

        result += f"    push %rdi\n"
        result += f"    push %rsi\n"
        result += f"    push %rdx\n"

        result += f"\n# Align start part start\n\n"
        result += f"    mov %rsp, %rax\n"
        n = (8*(len(args)))
        result += f"    sub ${n}, %rax\n"
        result += f"    xor %rdx, %rdx\n"
        result += f"    mov $16, %rcx\n"
        result += f"    idiv %rcx\n"
        result += f"    sub %rdx, %rsp\n"
        result += f"    push %rdx\n"
        result += f"\n# Align start part end\n\n"

        if len(args) > 0:
            result += f"\n# Put first argument\n\n"
            result = process_expression(args[0], result,  context)
            result += "    movq %rax, %rdi\n"
        if len(args) > 1:
            result += f"\n# Put second argument\n\n"
            result = process_expression(args[1], result,  context)
            result += "    movq %rax, %rsi\n"
        if len(args) > 2:
            result += f"\n# Put third argument\n\n"
            result = process_expression(args[2], result,  context)
            result += "    movq %rax, %rdx\n"

        result += f"    callq _{node.name}\n"

        result += f"\n# Align end part start\n\n"
        result += f"    pop %rdx\n"
        result += f"    add %rdx, %rsp\n"
        result += f"\n# Align end part end\n\n"

        result += f"    pop %rdx\n"
        result += f"    pop %rsi\n"
        result += f"    pop %rdi\n"

    elif isinstance(node, BreakNode):
        result += f"    jmp {context.labels.end_label}\n"
    elif isinstance(node, ContinueNode):
        result += f"    jmp {context.labels.post_expression_label}\n"
    elif isinstance(node, VariableNode):
        variable = context.variables_data[node.name]
        result += f"    movq {variable}, %rax\n"
    elif isinstance(node, ReturnNode):
        if node.name == tokenType['return_']:
            result = process_expression(
                node.left, result, context)
            result += f"    jmp end_label_{context.function_name}\n"
    elif isinstance(node, AssignNode):
        result += "\n#Assignment start\n\n"
        result = process_expression(node.left, result, context)
        variable = context.variables_data[node.name]
        result += f"    movq %rax, {variable}\n"

        result += "\n#Assignment end\n\n"

    elif isinstance(node, ConditionalNode):
        result += "\n#Conditional (a ? b : c) condition  start\n\n"

        result = process_expression(
            node.condition, result, context)
        result += f"    cmp $0, %rax\n"
        false_branch_label = create_false_branch_label()
        post_conditional__label = create_post_conditional_number()

        result += f"    je {false_branch_label}\n"
        result += "\n#Conditional (a ? b : c) true branch  start\n\n"

        result = process_expression(
            node.true_branch, result, context)
        result += f"    jmp {post_conditional__label}\n"
        result += "\n#Conditional (a ? b : c) false branch  start\n\n"

        result += f"{false_branch_label}:\n"
        result = process_expression(
            node.false_branch, result, context)
        result += f"{post_conditional__label}:\n"
    elif isinstance(node, UnaryOperatorNode):
        if node.name == tokenType['negation']:
            result = process_expression(
                node.left, result, context)
            result += f"    neg %rax\n"
        elif node.name == tokenType['bitwise_complement']:
            result = process_expression(
                node.left, result, context)
            result += f"    not %rax\n"
        elif node.name == tokenType['logical_negation']:
            result = process_expression(
                node.left, result, context)
            result += f"    cmp $0, %rax\n"
            result += f"    movq $0, %rax\n"
            result += f"    sete %al\n"
    elif isinstance(node, NullNode):
        return result
    elif isinstance(node, BinaryOperatorNode):

        if node.name == tokenType['logical_or']:
            clauseLabel = create_clause_label()
            end_label = create_end_label()

            result = process_expression(
                node.left, result, context)
            result += f"    cmp $0, %rax\n"
            result += f"    je {clauseLabel}\n"
            result += f"    movq $1, %rax\n"
            result += f"    jmp {end_label}\n"
            result += f"{clauseLabel}:\n"
            result = process_expression(
                node.right, result, context)
            result += f"    cmp $0, %rax\n"
            result += f"    movq $0, %rax\n"
            result += f"    setne %al\n"
            result += f"{end_label}:\n"

        elif node.name == tokenType['logical_and']:
            clauseLabel = create_clause_label()
            end_label = create_end_label()

            result = process_expression(
                node.left, result, context)
            result += f"    cmp $0, %rax\n"
            result += f"    jne {clauseLabel}\n"
            result += f"    jmp {end_label}\n"
            result += f"{clauseLabel}:\n"
            result = process_expression(
                node.right, result, context)
            result += f"    cmp $0, %rax\n"
            result += f"    movq $0, %rax\n"
            result += f"    setne %al\n"
            result += f"{end_label}:\n"

        else:
            result = process_expression(
                node.right, result, context)
            result += f"    push %rax\n"
            result = process_expression(
                node.left, result, context)
            result += f"    pop %rbx\n"

            if node.name == tokenType['negation']:
                result += f"    sub %rbx, %rax\n"

            elif node.name == tokenType['addition']:
                result += f"    add %rbx, %rax\n"

            elif node.name == tokenType['multiplication']:
                result += f"    imul %rbx, %rax\n"

            elif node.name == tokenType['division']:
                result += f"    cqo\n"
                result += f"    idiv %rbx\n"

            elif node.name == tokenType['equal']:
                result += f"    cmp %rbx, %rax\n"
                result += f"    movq $0, %rax\n"
                result += f"    sete %al\n"

            elif node.name == tokenType['not_equal']:
                result += f"    cmp %rbx, %rax\n"
                result += f"    movq $0, %rax\n"
                result += f"    setne %al\n"

            elif node.name == tokenType['greater_then']:
                result += f"    cmp %rbx, %rax\n"
                result += f"    movq $0, %rax\n"
                result += f"    setg %al\n"

            elif node.name == tokenType['greater_than_or_equal']:
                result += f"    cmp %rbx, %rax\n"
                result += f"    movq $0, %rax\n"
                result += f"    setge %al\n"

            elif node.name == tokenType['less_than']:
                result += f"    cmp %rbx, %rax\n"
                result += f"    movq $0, %rax\n"
                result += f"    setl %al\n"

            elif node.name == tokenType['less_than_equal']:
                result += f"    cmp %rbx, %rax\n"
                result += f"    movq $0, %rax\n"
                result += f"    setle %al\n"

            elif node.name == tokenType['mod']:
                result += f"    cqo\n"
                result += f"    idiv %rbx\n"
                result += f"    mov %rdx, %rax\n"

            else:
                raise 'wrong node'
    else:
        raise 'wrong node'
    return result


if __name__=="__main__":
    try:
        file_name = argv[1]
    except:
        file_name = input('Enter the file name you want to compile : ').strip()
    with open(file_name, 'r') as source_script:
        script = source_script.read()
        tokens = create_tokens(script)
        tokens_iterator = peekable(tokens)
        tree = parse_tokens(tokens_iterator)
        compiled = generate(tree)
        with open(f'{file_name.split(".")[0]}.asm', 'a') as assembled_file:
            assembled_file.write(compiled)

    print('Assembly Completed')


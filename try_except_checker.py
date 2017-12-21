import ast
import sys


__version__ = '0.0.1'


class TryExceptUninitializedVariableChecker(object):
    """
    Checks uninitialized variables being used in try/except clauses.

    It protects users from using variables initialized using only the try block
    as these variables might never be initialized once an exception is thrown
    inside the try block.
    """

    name = "TryExceptUninitializedVariable"
    version = __version__
    _code = 'S901'
    _error_tmpl = "S901: Uninitialized variable {} in Try/Except clause at line {}"  # noqa

    def __init__(self, tree, filename):
        self.tree = tree
        self.defined_variables = []

    def _get_assign_node_targets(self, ast_node):
        """Returns the node names and line numbers of all the `ast.Name` type
        node targets present in `ast.Assign` type node.
        """
        assert isinstance(ast_node, ast.Assign), 'Invalid ast node type'

        node_targets = []

        for target in ast_node.targets:
            if isinstance(target, ast.Name):
                node_targets.append(
                    {'name': str(target.id), 'line_no': target.lineno})

        return node_targets

    def _build_function_scope_variables(self, node):
        """Builds a list of variables valid in the current function scope in
        `self.defined_variables`.
        """
        # Add globally declared variables to the function scope
        if isinstance(node, ast.Assign):
            assign_targets = self._get_assign_node_targets(node)
            self.defined_variables += \
                [target['name'] for target in assign_targets]

        # Add top level function variables (and not if/else/try/loop based
        # block variables) to the current functional scope
        if isinstance(node, ast.FunctionDef):
            for child_node in ast.iter_child_nodes(node):
                self._build_function_scope_variables(child_node)

    def _find_uninitialized_variables_in_try_except(self, node):

        uninitialized_variable_report = []
        if not isinstance(node, ast.TryExcept):
            return uninitialized_variable_report

        for child_node in node.body:
            if isinstance(child_node, ast.Assign):
                assigned_targets = self._get_assign_node_targets(child_node)

                for target in assigned_targets:
                    if target['name'] not in self.defined_variables:
                        error_msg = self._error_tmpl.format(
                            target['name'], target['line_no'])
                        uninitialized_variable_report.append(
                            (target['line_no'], 0, error_msg, type(self)))

        return uninitialized_variable_report

    def run(self):
        for node in ast.walk(self.tree):
            self._build_function_scope_variables(node)
            reports = self._find_uninitialized_variables_in_try_except(node)

            for report in reports:
                yield report

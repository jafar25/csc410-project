from pycparser import parse_file
from pycparser.c_ast import *
from minic.c_ast_to_minic import transform
import sys

sys.path.extend(['.', '..'])

all_vars = set()
written_vars = set()


class LHSPrinter(NodeVisitor):
  '''
  Same idea as tutorial
  '''
  def visit_Assignment(self, assignment):
    global all_vars
    global written_vars
    # check the 3 instances
    if isinstance(assignment.lvalue, ID):
      written_vars.add(assignment.lvalue.name)
      all_vars.add(assignment.lvalue.name)
    
    if isinstance(assignment.rvalue, BinaryOp):
      readVisitor().visit(assignment.rvalue)

    if isinstance(assignment.rvalue, ArrayRef):
      all_vars.add(assignment.rvalue.name.name)


class readVisitor(NodeVisitor):
  '''
  Additional visitor for handling read variables in binary operations
  '''
  
  def visit_BinaryOp(self, assignment):
    global all_vars
    if isinstance(assignment.left, ID):
      all_vars.add(assignment.left.name)
    
    if isinstance(assignment.right, ID):
      all_vars.add(assignment.right.name)


mast = parse_file("tests/c_files/minic.c")
LHSPrinter().visit(mast)
print("All variables: " + " ".join(all_vars))
print("Written set: " + " ".join(written_vars))
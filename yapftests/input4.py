# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Basic tests for yapf.reformatter."""

import textwrap
import unittest

from yapf.yapflib import reformatter
from yapf.yapflib import style

from yapftests import yapf_test_helper


class BasicReformatterTest(yapf_test_helper.YAPFTest):

  @classmethod
  def setUpClass(cls):
    style.SetGlobalStyle(style.CreateChromiumStyle())

  def testSimple(self):
    unformatted_code = textwrap.dedent("""\
        if a+b:
            pass
        """)
    expected_formatted_code = textwrap.dedent("""\
        if a + b:
          pass
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testSimpleFunctions(self):
    unformatted_code = textwrap.dedent("""\
        def g():
          pass

        def f():
          pass
        """)
    expected_formatted_code = textwrap.dedent("""\
        def g():
          pass


        def f():
          pass
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testSimpleFunctionsWithTrailingComments(self):
    unformatted_code = textwrap.dedent("""\
        def g():  # Trailing comment
          if (xxxxxxxxxxxx.yyyyyyyy(zzzzzzzzzzzzz[0]) == 'aaaaaaaaaaa' and
              xxxxxxxxxxxx.yyyyyyyy(zzzzzzzzzzzzz[0].mmmmmmmm[0]) == 'bbbbbbb'):
            pass

        def f(  # Intermediate comment
        ):
          if (xxxxxxxxxxxx.yyyyyyyy(zzzzzzzzzzzzz[0]) == 'aaaaaaaaaaa' and
              xxxxxxxxxxxx.yyyyyyyy(zzzzzzzzzzzzz[0].mmmmmmmm[0]) == 'bbbbbbb'):
            pass
        """)
    expected_formatted_code = textwrap.dedent("""\
        def g():  # Trailing comment
          if (xxxxxxxxxxxx.yyyyyyyy(zzzzzzzzzzzzz[0]) == 'aaaaaaaaaaa' and
              xxxxxxxxxxxx.yyyyyyyy(zzzzzzzzzzzzz[0].mmmmmmmm[0]) == 'bbbbbbb'):
            pass


        def f(  # Intermediate comment
        ):
          if (xxxxxxxxxxxx.yyyyyyyy(zzzzzzzzzzzzz[0]) == 'aaaaaaaaaaa' and
              xxxxxxxxxxxx.yyyyyyyy(zzzzzzzzzzzzz[0].mmmmmmmm[0]) == 'bbbbbbb'):
            pass
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testBlankLinesAtEndOfFile(self):
    unformatted_code = textwrap.dedent("""\
        def foobar(): # foo
         pass



        """)
    expected_formatted_code = textwrap.dedent("""\
        def foobar():  # foo
          pass
    """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

    unformatted_code = textwrap.dedent("""\
        x = {  'a':37,'b':42,

        'c':927}

        """)
    expected_formatted_code = textwrap.dedent("""\
        x = {'a': 37, 'b': 42, 'c': 927}
    """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testMultipleUgliness(self):
    unformatted_code = textwrap.dedent("""\
        x = {  'a':37,'b':42,

        'c':927}

        y = 'hello ''world'
        z = 'hello '+'world'
        a = 'hello {}'.format('world')
        class foo  (     object  ):
          def f    (self   ):
            return       37*-+2
          def g(self, x,y=42):
              return y
        def f  (   a ) :
          return      37+-+a[42-x :  y**3]
        """)
    expected_formatted_code = textwrap.dedent("""\
        x = {'a': 37, 'b': 42, 'c': 927}

        y = 'hello ' 'world'
        z = 'hello ' + 'world'
        a = 'hello {}'.format('world')


        class foo(object):

          def f(self):
            return 37 * -+2

          def g(self, x, y=42):
            return y


        def f(a):
          return 37 + -+a[42 - x:y**3]
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testComments(self):
    unformatted_code = textwrap.dedent("""\
        class Foo(object):
          pass

        # Attached comment
        class Bar(object):
          pass

        global_assignment = 42

        # Comment attached to class with decorator.
        # Comment attached to class with decorator.
        @noop
        @noop
        class Baz(object):
          pass

        # Intermediate comment

        class Qux(object):
          pass
        """)
    expected_formatted_code = textwrap.dedent("""\
        class Foo(object):
          pass


        # Attached comment
        class Bar(object):
          pass


        global_assignment = 42


        # Comment attached to class with decorator.
        # Comment attached to class with decorator.
        @noop
        @noop
        class Baz(object):
          pass


        # Intermediate comment


        class Qux(object):
          pass
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testSingleComment(self):
    code = textwrap.dedent("""\
        # Thing 1
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testCommentsWithTrailingSpaces(self):
    unformatted_code = textwrap.dedent("""\
        # Thing 1    
        # Thing 2    
        """)
    expected_formatted_code = textwrap.dedent("""\
        # Thing 1
        # Thing 2
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testCommentsInDataLiteral(self):
    code = textwrap.dedent("""\
        def f():
          return collections.OrderedDict({
              # First comment.
              'fnord': 37,

              # Second comment.
              # Continuation of second comment.
              'bork': 42,

              # Ending comment.
          })
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testEndingWhitespaceAfterSimpleStatement(self):
    code = textwrap.dedent("""\
        import foo as bar
        # Thing 1
        # Thing 2
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testDocstrings(self):
    unformatted_code = textwrap.dedent('''\
        u"""Module-level docstring."""
        import os
        class Foo(object):

          """Class-level docstring."""
          # A comment for qux.
          def qux(self):


            """Function-level docstring.

            A multiline function docstring.
            """
            print('hello {}'.format('world'))
            return 42
        ''')
    expected_formatted_code = textwrap.dedent('''\
        u"""Module-level docstring."""
        import os


        class Foo(object):
          """Class-level docstring."""

          # A comment for qux.
          def qux(self):
            """Function-level docstring.

            A multiline function docstring.
            """
            print('hello {}'.format('world'))
            return 42
        ''')
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testDocstringAndMultilineComment(self):
    unformatted_code = textwrap.dedent('''\
        """Hello world"""
        # A multiline
        # comment
        class bar(object):
          """class docstring"""
          # class multiline
          # comment
          def foo(self):
            """Another docstring."""
            # Another multiline
            # comment
            pass
        ''')
    expected_formatted_code = textwrap.dedent('''\
        """Hello world"""


        # A multiline
        # comment
        class bar(object):
          """class docstring"""

          # class multiline
          # comment
          def foo(self):
            """Another docstring."""
            # Another multiline
            # comment
            pass
        ''')
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testMultilineDocstringAndMultilineComment(self):
    unformatted_code = textwrap.dedent('''\
        """Hello world

        RIP Dennis Richie.
        """
        # A multiline
        # comment
        class bar(object):
          """class docstring

          A classy class.
          """
          # class multiline
          # comment
          def foo(self):
            """Another docstring.

            A functional function.
            """
            # Another multiline
            # comment
            pass
        ''')
    expected_formatted_code = textwrap.dedent('''\
        """Hello world

        RIP Dennis Richie.
        """


        # A multiline
        # comment
        class bar(object):
          """class docstring

          A classy class.
          """

          # class multiline
          # comment
          def foo(self):
            """Another docstring.

            A functional function.
            """
            # Another multiline
            # comment
            pass
        ''')
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testTupleCommaBeforeLastParen(self):
    unformatted_code = textwrap.dedent("""\
        a = ( 1, )
        """)
    expected_formatted_code = textwrap.dedent("""\
        a = (1,)
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testNoBreakOutsideOfBracket(self):
    # FIXME(morbo): How this is formatted is not correct. But it's syntactically
    # correct.
    unformatted_code = textwrap.dedent("""\
        def f():
          assert port >= minimum, \
'Unexpected port %d when minimum was %d.' % (port, minimum)
        """)
    expected_formatted_code = textwrap.dedent("""\
        def f():
          assert port >= minimum, 'Unexpected port %d when minimum was %d.' % (port,
                                                                               minimum)
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testBlankLinesBeforeDecorators(self):
    unformatted_code = textwrap.dedent("""\
        @foo()
        class A(object):
          @bar()
          @baz()
          def x(self):
            pass
        """)
    expected_formatted_code = textwrap.dedent("""\
        @foo()
        class A(object):

          @bar()
          @baz()
          def x(self):
            pass
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testCommentBetweenDecorators(self):
    unformatted_code = textwrap.dedent("""\
        @foo()
        # frob
        @bar
        def x  (self):
            pass
        """)
    expected_formatted_code = textwrap.dedent("""\
        @foo()
        # frob
        @bar
        def x(self):
          pass
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testListComprehension(self):
    unformatted_code = textwrap.dedent("""\
        def given(y):
            [k for k in ()
              if k in y]
        """)
    expected_formatted_code = textwrap.dedent("""\
        def given(y):
          [k for k in () if k in y]
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testListComprehensionPreferOneLine(self):
    unformatted_code = textwrap.dedent("""\
        def given(y):
            long_variable_name = [
                long_var_name + 1
                for long_var_name in ()
                if long_var_name == 2]
        """)
    expected_formatted_code = textwrap.dedent("""\
        def given(y):
          long_variable_name = [
              long_var_name + 1 for long_var_name in () if long_var_name == 2
          ]
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testListComprehensionPreferOneLineOverArithmeticSplit(self):
    unformatted_code = textwrap.dedent("""\
        def given(used_identifiers):
          return (sum(len(identifier)
                      for identifier in used_identifiers) / len(used_identifiers))
        """)
    expected_formatted_code = textwrap.dedent("""\
        def given(used_identifiers):
          return (sum(len(identifier) for identifier in used_identifiers) /
                  len(used_identifiers))
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testListComprehensionPreferThreeLinesForLineWrap(self):
    unformatted_code = textwrap.dedent("""\
        def given(y):
            long_variable_name = [
                long_var_name + 1
                for long_var_name, number_two in ()
                if long_var_name == 2 and number_two == 3]
        """)
    expected_formatted_code = textwrap.dedent("""\
        def given(y):
          long_variable_name = [
              long_var_name + 1
              for long_var_name, number_two in ()
              if long_var_name == 2 and number_two == 3
          ]
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testListComprehensionPreferNoBreakForTrivialExpression(self):
    unformatted_code = textwrap.dedent("""\
        def given(y):
            long_variable_name = [
                long_var_name
                for long_var_name, number_two in ()
                if long_var_name == 2 and number_two == 3]
        """)
    expected_formatted_code = textwrap.dedent("""\
        def given(y):
          long_variable_name = [
              long_var_name for long_var_name, number_two in ()
              if long_var_name == 2 and number_two == 3
          ]
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testOpeningAndClosingBrackets(self):
    unformatted_code = """\
foo( (1, ) )
foo( ( 1, 2, 3  ) )
foo( ( 1, 2, 3, ) )
"""
    expected_formatted_code = """\
foo((1,))
foo((1, 2, 3))
foo((
    1,
    2,
    3,
))
"""
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testSingleLineFunctions(self):
    unformatted_code = textwrap.dedent("""\
        def foo():  return 42
        """)
    expected_formatted_code = textwrap.dedent("""\
        def foo():
          return 42
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testNoQueueSeletionInMiddleOfLine(self):
    # If the queue isn't properly constructed, then a token in the middle of the
    # line may be selected as the one with least penalty. The tokens after that
    # one are then splatted at the end of the line with no formatting.
    unformatted_code = """\
find_symbol(node.type) + "< " + " ".join(find_pattern(n) for n in node.child) + " >"
"""
    expected_formatted_code = """\
find_symbol(node.type) + "< " + " ".join(
    find_pattern(n) for n in node.child) + " >"
"""
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testNoSpacesBetweenSubscriptsAndCalls(self):
    unformatted_code = textwrap.dedent("""\
        aaaaaaaaaa = bbbbbbbb.ccccccccc() [42] (a, 2)
        """)
    expected_formatted_code = textwrap.dedent("""\
        aaaaaaaaaa = bbbbbbbb.ccccccccc()[42](a, 2)
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testNoSpacesBetweenOpeningBracketAndStartingOperator(self):
    # Unary operator.
    unformatted_code = textwrap.dedent("""\
        aaaaaaaaaa = bbbbbbbb.ccccccccc[ -1 ]( -42 )
        """)
    expected_formatted_code = textwrap.dedent("""\
        aaaaaaaaaa = bbbbbbbb.ccccccccc[-1](-42)
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

    # Varargs and kwargs.
    unformatted_code = textwrap.dedent("""\
        aaaaaaaaaa = bbbbbbbb.ccccccccc( *varargs )
        aaaaaaaaaa = bbbbbbbb.ccccccccc( **kwargs )
        """)
    expected_formatted_code = textwrap.dedent("""\
        aaaaaaaaaa = bbbbbbbb.ccccccccc(*varargs)
        aaaaaaaaaa = bbbbbbbb.ccccccccc(**kwargs)
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testMultilineCommentReformatted(self):
    unformatted_code = textwrap.dedent("""\
        if True:
            # This is a multiline
            # comment.
            pass
        """)
    expected_formatted_code = textwrap.dedent("""\
        if True:
          # This is a multiline
          # comment.
          pass
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testDictionaryMakerFormatting(self):
    unformatted_code = textwrap.dedent("""\
        _PYTHON_STATEMENTS = frozenset({
            lambda x, y: 'simple_stmt': 'small_stmt', 'expr_stmt': 'print_stmt', 'del_stmt':
            'pass_stmt', lambda: 'break_stmt': 'continue_stmt', 'return_stmt': 'raise_stmt',
            'yield_stmt': 'import_stmt', lambda: 'global_stmt': 'exec_stmt', 'assert_stmt':
            'if_stmt', 'while_stmt': 'for_stmt',
        })
        """)
    expected_formatted_code = textwrap.dedent("""\
        _PYTHON_STATEMENTS = frozenset({
            lambda x, y: 'simple_stmt': 'small_stmt',
            'expr_stmt': 'print_stmt',
            'del_stmt': 'pass_stmt',
            lambda: 'break_stmt': 'continue_stmt',
            'return_stmt': 'raise_stmt',
            'yield_stmt': 'import_stmt',
            lambda: 'global_stmt': 'exec_stmt',
            'assert_stmt': 'if_stmt',
            'while_stmt': 'for_stmt',
        })
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testSimpleMultilineCode(self):
    unformatted_code = textwrap.dedent("""\
        if True:
          aaaaaaaaaaaaaa.bbbbbbbbbbbbbb.ccccccc(zzzzzzzzzzzz, \
xxxxxxxxxxx, yyyyyyyyyyyy, vvvvvvvvv)
          aaaaaaaaaaaaaa.bbbbbbbbbbbbbb.ccccccc(zzzzzzzzzzzz, \
xxxxxxxxxxx, yyyyyyyyyyyy, vvvvvvvvv)
        """)
    expected_formatted_code = textwrap.dedent("""\
        if True:
          aaaaaaaaaaaaaa.bbbbbbbbbbbbbb.ccccccc(zzzzzzzzzzzz, xxxxxxxxxxx, yyyyyyyyyyyy,
                                                vvvvvvvvv)
          aaaaaaaaaaaaaa.bbbbbbbbbbbbbb.ccccccc(zzzzzzzzzzzz, xxxxxxxxxxx, yyyyyyyyyyyy,
                                                vvvvvvvvv)
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testMultilineComment(self):
    code = textwrap.dedent("""\
        if Foo:
          # Hello world
          # Yo man.
          # Yo man.
          # Yo man.
          # Yo man.
          a = 42
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testMultilineString(self):
    code = textwrap.dedent("""\
        code = textwrap.dedent('''\
            if Foo:
              # Hello world
              # Yo man.
              # Yo man.
              # Yo man.
              # Yo man.
              a = 42
            ''')
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

    unformatted_code = textwrap.dedent('''\
        def f():
            email_text += """<html>This is a really long docstring that goes over the column limit and is multi-line.<br><br>
        <b>Czar: </b>"""+despot["Nicholas"]+"""<br>
        <b>Minion: </b>"""+serf["Dmitri"]+"""<br>
        <b>Residence: </b>"""+palace["Winter"]+"""<br>
        </body>
        </html>"""
        ''')
    expected_formatted_code = textwrap.dedent('''\
        def f():
          email_text += """<html>This is a really long docstring that goes over the column limit and is multi-line.<br><br>
        <b>Czar: </b>""" + despot["Nicholas"] + """<br>
        <b>Minion: </b>""" + serf["Dmitri"] + """<br>
        <b>Residence: </b>""" + palace["Winter"] + """<br>
        </body>
        </html>"""
        ''')
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testSimpleMultilineWithComments(self):
    code = textwrap.dedent("""\
        if (  # This is the first comment
            a and  # This is the second comment
            # This is the third comment
            b):  # A trailing comment
          # Whoa! A normal comment!!
          pass  # Another trailing comment
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testMatchingParenSplittingMatching(self):
    unformatted_code = textwrap.dedent("""\
        def f():
          raise RuntimeError('unable to find insertion point for target node',
                             (target,))
        """)
    expected_formatted_code = textwrap.dedent("""\
        def f():
          raise RuntimeError('unable to find insertion point for target node',
                             (target,))
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testContinuationIndent(self):
    unformatted_code = textwrap.dedent('''\
        class F:
          def _ProcessArgLists(self, node):
            """Common method for processing argument lists."""
            for child in node.children:
              if isinstance(child, pytree.Leaf):
                self._SetTokenSubtype(
                    child, subtype=_ARGLIST_TOKEN_TO_SUBTYPE.get(
                        child.value, format_token.Subtype.NONE))
        ''')
    expected_formatted_code = textwrap.dedent('''\
        class F:

          def _ProcessArgLists(self, node):
            """Common method for processing argument lists."""
            for child in node.children:
              if isinstance(child, pytree.Leaf):
                self._SetTokenSubtype(
                    child,
                    subtype=_ARGLIST_TOKEN_TO_SUBTYPE.get(child.value,
                                                          format_token.Subtype.NONE))
        ''')
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testTrailingCommaAndBracket(self):
    unformatted_code = textwrap.dedent('''\
        a = { 42, }
        b = ( 42, )
        c = [ 42, ]
        ''')
    expected_formatted_code = textwrap.dedent('''\
        a = {
            42,
        }
        b = (42,)
        c = [
            42,
        ]
        ''')
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testI18n(self):
    code = textwrap.dedent("""\
        N_('Some years ago - never mind how long precisely - having little or no money in my purse, and nothing particular to interest me on shore, I thought I would sail about a little and see the watery part of the world.')  # A comment is here.
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

    code = textwrap.dedent("""\
        foo('Fake function call')  #. Some years ago - never mind how long precisely - having little or no money in my purse, and nothing particular to interest me on shore, I thought I would sail about a little and see the watery part of the world.
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testI18nCommentsInDataLiteral(self):
    code = textwrap.dedent("""\
        def f():
          return collections.OrderedDict({
              #. First i18n comment.
              'bork': 'foo',

              #. Second i18n comment.
              'snork': 'bar#.*=\\\\0',
          })
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testClosingBracketIndent(self):
    code = textwrap.dedent('''\
        def f():

          def g():
            while (xxxxxxxxxxxxxxxxxxxxx(yyyyyyyyyyyyy[zzzzz]) == 'aaaaaaaaaaa' and
                   xxxxxxxxxxxxxxxxxxxxx(
                       yyyyyyyyyyyyy[zzzzz].aaaaaaaa[0]) == 'bbbbbbb'):
              pass
        ''')
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testClosingBracketsInlinedInCall(self):
    unformatted_code = textwrap.dedent("""\
        class Foo(object):

          def bar(self):
            self.aaaaaaaa = xxxxxxxxxxxxxxxxxxx.yyyyyyyyyyyyy(
                self.cccccc.ddddddddd.eeeeeeee,
                options={
                    "forkforkfork": 1,
                    "borkborkbork": 2,
                    "corkcorkcork": 3,
                    "horkhorkhork": 4,
                    "porkporkpork": 5,
                    })
        """)
    expected_formatted_code = textwrap.dedent("""\
        class Foo(object):

          def bar(self):
            self.aaaaaaaa = xxxxxxxxxxxxxxxxxxx.yyyyyyyyyyyyy(
                self.cccccc.ddddddddd.eeeeeeee,
                options={
                    "forkforkfork": 1,
                    "borkborkbork": 2,
                    "corkcorkcork": 3,
                    "horkhorkhork": 4,
                    "porkporkpork": 5,
                })
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testLineWrapInForExpression(self):
    code = textwrap.dedent("""\
        class A:

          def x(self, node, name, n=1):
            for i, child in enumerate(
                itertools.ifilter(lambda c: pytree_utils.NodeName(c) == name,
                                  node.pre_order())):
              pass
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testFunctionCallContinuationLine(self):
    code = """\
class foo:

  def bar(self, node, name, n=1):
    if True:
      if True:
        return [(aaaaaaaaaa,
                 bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb(
                     cccc, ddddddddddddddddddddddddddddddddddddd))]
"""
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testI18nNonFormatting(self):
    code = textwrap.dedent("""\
        class F(object):

          def __init__(self, fieldname,
                       #. Error message indicating an invalid e-mail address.
                       message=N_('Please check your email address.'), **kwargs):
            pass
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testNoSpaceBetweenUnaryOpAndOpeningParen(self):
    code = textwrap.dedent("""\
        if ~(a or b):
          pass
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testCommentBeforeFuncDef(self):
    code = textwrap.dedent("""\
        class Foo(object):

          a = 42

          # This is a comment.
          def __init__(self,
                       xxxxxxx,
                       yyyyy=0,
                       zzzzzzz=None,
                       aaaaaaaaaaaaaaaaaa=False,
                       bbbbbbbbbbbbbbb=False):
            pass
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testExcessLineCountWithDefaultKeywords(self):
    unformatted_code = textwrap.dedent("""\
        class Fnord(object):
          def Moo(self):
            aaaaaaaaaaaaaaaa = self._bbbbbbbbbbbbbbbbbbbbbbb(
                ccccccccccccc=ccccccccccccc, ddddddd=ddddddd, eeee=eeee,
                fffff=fffff, ggggggg=ggggggg, hhhhhhhhhhhhh=hhhhhhhhhhhhh,
                iiiiiii=iiiiiiiiiiiiii)
        """)
    expected_formatted_code = textwrap.dedent("""\
        class Fnord(object):

          def Moo(self):
            aaaaaaaaaaaaaaaa = self._bbbbbbbbbbbbbbbbbbbbbbb(
                ccccccccccccc=ccccccccccccc,
                ddddddd=ddddddd,
                eeee=eeee,
                fffff=fffff,
                ggggggg=ggggggg,
                hhhhhhhhhhhhh=hhhhhhhhhhhhh,
                iiiiiii=iiiiiiiiiiiiii)
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testSpaceAfterNotOperator(self):
    code = textwrap.dedent("""\
        if not (this and that):
          pass
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testNoPenaltySplitting(self):
    code = textwrap.dedent("""\
        def f():
          if True:
            if True:
              python_files.extend(
                  os.path.join(filename, f)
                  for f in os.listdir(filename)
                  if IsPythonFile(os.path.join(filename, f)))
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testExpressionPenalties(self):
    code = textwrap.dedent("""\
      def f():
        if ((left.value == '(' and right.value == ')') or
            (left.value == '[' and right.value == ']') or
            (left.value == '{' and right.value == '}')):
          return False
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testLineDepthOfSingleLineStatement(self):
    unformatted_code = textwrap.dedent("""\
        while True: continue
        for x in range(3): continue
        try: a = 42
        except: b = 42
        with open(a) as fd: a = fd.read()
        """)
    expected_formatted_code = textwrap.dedent("""\
        while True:
          continue
        for x in range(3):
          continue
        try:
          a = 42
        except:
          b = 42
        with open(a) as fd:
          a = fd.read()
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testSplitListWithTerminatingComma(self):
    unformatted_code = textwrap.dedent("""\
        FOO = ['bar', 'baz', 'mux', 'qux', 'quux', 'quuux', 'quuuux',
          'quuuuux', 'quuuuuux', 'quuuuuuux', lambda a, b: 37,]
        """)
    expected_formatted_code = textwrap.dedent("""\
        FOO = [
            'bar',
            'baz',
            'mux',
            'qux',
            'quux',
            'quuux',
            'quuuux',
            'quuuuux',
            'quuuuuux',
            'quuuuuuux',
            lambda a, b: 37,
        ]
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testSplitListWithInterspersedComments(self):
    code = textwrap.dedent("""\
        FOO = [
            'bar',  # bar
            'baz',  # baz
            'mux',  # mux
            'qux',  # qux
            'quux',  # quux
            'quuux',  # quuux
            'quuuux',  # quuuux
            'quuuuux',  # quuuuux
            'quuuuuux',  # quuuuuux
            'quuuuuuux',  # quuuuuuux
            lambda a, b: 37  # lambda
        ]
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testRelativeImportStatements(self):
    code = textwrap.dedent("""\
        from ... import bork
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testSingleLineList(self):
    # A list on a single line should prefer to remain contiguous.
    unformatted_code = textwrap.dedent("""\
        bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb = aaaaaaaaaaa(
            ("...", "."), "..",
            ".............................................."
        )
        """)
    expected_formatted_code = textwrap.dedent("""\
        bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb = aaaaaaaaaaa(
            ("...", "."), "..", "..............................................")
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testBlankLinesBeforeFunctionsNotInColumnZero(self):
    unformatted_code = textwrap.dedent("""\
        import signal


        try:
          signal.SIGALRM
          # ..................................................................
          # ...............................................................


          def timeout(seconds=1):
            pass
        except:
          pass
        """)
    expected_formatted_code = textwrap.dedent("""\
        import signal

        try:
          signal.SIGALRM

          # ..................................................................
          # ...............................................................


          def timeout(seconds=1):
            pass
        except:
          pass
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testNoKeywordArgumentBreakage(self):
    code = textwrap.dedent("""\
        class A(object):

          def b(self):
            if self.aaaaaaaaaaaaaaaaaaaa not in self.bbbbbbbbbb(
                cccccccccccccccccccc=True):
              pass
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testTrailerOnSingleLine(self):
    code = """\
urlpatterns = patterns('', url(r'^$', 'homepage_view'),
                       url(r'^/login/$', 'login_view'),
                       url(r'^/login/$', 'logout_view'),
                       url(r'^/user/(?P<username>\\w+)/$', 'profile_view'))
"""
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testIfConditionalParens(self):
    code = textwrap.dedent("""\
        class Foo:

          def bar():
            if True:
              if (child.type == grammar_token.NAME and
                  child.value in substatement_names):
                pass
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testContinuationMarkers(self):
    code = textwrap.dedent("""\
        text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec a diam lectus. "\\
               "Sed sit amet ipsum mauris. Maecenas congue ligula ac quam viverra nec consectetur "\\
               "ante hendrerit. Donec et mollis dolor. Praesent et diam eget libero egestas mattis "\\
               "sit amet vitae augue. Nam tincidunt congue enim, ut porta lorem lacinia consectetur. "\\
               "Donec ut libero sed arcu vehicula ultricies a non tortor. Lorem ipsum dolor sit amet"
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

    code = textwrap.dedent("""\
        from __future__ import nested_scopes, generators, division, absolute_import, with_statement, \\
            print_function, unicode_literals
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

    code = textwrap.dedent("""\
        if aaaaaaaaa == 42 and bbbbbbbbbbbbbb == 42 and \\
           cccccccc == 42:
          pass
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testCommentsWithContinuationMarkers(self):
    code = textwrap.dedent("""\
        def fn(arg):
          v = fn2(key1=True,
                  #c1
                  key2=arg)\\
                        .fn3()
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testMultipleContinuationMarkers(self):
    code = textwrap.dedent("""\
        xyz = \\
            \\
            some_thing()
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testContinuationMarkerAfterStringWithContinuation(self):
    code = """\
s = 'foo \\
    bar' \\
    .format()
"""
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testEmptyContainers(self):
    code = textwrap.dedent("""\
        flags.DEFINE_list(
            'output_dirs', [],
            'Lorem ipsum dolor sit amet, consetetur adipiscing elit. Donec a diam lectus. '
            'Sed sit amet ipsum mauris. Maecenas congue.')
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testSplitStringsIfSurroundedByParens(self):
    unformatted_code = textwrap.dedent("""\
        a = foo.bar({'xxxxxxxxxxxxxxxxxxxxxxx' 'yyyyyyyyyyyyyyyyyyyyyyyyyy': baz[42]} + 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa' 'bbbbbbbbbbbbbbbbbbbbbbbbbb' 'cccccccccccccccccccccccccccccccc' 'ddddddddddddddddddddddddddddd')
        """)
    expected_formatted_code = textwrap.dedent("""\
        a = foo.bar({
            'xxxxxxxxxxxxxxxxxxxxxxx'
            'yyyyyyyyyyyyyyyyyyyyyyyyyy': baz[42]
        } + 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
                    'bbbbbbbbbbbbbbbbbbbbbbbbbb'
                    'cccccccccccccccccccccccccccccccc'
                    'ddddddddddddddddddddddddddddd')
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

    code = textwrap.dedent("""\
        a = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa' \
'bbbbbbbbbbbbbbbbbbbbbbbbbb' 'cccccccccccccccccccccccccccccccc' \
'ddddddddddddddddddddddddddddd'
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testMultilineShebang(self):
    code = textwrap.dedent("""\
        #!/bin/sh
        if "true" : '''\'
        then

        export FOO=123
        exec /usr/bin/env python "$0" "$@"

        exit 127
        fi
        '''

        import os

        assert os.environ['FOO'] == '123'
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testNoSplittingAroundTermOperators(self):
    code = textwrap.dedent("""\
        a_very_long_function_call_yada_yada_etc_etc_etc(long_arg1,
                                                        long_arg2 / long_arg3)
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testNoSplittingWithinSubscriptList(self):
    code = textwrap.dedent("""\
        somequitelongvariablename.somemember[(a, b)] = {
            'somelongkey': 1,
            'someotherlongkey': 2
        }
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testExcessCharacters(self):
    code = textwrap.dedent("""\
        class foo:

          def bar(self):
            self.write(s=[
                '%s%s %s' % ('many of really', 'long strings', '+ just makes up 81')
            ])
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

    unformatted_code = textwrap.dedent("""\
        def _():
          if True:
            if True:
              if contract == allow_contract and attr_dict.get(if_attribute) == has_value:
                return True
        """)
    expected_code = textwrap.dedent("""\
        def _():
          if True:
            if True:
              if contract == allow_contract and attr_dict.get(
                  if_attribute) == has_value:
                return True
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertEqual(expected_code, reformatter.Reformat(uwlines))

  def testDictSetGenerator(self):
    code = textwrap.dedent("""\
        foo = {
            variable: 'hello world. How are you today?'
            for variable in fnord
            if variable != 37
        }
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testUnaryOpInDictionaryValue(self):
    code = textwrap.dedent("""\
        beta = "123"

        test = {'alpha': beta[-1]}

        print(beta[-1])
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testUnaryNotOperator(self):
    code = textwrap.dedent("""\
        if True:
          if True:
            if True:
              if True:
                remote_checksum = self.get_checksum(conn, tmp, dest, inject,
                                                    not directory_prepended, source)
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testRelaxArraySubscriptAffinity(self):
    code = textwrap.dedent("""\
        class A(object):

          def f(self, aaaaaaaaa, bbbbbbbbbbbbb, row):
            if True:
              if True:
                if True:
                  if True:
                    if row[4] is None or row[5] is None:
                      bbbbbbbbbbbbb['..............'] = row[
                          5] if row[5] is not None else 5
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testFunctionCallInDict(self):
    code = "a = {'a': b(c=d, **e)}\n"
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testFunctionCallInNestedDict(self):
    code = "a = {'a': {'a': {'a': b(c=d, **e)}}}\n"
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testUnbreakableNot(self):
    code = textwrap.dedent("""\
        def test():
          if not "Foooooooooooooooooooooooooooooo" or "Foooooooooooooooooooooooooooooo" == "Foooooooooooooooooooooooooooooo":
            pass
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testSplitListWithComment(self):
    code = textwrap.dedent("""\
      a = [
          'a',
          'b',
          'c'  # hello world
      ]
      """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testOverColumnLimit(self):
    unformatted_code = textwrap.dedent("""\
      class Test:

        def testSomething(self):
          expected = {
              ('aaaaaaaaaaaaa', 'bbbb'): 'ccccccccccccccccccccccccccccccccccccccccccc',
              ('aaaaaaaaaaaaa', 'bbbb'): 'ccccccccccccccccccccccccccccccccccccccccccc',
              ('aaaaaaaaaaaaa', 'bbbb'): 'ccccccccccccccccccccccccccccccccccccccccccc',
          }
        """)
    expected_formatted_code = textwrap.dedent("""\
      class Test:

        def testSomething(self):
          expected = {
              ('aaaaaaaaaaaaa', 'bbbb'):
                  'ccccccccccccccccccccccccccccccccccccccccccc',
              ('aaaaaaaaaaaaa', 'bbbb'):
                  'ccccccccccccccccccccccccccccccccccccccccccc',
              ('aaaaaaaaaaaaa', 'bbbb'):
                  'ccccccccccccccccccccccccccccccccccccccccccc',
          }
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testEndingComment(self):
    code = textwrap.dedent("""\
      a = f(
          a="something",
          b="something requiring comment which is quite long",  # comment about b (pushes line over 79)
          c="something else, about which comment doesn't make sense")
      """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testContinuationSpaceRetention(self):
    code = textwrap.dedent("""\
      def fn():
        return module \\
               .method(Object(data,
                   fn2(arg)
               ))
      """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testIfExpressionWithFunctionCall(self):
    code = textwrap.dedent("""\
      if x or z.y(
          a,
          c,
          aaaaaaaaaaaaaaaaaaaaa=aaaaaaaaaaaaaaaaaa,
          bbbbbbbbbbbbbbbbbbbbb=bbbbbbbbbbbbbbbbbb):
        pass
      """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testUnformattedAfterMultilineString(self):
    code = textwrap.dedent("""\
      def foo():
        com_text = \\
      '''
      TEST
      ''' % (input_fname, output_fname)
      """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testNoSpacesAroundKeywordDefaultValues(self):
    code = textwrap.dedent("""\
      sources = {
          'json': request.get_json(silent=True) or {},
          'json2': request.get_json(silent=True),
      }
      json = request.get_json(silent=True) or {}
      """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testNoSplittingBeforeEndingSubscriptBracket(self):
    unformatted_code = textwrap.dedent("""\
        if True:
          if True:
            status = cf.describe_stacks(StackName=stackname)[u'Stacks'][0][u'StackStatus']
        """)
    expected_formatted_code = textwrap.dedent("""\
        if True:
          if True:
            status = cf.describe_stacks(
                StackName=stackname)[u'Stacks'][0][u'StackStatus']
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testNoSplittingOnSingleArgument(self):
    unformatted_code = textwrap.dedent("""\
        xxxxxxxxxxxxxx = (re.search(r'(\\d+\\.\\d+\\.\\d+\\.)\\d+',
                                    aaaaaaa.bbbbbbbbbbbb).group(1) +
                          re.search(r'\\d+\\.\\d+\\.\\d+\\.(\\d+)',
                                    ccccccc).group(1))
        xxxxxxxxxxxxxx = (re.search(r'(\\d+\\.\\d+\\.\\d+\\.)\\d+',
                                    aaaaaaa.bbbbbbbbbbbb).group(a.b) +
                          re.search(r'\\d+\\.\\d+\\.\\d+\\.(\\d+)',
                                    ccccccc).group(c.d))
        """)
    expected_formatted_code = textwrap.dedent("""\
        xxxxxxxxxxxxxx = (
            re.search(r'(\\d+\\.\\d+\\.\\d+\\.)\\d+', aaaaaaa.bbbbbbbbbbbb).group(1) +
            re.search(r'\\d+\\.\\d+\\.\\d+\\.(\\d+)', ccccccc).group(1))
        xxxxxxxxxxxxxx = (
            re.search(r'(\\d+\\.\\d+\\.\\d+\\.)\\d+', aaaaaaa.bbbbbbbbbbbb).group(a.b) +
            re.search(r'\\d+\\.\\d+\\.\\d+\\.(\\d+)', ccccccc).group(c.d))
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testSplittingArraysSensibly(self):
    unformatted_code = textwrap.dedent("""\
        while True:
          while True:
            aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa = list['bbbbbbbbbbbbbbbbbbbbbbbbb'].split(',')
            aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa = list('bbbbbbbbbbbbbbbbbbbbbbbbb').split(',')
        """)
    expected_formatted_code = textwrap.dedent("""\
        while True:
          while True:
            aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa = list[
                'bbbbbbbbbbbbbbbbbbbbbbbbb'].split(',')
            aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa = list(
                'bbbbbbbbbbbbbbbbbbbbbbbbb').split(',')
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testComprehensionForAndIf(self):
    unformatted_code = textwrap.dedent("""\
        class f:

          def __repr__(self):
            tokens_repr = ','.join(['{0}({1!r})'.format(tok.name, tok.value) for tok in self._tokens])
        """)
    expected_formatted_code = textwrap.dedent("""\
        class f:

          def __repr__(self):
            tokens_repr = ','.join(
                ['{0}({1!r})'.format(tok.name, tok.value) for tok in self._tokens])
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testFunctionCallArguments(self):
    unformatted_code = textwrap.dedent("""\
        def f():
          if True:
            pytree_utils.InsertNodesBefore(_CreateCommentsFromPrefix(
                comment_prefix, comment_lineno, comment_column,
                standalone=True), ancestor_at_indent)
            pytree_utils.InsertNodesBefore(_CreateCommentsFromPrefix(
                comment_prefix, comment_lineno, comment_column,
                standalone=True))
        """)
    expected_formatted_code = textwrap.dedent("""\
        def f():
          if True:
            pytree_utils.InsertNodesBefore(
                _CreateCommentsFromPrefix(
                    comment_prefix, comment_lineno, comment_column, standalone=True),
                ancestor_at_indent)
            pytree_utils.InsertNodesBefore(
                _CreateCommentsFromPrefix(
                    comment_prefix, comment_lineno, comment_column, standalone=True))
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testBinaryOperators(self):
    unformatted_code = textwrap.dedent("""\
        a = b ** 37
        c = (20 ** -3) / (_GRID_ROWS ** (code_length - 10))
        """)
    expected_formatted_code = textwrap.dedent("""\
        a = b**37
        c = (20**-3) / (_GRID_ROWS**(code_length - 10))
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

    code = textwrap.dedent("""\
      def f():
        if True:
          if (self.stack[-1].split_before_closing_bracket and
              # FIXME(morbo): Use the 'matching_bracket' instead of this.
              # FIXME(morbo): Don't forget about tuples!
              current.value in ']}'):
            pass
      """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testContiguousList(self):
    code = textwrap.dedent("""\
      [retval1, retval2] = a_very_long_function(argument_1, argument2, argument_3,
                                                argument_4)
      """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testArgsAndKwargsFormatting(self):
    code = textwrap.dedent("""\
      a(a=aaaaaaaaaaaaaaaaaaaaa,
        b=aaaaaaaaaaaaaaaaaaaaaaaa,
        c=aaaaaaaaaaaaaaaaaa,
        *d,
        **e)
      """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

    code = textwrap.dedent("""\
      def foo():
        return [
            Bar(xxx='some string',
                yyy='another long string',
                zzz='a third long string')
        ]
      """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testCommentColumnLimitOverflow(self):
    code = textwrap.dedent("""\
      def f():
        if True:
          TaskManager.get_tags = MagicMock(
              name='get_tags_mock',
              return_value=[157031694470475],
              # side_effect=[(157031694470475), (157031694470475),],
          )
      """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testMultilineLambdas(self):
    try:
      style.SetGlobalStyle(
          style.CreateStyleFromConfig(
              '{based_on_style: chromium, allow_multiline_lambdas: true}'))
      unformatted_code = textwrap.dedent("""\
          class SomeClass(object):
            do_something = True

            def succeeded(self, dddddddddddddd):
              d = defer.succeed(None)

              if self.do_something:
                d.addCallback(lambda _: self.aaaaaa.bbbbbbbbbbbbbbbb.cccccccccccccccccccccccccccccccc(dddddddddddddd))
              return d
          """)
      expected_formatted_code = textwrap.dedent("""\
          class SomeClass(object):
            do_something = True

            def succeeded(self, dddddddddddddd):
              d = defer.succeed(None)

              if self.do_something:
                d.addCallback(lambda _: self.aaaaaa.bbbbbbbbbbbbbbbb.
                              cccccccccccccccccccccccccccccccc(dddddddddddddd))
              return d
          """)
      uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
      self.assertCodeEqual(expected_formatted_code,
                           reformatter.Reformat(uwlines))
    finally:
      style.SetGlobalStyle(style.CreateChromiumStyle())

  def testMultilineDictionaryKeys(self):
    try:
      style.SetGlobalStyle(
          style.CreateStyleFromConfig('{based_on_style: chromium, '
                                      'allow_multiline_dictionary_keys: true}'))
      unformatted_code = textwrap.dedent("""\
          MAP_WITH_LONG_KEYS = {
              ('lorem ipsum', 'dolor sit amet'):
                  1,
              ('consectetur adipiscing elit.', 'Vestibulum mauris justo, ornare eget dolor eget'):
                  2,
              ('vehicula convallis nulla. Vestibulum dictum nisl in malesuada finibus.',):
                  3
          }
          """)
      expected_formatted_code = textwrap.dedent("""\
          MAP_WITH_LONG_KEYS = {
              ('lorem ipsum', 'dolor sit amet'):
                  1,
              ('consectetur adipiscing elit.',
               'Vestibulum mauris justo, ornare eget dolor eget'):
                  2,
              ('vehicula convallis nulla. Vestibulum dictum nisl in malesuada finibus.',):
                  3
          }
          """)
      uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
      self.assertCodeEqual(expected_formatted_code,
                           reformatter.Reformat(uwlines))
    finally:
      style.SetGlobalStyle(style.CreateChromiumStyle())

  def testStableDictionaryFormatting(self):
    try:
      style.SetGlobalStyle(
          style.CreateStyleFromConfig(
              '{based_on_style: pep8, indent_width: 2, '
              'continuation_indent_width: 4, indent_dictionary_value: True}'))
      code = textwrap.dedent("""\
          class A(object):
            def method(self):
              filters = {
                  'expressions': [{
                      'field': {
                          'search_field': {
                              'user_field': 'latest_party__number_of_guests'
                          },
                      }
                  }]
              }
          """)
      uwlines = yapf_test_helper.ParseAndUnwrap(code)
      reformatted_code = reformatter.Reformat(uwlines)
      self.assertCodeEqual(code, reformatted_code)

      uwlines = yapf_test_helper.ParseAndUnwrap(reformatted_code)
      reformatted_code = reformatter.Reformat(uwlines)
      self.assertCodeEqual(code, reformatted_code)
    finally:
      style.SetGlobalStyle(style.CreateChromiumStyle())

  def testStableInlinedDictionaryFormatting(self):
    try:
      style.SetGlobalStyle(style.CreatePEP8Style())
      unformatted_code = textwrap.dedent("""\
          def _():
              url = "http://{0}/axis-cgi/admin/param.cgi?{1}".format(
                  value, urllib.urlencode({'action': 'update', 'parameter': value}))
          """)
      expected_formatted_code = textwrap.dedent("""\
          def _():
              url = "http://{0}/axis-cgi/admin/param.cgi?{1}".format(
                  value, urllib.urlencode({
                      'action': 'update',
                      'parameter': value
                  }))
          """)

      uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
      reformatted_code = reformatter.Reformat(uwlines)
      self.assertCodeEqual(expected_formatted_code, reformatted_code)

      uwlines = yapf_test_helper.ParseAndUnwrap(reformatted_code)
      reformatted_code = reformatter.Reformat(uwlines)
      self.assertCodeEqual(expected_formatted_code, reformatted_code)
    finally:
      style.SetGlobalStyle(style.CreateChromiumStyle())

  def testDontSplitKeywordValueArguments(self):
    unformatted_code = textwrap.dedent("""\
        def mark_game_scored(gid):
          _connect.execute(_games.update().where(_games.c.gid == gid).values(
              scored=True))
        """)
    expected_formatted_code = textwrap.dedent("""\
        def mark_game_scored(gid):
          _connect.execute(
              _games.update().where(_games.c.gid == gid).values(scored=True))
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testDontAddBlankLineAfterMultilineString(self):
    code = textwrap.dedent("""\
      query = '''SELECT id 
      FROM table 
      WHERE day in {}'''
      days = ",".join(days)
      """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testFormattingListComprehensions(self):
    code = textwrap.dedent("""\
      def a():
        if True:
          if True:
            if True:
              columns = [
                  x for x, y in self._heap_this_is_very_long if x.route[0] == choice
              ]
              self._heap = [x for x in self._heap if x.route and x.route[0] == choice]
      """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testNoSplittingWhenBinPacking(self):
    try:
      style.SetGlobalStyle(
          style.CreateStyleFromConfig(
              '{based_on_style: pep8, indent_width: 2, '
              'continuation_indent_width: 4, indent_dictionary_value: True, '
              'dedent_closing_brackets: True, '
              'split_before_named_assigns: False}'))
      code = textwrap.dedent("""\
          a_very_long_function_name(
              long_argument_name_1=1,
              long_argument_name_2=2,
              long_argument_name_3=3,
              long_argument_name_4=4,
          )

          a_very_long_function_name(
              long_argument_name_1=1, long_argument_name_2=2, long_argument_name_3=3,
              long_argument_name_4=4
          )
          """)
      uwlines = yapf_test_helper.ParseAndUnwrap(code)
      reformatted_code = reformatter.Reformat(uwlines)
      self.assertCodeEqual(code, reformatted_code)

      uwlines = yapf_test_helper.ParseAndUnwrap(reformatted_code)
      reformatted_code = reformatter.Reformat(uwlines)
      self.assertCodeEqual(code, reformatted_code)
    finally:
      style.SetGlobalStyle(style.CreateChromiumStyle())

  def testNotSplittingAfterSubscript(self):
    unformatted_code = textwrap.dedent("""\
        if not aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.b(c == d[
                'eeeeee']).ffffff():
          pass
        """)
    expected_formatted_code = textwrap.dedent("""\
        if not aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.b(
            c == d['eeeeee']).ffffff():
          pass
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testSplittingOneArgumentList(self):
    unformatted_code = textwrap.dedent("""\
        def _():
          if True:
            if True:
              if True:
                if True:
                  if True:
                    boxes[id_] = np.concatenate((points.min(axis=0), qoints.max(axis=0)))
        """)
    expected_formatted_code = textwrap.dedent("""\
        def _():
          if True:
            if True:
              if True:
                if True:
                  if True:
                    boxes[id_] = np.concatenate((points.min(axis=0),
                                                 qoints.max(axis=0)))
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testSplittingBeforeFirstElementListArgument(self):
    unformatted_code = textwrap.dedent("""\
        class _():
          @classmethod
          def _pack_results_for_constraint_or(cls, combination, constraints):
            if True:
              if True:
                if True:
                  return cls._create_investigation_result(
                          (
                                  clue for clue in combination if not clue == Verifier.UNMATCHED
                          ), constraints, InvestigationResult.OR
                  )
        """)
    expected_formatted_code = textwrap.dedent("""\
        class _():

          @classmethod
          def _pack_results_for_constraint_or(cls, combination, constraints):
            if True:
              if True:
                if True:
                  return cls._create_investigation_result(
                      (clue for clue in combination if not clue == Verifier.UNMATCHED),
                      constraints, InvestigationResult.OR)
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testSplittingArgumentsTerminatedByComma(self):
    try:
      style.SetGlobalStyle(
          style.CreateStyleFromConfig(
              '{based_on_style: chromium, '
              'split_arguments_when_comma_terminated: True}'))
      unformatted_code = textwrap.dedent("""\
          function_name(argument_name_1=1, argument_name_2=2, argument_name_3=3)

          function_name(argument_name_1=1, argument_name_2=2, argument_name_3=3,)

          a_very_long_function_name(long_argument_name_1=1, long_argument_name_2=2, long_argument_name_3=3, long_argument_name_4=4)

          a_very_long_function_name(long_argument_name_1, long_argument_name_2, long_argument_name_3, long_argument_name_4,)

          r =f0 (1,  2,3,)
          """)
      expected_formatted_code = textwrap.dedent("""\
          function_name(argument_name_1=1, argument_name_2=2, argument_name_3=3)

          function_name(
              argument_name_1=1,
              argument_name_2=2,
              argument_name_3=3,
          )

          a_very_long_function_name(
              long_argument_name_1=1,
              long_argument_name_2=2,
              long_argument_name_3=3,
              long_argument_name_4=4)

          a_very_long_function_name(
              long_argument_name_1,
              long_argument_name_2,
              long_argument_name_3,
              long_argument_name_4,
          )

          r = f0(
              1,
              2,
              3,
          )
          """)
      uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
      reformatted_code = reformatter.Reformat(uwlines)
      self.assertCodeEqual(expected_formatted_code, reformatted_code)

      uwlines = yapf_test_helper.ParseAndUnwrap(reformatted_code)
      reformatted_code = reformatter.Reformat(uwlines)
      self.assertCodeEqual(expected_formatted_code, reformatted_code)
    finally:
      style.SetGlobalStyle(style.CreateChromiumStyle())

  def testImportAsList(self):
    code = textwrap.dedent("""\
        from toto import titi, tata, tutu  # noqa
        from toto import titi, tata, tutu
        from toto import (titi, tata, tutu)
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testDictionaryValuesOnOwnLines(self):
    unformatted_code = textwrap.dedent("""\
        a = {
        'aaaaaaaaaaaaaaaaaaaaaaaa':
            Check('ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ', '=', True),
        'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbb':
            Check('YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY', '=', True),
        'ccccccccccccccc':
            Check('XXXXXXXXXXXXXXXXXXX', '!=', 'SUSPENDED'),
        'dddddddddddddddddddddddddddddd':
            Check('WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW', '=', False),
        'eeeeeeeeeeeeeeeeeeeeeeeeeeeee':
            Check('VVVVVVVVVVVVVVVVVVVVVVVVVVVVVV', '=', False),
        'ffffffffffffffffffffffffff':
            Check('UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU', '=', True),
        'ggggggggggggggggg':
            Check('TTTTTTTTTTTTTTTTTTTTTTTTTTTTTT', '=', True),
        'hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh':
            Check('SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS', '=', True),
        'iiiiiiiiiiiiiiiiiiiiiiii':
            Check('RRRRRRRRRRRRRRRRRRRRRRRRRRR', '=', True),
        'jjjjjjjjjjjjjjjjjjjjjjjjjj':
            Check('QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ', '=', False),
        }
        """)
    expected_formatted_code = textwrap.dedent("""\
        a = {
            'aaaaaaaaaaaaaaaaaaaaaaaa':
                Check('ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ', '=', True),
            'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbb':
                Check('YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY', '=', True),
            'ccccccccccccccc':
                Check('XXXXXXXXXXXXXXXXXXX', '!=', 'SUSPENDED'),
            'dddddddddddddddddddddddddddddd':
                Check('WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW', '=', False),
            'eeeeeeeeeeeeeeeeeeeeeeeeeeeee':
                Check('VVVVVVVVVVVVVVVVVVVVVVVVVVVVVV', '=', False),
            'ffffffffffffffffffffffffff':
                Check('UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU', '=', True),
            'ggggggggggggggggg':
                Check('TTTTTTTTTTTTTTTTTTTTTTTTTTTTTT', '=', True),
            'hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh':
                Check('SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS', '=', True),
            'iiiiiiiiiiiiiiiiiiiiiiii':
                Check('RRRRRRRRRRRRRRRRRRRRRRRRRRR', '=', True),
            'jjjjjjjjjjjjjjjjjjjjjjjjjj':
                Check('QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ', '=', False),
        }
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testDictionaryOnOwnLine(self):
    unformatted_code = textwrap.dedent("""\
        doc = test_utils.CreateTestDocumentViaController(
            content={ 'a': 'b' },
            branch_key=branch.key,
            collection_key=collection.key)
        """)
    expected_formatted_code = textwrap.dedent("""\
        doc = test_utils.CreateTestDocumentViaController(
            content={'a': 'b'}, branch_key=branch.key, collection_key=collection.key)
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

    unformatted_code = textwrap.dedent("""\
        doc = test_utils.CreateTestDocumentViaController(
            content={ 'a': 'b' },
            branch_key=branch.key,
            collection_key=collection.key,
            collection_key2=collection.key2)
        """)
    expected_formatted_code = textwrap.dedent("""\
        doc = test_utils.CreateTestDocumentViaController(
            content={'a': 'b'},
            branch_key=branch.key,
            collection_key=collection.key,
            collection_key2=collection.key2)
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testNestedListsInDictionary(self):
    unformatted_code = textwrap.dedent("""\
        _A = {
            'cccccccccc': ('^^1',),
            'rrrrrrrrrrrrrrrrrrrrrrrrr': ('^7913',  # AAAAAAAAAAAAAA.
                                         ),
            'eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee': ('^6242',  # BBBBBBBBBBBBBBB.
                                                  ),
            'vvvvvvvvvvvvvvvvvvv': ('^27959',  # CCCCCCCCCCCCCCCCCC.
                                    '^19746',  # DDDDDDDDDDDDDDDDDDDDDDD.
                                    '^22907',  # EEEEEEEEEEEEEEEEEEEEEEEE.
                                    '^21098',  # FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF.
                                    '^22826',  # GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG.
                                    '^22769',  # HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH.
                                    '^22935',  # IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII.
                                    '^3982',  # JJJJJJJJJJJJJ.
                                   ),
            'uuuuuuuuuuuu': ('^19745',  # LLLLLLLLLLLLLLLLLLLLLLLLLL.
                             '^21324',  # MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM.
                             '^22831',  # NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN.
                             '^17081',  # OOOOOOOOOOOOOOOOOOOOO.
                            ),
            'eeeeeeeeeeeeee': (
                '^9416',  # Reporter email. Not necessarily the reporter.
                '^^3',  # This appears to be the raw email field.
            ),
            'cccccccccc': ('^21109',  # PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP.
                          ),
        }
        """)
    expected_formatted_code = textwrap.dedent("""\
        _A = {
            'cccccccccc': ('^^1',),
            'rrrrrrrrrrrrrrrrrrrrrrrrr': (
                '^7913',  # AAAAAAAAAAAAAA.
            ),
            'eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee': (
                '^6242',  # BBBBBBBBBBBBBBB.
            ),
            'vvvvvvvvvvvvvvvvvvv': (
                '^27959',  # CCCCCCCCCCCCCCCCCC.
                '^19746',  # DDDDDDDDDDDDDDDDDDDDDDD.
                '^22907',  # EEEEEEEEEEEEEEEEEEEEEEEE.
                '^21098',  # FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF.
                '^22826',  # GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG.
                '^22769',  # HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH.
                '^22935',  # IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII.
                '^3982',  # JJJJJJJJJJJJJ.
            ),
            'uuuuuuuuuuuu': (
                '^19745',  # LLLLLLLLLLLLLLLLLLLLLLLLLL.
                '^21324',  # MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM.
                '^22831',  # NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN.
                '^17081',  # OOOOOOOOOOOOOOOOOOOOO.
            ),
            'eeeeeeeeeeeeee': (
                '^9416',  # Reporter email. Not necessarily the reporter.
                '^^3',  # This appears to be the raw email field.
            ),
            'cccccccccc': (
                '^21109',  # PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP.
            ),
        }
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testNestedDictionary(self):
    unformatted_code = textwrap.dedent("""\
        class _():
          def _():
            breadcrumbs = [{'name': 'Admin',
                            'url': url_for(".home")},
                           {'title': title},]
            breadcrumbs = [{'name': 'Admin',
                            'url': url_for(".home")},
                           {'title': title}]
        """)
    expected_formatted_code = textwrap.dedent("""\
        class _():
          def _():
            breadcrumbs = [
                {
                    'name': 'Admin',
                    'url': url_for(".home")
                },
                {
                    'title': title
                },
            ]
            breadcrumbs = [{'name': 'Admin', 'url': url_for(".home")}, {'title': title}]
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testDictionaryElementsOnOneLine(self):
    code = textwrap.dedent("""\
        class _():

          @mock.patch.dict(
              os.environ,
              {'HTTP_' + xsrf._XSRF_TOKEN_HEADER.replace('-', '_'): 'atoken'})
          def _():
            pass


        AAAAAAAAAAAAAAAAAAAAAAAA = {
            Environment.XXXXXXXXXX: 'some text more text even more tex',
            Environment.YYYYYYY: 'some text more text even more text yet ag',
            Environment.ZZZZZZZZZZZ: 'some text more text even mor etext yet again tex',
        }
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testNotInParams(self):
    unformatted_code = textwrap.dedent("""\
        list("a long line to break the line. a long line to break the brk a long lin", not True)
        """)
    expected_code = textwrap.dedent("""\
        list("a long line to break the line. a long line to break the brk a long lin",
             not True)
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertEqual(expected_code, reformatter.Reformat(uwlines))

  def testNamedAssignNotAtEndOfLine(self):
    unformatted_code = textwrap.dedent("""\
        def _():
          if True:
            with py3compat.open_with_encoding(filename, mode='w',
                                              encoding=encoding) as fd:
              pass
        """)
    expected_code = textwrap.dedent("""\
        def _():
          if True:
            with py3compat.open_with_encoding(
                filename, mode='w', encoding=encoding) as fd:
              pass
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertEqual(expected_code, reformatter.Reformat(uwlines))

  def testBlankLineBeforeClassDocstring(self):
    unformatted_code = textwrap.dedent('''\
        class A:

          """Does something.

          Also, here are some details.
          """

          def __init__(self):
            pass
        ''')
    expected_code = textwrap.dedent('''\
        class A:
          """Does something.

          Also, here are some details.
          """

          def __init__(self):
            pass
        ''')
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertEqual(expected_code, reformatter.Reformat(uwlines))

    try:
      style.SetGlobalStyle(
          style.CreateStyleFromConfig(
              '{based_on_style: chromium, '
              'blank_line_before_class_docstring: True}'))
      unformatted_code = textwrap.dedent('''\
          class A:

            """Does something.

            Also, here are some details.
            """

            def __init__(self):
              pass
          ''')
      expected_formatted_code = textwrap.dedent('''\
          class A:

            """Does something.

            Also, here are some details.
            """

            def __init__(self):
              pass
          ''')
      uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
      self.assertCodeEqual(expected_formatted_code,
                           reformatter.Reformat(uwlines))
    finally:
      style.SetGlobalStyle(style.CreateChromiumStyle())

  def testTupleCohesion(self):
    unformatted_code = textwrap.dedent("""\
        def f():
          this_is_a_very_long_function_name(an_extremely_long_variable_name, (
              'a string that may be too long %s' % 'M15'))
        """)
    expected_code = textwrap.dedent("""\
        def f():
          this_is_a_very_long_function_name(
              an_extremely_long_variable_name,
              ('a string that may be too long %s' % 'M15'))
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertEqual(expected_code, reformatter.Reformat(uwlines))

  def testSubscriptExpression(self):
    code = textwrap.dedent("""\
        foo = d[not a]
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testListWithFunctionCalls(self):
    unformatted_code = textwrap.dedent("""\
        def foo():
          return [
              Bar(
                  xxx='some string',
                  yyy='another long string',
                  zzz='a third long string'), Bar(
                      xxx='some string',
                      yyy='another long string',
                      zzz='a third long string')
          ]
        """)
    expected_code = textwrap.dedent("""\
        def foo():
          return [
              Bar(xxx='some string',
                  yyy='another long string',
                  zzz='a third long string'),
              Bar(xxx='some string',
                  yyy='another long string',
                  zzz='a third long string')
          ]
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertEqual(expected_code, reformatter.Reformat(uwlines))

  def testEllipses(self):
    unformatted_code = textwrap.dedent("""\
        X=...
        Y = X if ... else X
        """)
    expected_code = textwrap.dedent("""\
        X = ...
        Y = X if ... else X
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertEqual(expected_code, reformatter.Reformat(uwlines))

  def testSplittingBeforeFirstArgumentOnFunctionCall(self):
    """Tests split_before_first_argument on a function call."""
    try:
      style.SetGlobalStyle(
          style.CreateStyleFromConfig(
              '{based_on_style: chromium, split_before_first_argument: True}'))
      unformatted_code = textwrap.dedent("""\
          a_very_long_function_name("long string with formatting {0:s}".format(
              "mystring"))
          """)
      expected_formatted_code = textwrap.dedent("""\
          a_very_long_function_name(
              "long string with formatting {0:s}".format("mystring"))
          """)
      uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
      self.assertCodeEqual(expected_formatted_code,
                           reformatter.Reformat(uwlines))
    finally:
      style.SetGlobalStyle(style.CreateChromiumStyle())

  def testSplittingBeforeFirstArgumentOnFunctionDefinition(self):
    """Tests split_before_first_argument on a function definition."""
    try:
      style.SetGlobalStyle(
          style.CreateStyleFromConfig(
              '{based_on_style: chromium, split_before_first_argument: True}'))
      unformatted_code = textwrap.dedent("""\
          def _GetNumberOfSecondsFromElements(year, month, day, hours,
                                              minutes, seconds, microseconds):
            return
          """)
      expected_formatted_code = textwrap.dedent("""\
          def _GetNumberOfSecondsFromElements(
              year, month, day, hours, minutes, seconds, microseconds):
            return
          """)
      uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
      self.assertCodeEqual(expected_formatted_code,
                           reformatter.Reformat(uwlines))
    finally:
      style.SetGlobalStyle(style.CreateChromiumStyle())

  def testSplittingBeforeFirstArgumentOnCompoundStatement(self):
    """Tests split_before_first_argument on a compound statement."""
    try:
      style.SetGlobalStyle(
          style.CreateStyleFromConfig(
              '{based_on_style: chromium, split_before_first_argument: True}'))
      unformatted_code = textwrap.dedent("""\
          if (long_argument_name_1 == 1 or
              long_argument_name_2 == 2 or
              long_argument_name_3 == 3 or
              long_argument_name_4 == 4):
            pass
          """)
      expected_formatted_code = textwrap.dedent("""\
          if (long_argument_name_1 == 1 or long_argument_name_2 == 2 or
              long_argument_name_3 == 3 or long_argument_name_4 == 4):
            pass
          """)
      uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
      self.assertCodeEqual(expected_formatted_code,
                           reformatter.Reformat(uwlines))
    finally:
      style.SetGlobalStyle(style.CreateChromiumStyle())

  def testCoalesceBracketsOnDict(self):
    """Tests coalesce_brackets on a dictionary."""
    try:
      style.SetGlobalStyle(
          style.CreateStyleFromConfig(
              '{based_on_style: chromium, coalesce_brackets: True}'))
      unformatted_code = textwrap.dedent("""\
          date_time_values = (
              {
                  u'year': year,
                  u'month': month,
                  u'day_of_month': day_of_month,
                  u'hours': hours,
                  u'minutes': minutes,
                  u'seconds': seconds
              }
          )
          """)
      expected_formatted_code = textwrap.dedent("""\
          date_time_values = ({
              u'year': year,
              u'month': month,
              u'day_of_month': day_of_month,
              u'hours': hours,
              u'minutes': minutes,
              u'seconds': seconds
          })
          """)
      uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
      self.assertCodeEqual(expected_formatted_code,
                           reformatter.Reformat(uwlines))
    finally:
      style.SetGlobalStyle(style.CreateChromiumStyle())

  def testSplitAfterComment(self):
    try:
      style.SetGlobalStyle(
          style.CreateStyleFromConfig(
              '{based_on_style: chromium, coalesce_brackets: True, '
              'dedent_closing_brackets: true}'))
      code = textwrap.dedent("""\
          if __name__ == "__main__":
            with another_resource:
              account = {
                  "validUntil":
                      int(time() + (6 * 7 * 24 * 60 * 60))  # in 6 weeks time
              }
          """)
      uwlines = yapf_test_helper.ParseAndUnwrap(code)
      self.assertCodeEqual(code, reformatter.Reformat(uwlines))
    finally:
      style.SetGlobalStyle(style.CreateChromiumStyle())

  def testAsyncAsNonKeyword(self):
    try:
      style.SetGlobalStyle(style.CreatePEP8Style())

      # In Python 2, async may be used as a non-keyword identifier.
      code = textwrap.dedent("""\
          from util import async


          class A(object):
              def foo(self):
                  async.run()

              def bar(self):
                  pass
          """)
      uwlines = yapf_test_helper.ParseAndUnwrap(code)
      self.assertCodeEqual(code, reformatter.Reformat(uwlines, verify=False))
    finally:
      style.SetGlobalStyle(style.CreateChromiumStyle())


if __name__ == '__main__':
  unittest.main()

# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Buganizer tests for yapf.reformatter."""

import textwrap
import unittest

from yapf.yapflib import reformatter
from yapf.yapflib import style

from yapftests import yapf_test_helper


class BuganizerFixes(yapf_test_helper.YAPFTest):

  @classmethod
  def setUpClass(cls):
    style.SetGlobalStyle(style.CreateChromiumStyle())

  def testB67935450(self):
    unformatted_code = """\
def _():
  return (
      (Gauge(
          metric='aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
          group_by=group_by + ['metric:process_name'],
          metric_filter={'metric:process_name': process_name_re}),
       Gauge(
           metric='bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb',
           group_by=group_by + ['metric:process_name'],
           metric_filter={'metric:process_name': process_name_re}))
      | expr.Join(
          left_name='start', left_default=0, right_name='end', right_default=0)
      | m.Point(
          m.Cond(m.VAL['end'] != 0, m.VAL['end'], k.TimestampMicros() /
                 1000000L) - m.Cond(m.VAL['start'] != 0, m.VAL['start'],
                                    m.TimestampMicros() / 1000000L)))
"""
    expected_formatted_code = """\
def _():
  return (
      (Gauge(
          metric='aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
          group_by=group_by + ['metric:process_name'],
          metric_filter={'metric:process_name': process_name_re}),
       Gauge(
           metric='bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb',
           group_by=group_by + ['metric:process_name'],
           metric_filter={'metric:process_name': process_name_re}))
      | expr.Join(
          left_name='start', left_default=0, right_name='end', right_default=0)
      | m.Point(
          m.Cond(m.VAL['end'] != 0, m.VAL['end'],
                 k.TimestampMicros() / 1000000L) -
          m.Cond(m.VAL['start'] != 0, m.VAL['start'],
                 m.TimestampMicros() / 1000000L)))
"""
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB66011084(self):
    unformatted_code = """\
X = {
"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa":  # Comment 1.
([] if True else [ # Comment 2.
    "bbbbbbbbbbbbbbbbbbb",  # Comment 3.
    "cccccccccccccccccccccccc", # Comment 4.
    "ddddddddddddddddddddddddd", # Comment 5.
    "eeeeeeeeeeeeeeeeeeeeeeeeeeeeeee", # Comment 6.
    "fffffffffffffffffffffffffffffff", # Comment 7.
    "ggggggggggggggggggggggggggg", # Comment 8.
    "hhhhhhhhhhhhhhhhhh",  # Comment 9.
]),
}
"""
    expected_formatted_code = """\
X = {
    "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa":  # Comment 1.
        ([] if True else [  # Comment 2.
            "bbbbbbbbbbbbbbbbbbb",  # Comment 3.
            "cccccccccccccccccccccccc",  # Comment 4.
            "ddddddddddddddddddddddddd",  # Comment 5.
            "eeeeeeeeeeeeeeeeeeeeeeeeeeeeeee",  # Comment 6.
            "fffffffffffffffffffffffffffffff",  # Comment 7.
            "ggggggggggggggggggggggggggg",  # Comment 8.
            "hhhhhhhhhhhhhhhhhh",  # Comment 9.
        ]),
}
"""
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB67455376(self):
    unformatted_code = """\
sponge_ids.extend(invocation.id() for invocation in self._client.GetInvocationsByLabels(labels))
"""
    expected_formatted_code = """\
sponge_ids.extend(invocation.id()
                  for invocation in self._client.GetInvocationsByLabels(labels))
"""
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB35210351(self):
    unformatted_code = """\
def _():
  config.AnotherRuleThing(
      'the_title_to_the_thing_here',
      {'monitorname': 'firefly',
       'service': ACCOUNTING_THING,
       'severity': 'the_bug',
       'monarch_module_name': alerts.TheLabel(qa_module_regexp, invert=True)},
      fanout,
      alerts.AlertUsToSomething(
          GetTheAlertToIt('the_title_to_the_thing_here'),
          GetNotificationTemplate('your_email_here')))
"""
    expected_formatted_code = """\
def _():
  config.AnotherRuleThing(
      'the_title_to_the_thing_here', {
          'monitorname': 'firefly',
          'service': ACCOUNTING_THING,
          'severity': 'the_bug',
          'monarch_module_name': alerts.TheLabel(qa_module_regexp, invert=True)
      }, fanout,
      alerts.AlertUsToSomething(
          GetTheAlertToIt('the_title_to_the_thing_here'),
          GetNotificationTemplate('your_email_here')))
"""
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB34774905(self):
    unformatted_code = """\
x=[VarExprType(ir_name=IrName( value='x',
expr_type=UnresolvedAttrExprType( atom=UnknownExprType(), attr_name=IrName(
    value='x', expr_type=UnknownExprType(), usage='UNKNOWN', fqn=None,
    astn=None), usage='REF'), usage='ATTR', fqn='<attr>.x', astn=None))]
"""
    expected_formatted_code = """\
x = [
    VarExprType(
        ir_name=IrName(
            value='x',
            expr_type=UnresolvedAttrExprType(
                atom=UnknownExprType(),
                attr_name=IrName(
                    value='x',
                    expr_type=UnknownExprType(),
                    usage='UNKNOWN',
                    fqn=None,
                    astn=None),
                usage='REF'),
            usage='ATTR',
            fqn='<attr>.x',
            astn=None))
]
"""
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB65176185(self):
    code = """\
xx = zip(*[(a, b) for (a, b, c) in yy])
"""
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB35210166(self):
    unformatted_code = """\
def _():
  query = (
      m.Fetch(n.Raw('monarch.BorgTask', '/proc/container/memory/usage'), { 'borg_user': borguser, 'borg_job': jobname })
      | o.Window(m.Align('5m')) | p.GroupBy(['borg_user', 'borg_job', 'borg_cell'], q.Mean()))
"""
    expected_formatted_code = """\
def _():
  query = (
      m.Fetch(
          n.Raw('monarch.BorgTask', '/proc/container/memory/usage'), {
              'borg_user': borguser,
              'borg_job': jobname
          })
      | o.Window(m.Align('5m'))
      | p.GroupBy(['borg_user', 'borg_job', 'borg_cell'], q.Mean()))
"""
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB32167774(self):
    unformatted_code = """\
X = (
    'is_official',
    'is_cover',
    'is_remix',
    'is_instrumental',
    'is_live',
    'has_lyrics',
    'is_album',
    'is_compilation',)
"""
    expected_formatted_code = """\
X = (
    'is_official',
    'is_cover',
    'is_remix',
    'is_instrumental',
    'is_live',
    'has_lyrics',
    'is_album',
    'is_compilation',
)
"""
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB66912275(self):
    unformatted_code = """\
def _():
  with self.assertRaisesRegexp(errors.HttpError, 'Invalid'):
    patch_op = api_client.forwardingRules().patch(
        project=project_id,
        region=region,
        forwardingRule=rule_name,
        body={'fingerprint': base64.urlsafe_b64encode('invalid_fingerprint')}).execute()
"""
    expected_formatted_code = """\
def _():
  with self.assertRaisesRegexp(errors.HttpError, 'Invalid'):
    patch_op = api_client.forwardingRules().patch(
        project=project_id,
        region=region,
        forwardingRule=rule_name,
        body={
            'fingerprint': base64.urlsafe_b64encode('invalid_fingerprint')
        }).execute()
"""
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB67312284(self):
    code = """\
def _():
  self.assertEqual(
      [u'to be published 2', u'to be published 1', u'to be published 0'],
      [el.text for el in page.first_column_tds])
"""
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB65241516(self):
    unformatted_code = """\
checkpoint_files = gfile.Glob(os.path.join(TrainTraceDir(unit_key, "*", "*"), embedding_model.CHECKPOINT_FILENAME + "-*"))
"""
    expected_formatted_code = """\
checkpoint_files = gfile.Glob(
    os.path.join(
        TrainTraceDir(unit_key, "*", "*"),
        embedding_model.CHECKPOINT_FILENAME + "-*"))
"""
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB37460004(self):
    code = textwrap.dedent("""\
        assert all(s not in (_SENTINEL, None) for s in nested_schemas
                  ), 'Nested schemas should never contain None/_SENTINEL'
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB36806207(self):
    code = """\
def _():
  linearity_data = [[row] for row in [
      "%.1f mm" % (np.mean(linearity_values["pos_error"]) * 1000.0),
      "%.1f mm" % (np.max(linearity_values["pos_error"]) * 1000.0),
      "%.1f mm" % (np.mean(linearity_values["pos_error_chunk_mean"]) * 1000.0),
      "%.1f mm" % (np.max(linearity_values["pos_error_chunk_max"]) * 1000.0),
      "%.1f deg" % math.degrees(np.mean(linearity_values["rot_noise"])),
      "%.1f deg" % math.degrees(np.max(linearity_values["rot_noise"])),
      "%.1f deg" % math.degrees(np.mean(linearity_values["rot_drift"])),
      "%.1f deg" % math.degrees(np.max(linearity_values["rot_drift"])),
      "%.1f%%" % (np.max(linearity_values["pos_discontinuity"]) * 100.0),
      "%.1f%%" % (np.max(linearity_values["rot_discontinuity"]) * 100.0)
  ]]
"""
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB36215507(self):
    code = textwrap.dedent("""\
        class X():

          def _():
            aaaaaaaaaaaaa._bbbbbbbbbbbbbbbbbbbbbbbbbbbbbb(
                mmmmmmmmmmmmm, nnnnn, ooooooooo,
                _(ppppppppppppppppppppppppppppppppppppp),
                *(qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq),
                **(qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq))
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB35212469(self):
    unformatted_code = textwrap.dedent("""\
        def _():
          X = {
            'retain': {
                'loadtest':  # This is a comment in the middle of a dictionary entry
                    ('/some/path/to/a/file/that/is/needed/by/this/process')
              }
          }
        """)
    expected_formatted_code = textwrap.dedent("""\
        def _():
          X = {
              'retain': {
                  'loadtest':  # This is a comment in the middle of a dictionary entry
                      ('/some/path/to/a/file/that/is/needed/by/this/process')
              }
          }
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB31063453(self):
    unformatted_code = textwrap.dedent("""\
        def _():
          while ((not mpede_proc) or ((time_time() - last_modified) < FLAGS_boot_idle_timeout)):
            pass
        """)
    expected_formatted_code = textwrap.dedent("""\
        def _():
          while ((not mpede_proc) or
                 ((time_time() - last_modified) < FLAGS_boot_idle_timeout)):
            pass
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB35021894(self):
    unformatted_code = textwrap.dedent("""\
        def _():
          labelacl = Env(qa={
              'read': 'name/some-type-of-very-long-name-for-reading-perms',
              'modify': 'name/some-other-type-of-very-long-name-for-modifying'
          },
                         prod={
                            'read': 'name/some-type-of-very-long-name-for-reading-perms',
                            'modify': 'name/some-other-type-of-very-long-name-for-modifying'
                         })
        """)
    expected_formatted_code = textwrap.dedent("""\
        def _():
          labelacl = Env(
              qa={
                  'read': 'name/some-type-of-very-long-name-for-reading-perms',
                  'modify': 'name/some-other-type-of-very-long-name-for-modifying'
              },
              prod={
                  'read': 'name/some-type-of-very-long-name-for-reading-perms',
                  'modify': 'name/some-other-type-of-very-long-name-for-modifying'
              })
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB34682902(self):
    unformatted_code = textwrap.dedent("""\
        logging.info("Mean angular velocity norm: %.3f", np.linalg.norm(np.mean(ang_vel_arr, axis=0)))
        """)
    expected_formatted_code = textwrap.dedent("""\
        logging.info("Mean angular velocity norm: %.3f",
                     np.linalg.norm(np.mean(ang_vel_arr, axis=0)))
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB33842726(self):
    unformatted_code = textwrap.dedent("""\
        class _():
          def _():
            hints.append(('hg tag -f -l -r %s %s # %s' % (short(ctx.node(
            )), candidatetag, firstline))[:78])
        """)
    expected_formatted_code = textwrap.dedent("""\
        class _():
          def _():
            hints.append(('hg tag -f -l -r %s %s # %s' %
                          (short(ctx.node()), candidatetag, firstline))[:78])
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB32931780(self):
    unformatted_code = textwrap.dedent("""\
        environments = {
            'prod': {
                # this is a comment before the first entry.
                'entry one':
                    'an entry.',
                # this is the comment before the second entry.
                'entry number 2.':
                    'something',
                # this is the comment before the third entry and it's a doozy. So big!
                'who':
                    'allin',
                # This is an entry that has a dictionary in it. It's ugly
                'something': {
                    'page': ['this-is-a-page@xxxxxxxx.com', 'something-for-eml@xxxxxx.com'],
                    'bug': ['bugs-go-here5300@xxxxxx.com'],
                    'email': ['sometypeof-email@xxxxxx.com'],
                },
                # a short comment
                'yolo!!!!!':
                    'another-email-address@xxxxxx.com',
                # this entry has an implicit string concatenation
                'implicit':
                    'https://this-is-very-long.url-addr.com/'
                    '?something=something%20some%20more%20stuff..',
                # A more normal entry.
                '.....':
                    'this is an entry',
            }
        }
        """)
    expected_formatted_code = textwrap.dedent("""\
        environments = {
            'prod': {
                # this is a comment before the first entry.
                'entry one': 'an entry.',
                # this is the comment before the second entry.
                'entry number 2.': 'something',
                # this is the comment before the third entry and it's a doozy. So big!
                'who': 'allin',
                # This is an entry that has a dictionary in it. It's ugly
                'something': {
                    'page': [
                        'this-is-a-page@xxxxxxxx.com', 'something-for-eml@xxxxxx.com'
                    ],
                    'bug': ['bugs-go-here5300@xxxxxx.com'],
                    'email': ['sometypeof-email@xxxxxx.com'],
                },
                # a short comment
                'yolo!!!!!': 'another-email-address@xxxxxx.com',
                # this entry has an implicit string concatenation
                'implicit': 'https://this-is-very-long.url-addr.com/'
                            '?something=something%20some%20more%20stuff..',
                # A more normal entry.
                '.....': 'this is an entry',
            }
        }
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB33047408(self):
    code = textwrap.dedent("""\
        def _():
          for sort in (sorts or []):
            request['sorts'].append({
                'field': {
                    'user_field': sort
                },
                'order': 'ASCENDING'
            })
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB32714745(self):
    code = textwrap.dedent("""\
        class _():

          def _BlankDefinition():
            '''Return a generic blank dictionary for a new field.'''
            return {
                'type': '',
                'validation': '',
                'name': 'fieldname',
                'label': 'Field Label',
                'help': '',
                'initial': '',
                'required': False,
                'required_msg': 'Required',
                'invalid_msg': 'Please enter a valid value',
                'options': {
                    'regex': '',
                    'widget_attr': '',
                    'choices_checked': '',
                    'choices_count': '',
                    'choices': {}
                },
                'isnew': True,
                'dirty': False,
            }
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB32737279(self):
    unformatted_code = textwrap.dedent("""\
        here_is_a_dict = {
            'key':
            # Comment.
            'value'
        }
        """)
    expected_formatted_code = textwrap.dedent("""\
        here_is_a_dict = {
            'key':  # Comment.
                'value'
        }
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB32570937(self):
    code = textwrap.dedent("""\
      def _():
        if (job_message.ball not in ('*', ball) or
            job_message.call not in ('*', call) or
            job_message.mall not in ('*', job_name)):
          return False
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB31937033(self):
    code = textwrap.dedent("""\
        class _():

          def __init__(self, metric, fields_cb=None):
            self._fields_cb = fields_cb or (lambda *unused_args, **unused_kwargs: {})
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB31911533(self):
    code = """\
class _():

  @parameterized.NamedParameters(
      ('IncludingModInfoWithHeaderList', AAAA, aaaa),
      ('IncludingModInfoWithoutHeaderList', BBBB, bbbbb),
      ('ExcludingModInfoWithHeaderList', CCCCC, cccc),
      ('ExcludingModInfoWithoutHeaderList', DDDDD, ddddd),
  )
  def _():
    pass
"""
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB31847238(self):
    unformatted_code = textwrap.dedent("""\
        class _():

          def aaaaa(self, bbbbb, cccccccccccccc=None):  # TODO(who): pylint: disable=unused-argument
            return 1

          def xxxxx(self, yyyyy, zzzzzzzzzzzzzz=None):  # A normal comment that runs over the column limit.
            return 1
        """)
    expected_formatted_code = textwrap.dedent("""\
        class _():

          def aaaaa(self, bbbbb, cccccccccccccc=None):  # TODO(who): pylint: disable=unused-argument
            return 1

          def xxxxx(
              self, yyyyy,
              zzzzzzzzzzzzzz=None):  # A normal comment that runs over the column limit.
            return 1
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB30760569(self):
    unformatted_code = textwrap.dedent("""\
        {'1234567890123456789012345678901234567890123456789012345678901234567890':
             '1234567890123456789012345678901234567890'}
        """)
    expected_formatted_code = textwrap.dedent("""\
        {
            '1234567890123456789012345678901234567890123456789012345678901234567890':
                '1234567890123456789012345678901234567890'
        }
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB26034238(self):
    unformatted_code = textwrap.dedent("""\
        class Thing:

          def Function(self):
            thing.Scrape('/aaaaaaaaa/bbbbbbbbbb/ccccc/dddd/eeeeeeeeeeeeee/ffffffffffffff').AndReturn(42)
        """)
    expected_formatted_code = textwrap.dedent("""\
        class Thing:

          def Function(self):
            thing.Scrape(
                '/aaaaaaaaa/bbbbbbbbbb/ccccc/dddd/eeeeeeeeeeeeee/ffffffffffffff'
            ).AndReturn(42)
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB30536435(self):
    unformatted_code = textwrap.dedent("""\
        def main(unused_argv):
          if True:
            if True:
              aaaaaaaaaaa.comment('import-from[{}] {} {}'.format(
                  bbbbbbbbb.usage,
                  ccccccccc.within,
                  imports.ddddddddddddddddddd(name_item.ffffffffffffffff)))
        """)
    expected_formatted_code = textwrap.dedent("""\
        def main(unused_argv):
          if True:
            if True:
              aaaaaaaaaaa.comment('import-from[{}] {} {}'.format(
                  bbbbbbbbb.usage, ccccccccc.within,
                  imports.ddddddddddddddddddd(name_item.ffffffffffffffff)))
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB30442148(self):
    unformatted_code = textwrap.dedent("""\
        def lulz():
          return (some_long_module_name.SomeLongClassName.
                  some_long_attribute_name.some_long_method_name())
        """)
    expected_formatted_code = textwrap.dedent("""\
        def lulz():
          return (some_long_module_name.SomeLongClassName.some_long_attribute_name.
                  some_long_method_name())
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB26868213(self):
    unformatted_code = textwrap.dedent("""\
      def _():
        xxxxxxxxxxxxxxxxxxx = {
            'ssssss': {'ddddd': 'qqqqq',
                       'p90': aaaaaaaaaaaaaaaaa,
                       'p99': bbbbbbbbbbbbbbbbb,
                       'lllllllllllll': yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy(),},
            'bbbbbbbbbbbbbbbbbbbbbbbbbbbb': {
                'ddddd': 'bork bork bork bo',
                'p90': wwwwwwwwwwwwwwwww,
                'p99': wwwwwwwwwwwwwwwww,
                'lllllllllllll': None,  # use the default
            }
        }
        """)
    expected_formatted_code = textwrap.dedent("""\
      def _():
        xxxxxxxxxxxxxxxxxxx = {
            'ssssss': {
                'ddddd': 'qqqqq',
                'p90': aaaaaaaaaaaaaaaaa,
                'p99': bbbbbbbbbbbbbbbbb,
                'lllllllllllll': yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy(),
            },
            'bbbbbbbbbbbbbbbbbbbbbbbbbbbb': {
                'ddddd': 'bork bork bork bo',
                'p90': wwwwwwwwwwwwwwwww,
                'p99': wwwwwwwwwwwwwwwww,
                'lllllllllllll': None,  # use the default
            }
        }
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB30173198(self):
    code = textwrap.dedent("""\
        class _():

          def _():
            self.assertFalse(
                evaluation_runner.get_larps_in_eval_set('these_arent_the_larps'))
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB29908765(self):
    code = textwrap.dedent("""\
        class _():

          def __repr__(self):
            return '<session %s on %s>' % (self._id,
                                           self._stub._stub.rpc_channel().target())  # pylint:disable=protected-access
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB30087362(self):
    code = textwrap.dedent("""\
        def _():
          for s in sorted(env['foo']):
            bar()
            # This is a comment

          # This is another comment
          foo()
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB30087363(self):
    code = textwrap.dedent("""\
        if False:
          bar()
          # This is a comment
        # This is another comment
        elif True:
          foo()
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB29093579(self):
    unformatted_code = textwrap.dedent("""\
        def _():
          _xxxxxxxxxxxxxxx(aaaaaaaa, bbbbbbbbbbbbbb.cccccccccc[
              dddddddddddddddddddddddddddd.eeeeeeeeeeeeeeeeeeeeee.fffffffffffffffffffff])
        """)
    expected_formatted_code = textwrap.dedent("""\
        def _():
          _xxxxxxxxxxxxxxx(
              aaaaaaaa,
              bbbbbbbbbbbbbb.cccccccccc[dddddddddddddddddddddddddddd.
                                        eeeeeeeeeeeeeeeeeeeeee.fffffffffffffffffffff])
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB26382315(self):
    code = textwrap.dedent("""\
        @hello_world
        # This is a first comment

        # Comment
        def foo():
          pass
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB27616132(self):
    unformatted_code = textwrap.dedent("""\
        if True:
          query.fetch_page.assert_has_calls([
              mock.call(100,
                        start_cursor=None),
              mock.call(100,
                        start_cursor=cursor_1),
              mock.call(100,
                        start_cursor=cursor_2),
          ])
        """)
    expected_formatted_code = textwrap.dedent("""\
        if True:
          query.fetch_page.assert_has_calls([
              mock.call(100, start_cursor=None),
              mock.call(100, start_cursor=cursor_1),
              mock.call(100, start_cursor=cursor_2),
          ])
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB27590179(self):
    unformatted_code = textwrap.dedent("""\
        if True:
          if True:
            self.aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa = (
                { True:
                     self.bbb.cccccccccc(ddddddddddddddddddddddd.eeeeeeeeeeeeeeeeeeeeee),
                 False:
                     self.bbb.cccccccccc(ddddddddddddddddddddddd.eeeeeeeeeeeeeeeeeeeeee)
                })
        """)
    expected_formatted_code = textwrap.dedent("""\
        if True:
          if True:
            self.aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa = ({
                True:
                    self.bbb.cccccccccc(ddddddddddddddddddddddd.eeeeeeeeeeeeeeeeeeeeee),
                False:
                    self.bbb.cccccccccc(ddddddddddddddddddddddd.eeeeeeeeeeeeeeeeeeeeee)
            })
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB27266946(self):
    unformatted_code = textwrap.dedent("""\
        def _():
          aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa = (self.bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb.cccccccccccccccccccccccccccccccccccc)
        """)
    expected_formatted_code = textwrap.dedent("""\
        def _():
          aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa = (
              self.bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb.
              cccccccccccccccccccccccccccccccccccc)
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB25505359(self):
    code = textwrap.dedent("""\
        _EXAMPLE = {
            'aaaaaaaaaaaaaa': [{
                'bbbb': 'cccccccccccccccccccccc',
                'dddddddddddd': []
            }, {
                'bbbb': 'ccccccccccccccccccc',
                'dddddddddddd': []
            }]
        }
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB25324261(self):
    code = textwrap.dedent("""\
        aaaaaaaaa = set(bbbb.cccc
                        for ddd in eeeeee.fffffffffff.gggggggggggggggg
                        for cccc in ddd.specification)
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB25136704(self):
    code = textwrap.dedent("""\
        class f:

          def test(self):
            self.bbbbbbb[0]['aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', {
                'xxxxxx': 'yyyyyy'
            }] = cccccc.ddd('1m', '10x1+1')
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB25165602(self):
    code = textwrap.dedent("""\
        def f():
          ids = {u: i for u, i in zip(self.aaaaa, xrange(42, 42 + len(self.aaaaaa)))}
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB25157123(self):
    code = textwrap.dedent("""\
        def ListArgs():
          FairlyLongMethodName([relatively_long_identifier_for_a_list],
                               another_argument_with_a_long_identifier)
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB25136820(self):
    unformatted_code = textwrap.dedent("""\
        def foo():
          return collections.OrderedDict({
              # Preceding comment.
              'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa':
              '$bbbbbbbbbbbbbbbbbbbbbbbb',
          })
        """)
    expected_formatted_code = textwrap.dedent("""\
        def foo():
          return collections.OrderedDict({
              # Preceding comment.
              'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa':
                  '$bbbbbbbbbbbbbbbbbbbbbbbb',
          })
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB25131481(self):
    unformatted_code = textwrap.dedent("""\
        APPARENT_ACTIONS = ('command_type', {
            'materialize': lambda x: some_type_of_function('materialize ' + x.command_def),
            '#': lambda x: x  # do nothing
        })
        """)
    expected_formatted_code = textwrap.dedent("""\
        APPARENT_ACTIONS = (
            'command_type',
            {
                'materialize':
                    lambda x: some_type_of_function('materialize ' + x.command_def),
                '#':
                    lambda x: x  # do nothing
            })
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB23445244(self):
    unformatted_code = textwrap.dedent("""\
        def foo():
          if True:
            return xxxxxxxxxxxxxxxx(
                command,
                extra_env={
                    "OOOOOOOOOOOOOOOOOOOOO": FLAGS.zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz,
                    "PPPPPPPPPPPPPPPPPPPPP":
                        FLAGS.aaaaaaaaaaaaaa + FLAGS.bbbbbbbbbbbbbbbbbbb,
                })
        """)
    expected_formatted_code = textwrap.dedent("""\
        def foo():
          if True:
            return xxxxxxxxxxxxxxxx(
                command,
                extra_env={
                    "OOOOOOOOOOOOOOOOOOOOO":
                        FLAGS.zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz,
                    "PPPPPPPPPPPPPPPPPPPPP":
                        FLAGS.aaaaaaaaaaaaaa + FLAGS.bbbbbbbbbbbbbbbbbbb,
                })
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB20559654(self):
    unformatted_code = textwrap.dedent("""\
      class A(object):

        def foo(self):
          unused_error, result = server.Query(
              ['AA BBBB CCC DDD EEEEEEEE X YY ZZZZ FFF EEE AAAAAAAA'],
              aaaaaaaaaaa=True, bbbbbbbb=None)
        """)
    expected_formatted_code = textwrap.dedent("""\
      class A(object):

        def foo(self):
          unused_error, result = server.Query(
              ['AA BBBB CCC DDD EEEEEEEE X YY ZZZZ FFF EEE AAAAAAAA'],
              aaaaaaaaaaa=True,
              bbbbbbbb=None)
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB23943842(self):
    unformatted_code = textwrap.dedent("""\
        class F():
          def f():
            self.assertDictEqual(
                accounts, {
                    'foo':
                    {'account': 'foo',
                     'lines': 'l1\\nl2\\nl3\\n1 line(s) were elided.'},
                    'bar': {'account': 'bar',
                            'lines': 'l5\\nl6\\nl7'},
                    'wiz': {'account': 'wiz',
                            'lines': 'l8'}
                })
        """)
    expected_formatted_code = textwrap.dedent("""\
        class F():

          def f():
            self.assertDictEqual(
                accounts, {
                    'foo': {
                        'account': 'foo',
                        'lines': 'l1\\nl2\\nl3\\n1 line(s) were elided.'
                    },
                    'bar': {
                        'account': 'bar',
                        'lines': 'l5\\nl6\\nl7'
                    },
                    'wiz': {
                        'account': 'wiz',
                        'lines': 'l8'
                    }
                })
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB20551180(self):
    unformatted_code = textwrap.dedent("""\
        def foo():
          if True:
            return (struct.pack('aaaa', bbbbbbbbbb, ccccccccccccccc, dddddddd) + eeeeeee)
        """)
    expected_formatted_code = textwrap.dedent("""\
        def foo():
          if True:
            return (
                struct.pack('aaaa', bbbbbbbbbb, ccccccccccccccc, dddddddd) + eeeeeee)
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB23944849(self):
    unformatted_code = textwrap.dedent("""\
        class A(object):
          def xxxxxxxxx(self, aaaaaaa, bbbbbbb=ccccccccccc, dddddd=300, eeeeeeeeeeeeee=None, fffffffffffffff=0):
            pass
        """)
    expected_formatted_code = textwrap.dedent("""\
        class A(object):

          def xxxxxxxxx(self,
                        aaaaaaa,
                        bbbbbbb=ccccccccccc,
                        dddddd=300,
                        eeeeeeeeeeeeee=None,
                        fffffffffffffff=0):
            pass
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB23935890(self):
    unformatted_code = textwrap.dedent("""\
        class F():
          def functioni(self, aaaaaaa, bbbbbbb, cccccc, dddddddddddddd, eeeeeeeeeeeeeee):
            pass
        """)
    expected_formatted_code = textwrap.dedent("""\
        class F():

          def functioni(self, aaaaaaa, bbbbbbb, cccccc, dddddddddddddd,
                        eeeeeeeeeeeeeee):
            pass
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB28414371(self):
    code = textwrap.dedent("""\
        def _():
          return ((m.fffff(
              m.rrr('mmmmmmmmmmmmmmmm', 'ssssssssssssssssssssssssss'), ffffffffffffffff)
                   | m.wwwwww(m.ddddd('1h'))
                   | m.ggggggg(bbbbbbbbbbbbbbb)
                   | m.ppppp(
                       (1 - m.ffffffffffffffff(llllllllllllllllllllll * 1000000, m.vvv))
                       * m.ddddddddddddddddd(m.vvv)),
                   m.fffff(
                       m.rrr('mmmmmmmmmmmmmmmm', 'sssssssssssssssssssssss'),
                       dict(
                           ffffffffffffffff, **{
                               'mmmmmm:ssssss':
                                   m.rrrrrrrrrrr('|'.join(iiiiiiiiiiiiii), iiiiii=True)
                           }))
                   | m.wwwwww(m.rrrr('1h'))
                   | m.ggggggg(bbbbbbbbbbbbbbb))
                  | m.jjjj()
                  | m.ppppp(m.vvv[0] + m.vvv[1]))
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB20127686(self):
    code = textwrap.dedent("""\
        def f():
          if True:
            return ((m.fffff(
                m.rrr('xxxxxxxxxxxxxxxx',
                      'yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy'),
                mmmmmmmm)
                     | m.wwwwww(m.rrrr(self.tttttttttt, self.mmmmmmmmmmmmmmmmmmmmm))
                     | m.ggggggg(self.gggggggg, m.sss()), m.fffff('aaaaaaaaaaaaaaaa')
                     | m.wwwwww(m.ddddd(self.tttttttttt, self.mmmmmmmmmmmmmmmmmmmmm))
                     | m.ggggggg(self.gggggggg))
                    | m.jjjj()
                    | m.ppppp(m.VAL[0] / m.VAL[1]))
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB20016122(self):
    try:
      style.SetGlobalStyle(
          style.CreateStyleFromConfig(
              '{based_on_style: pep8, split_penalty_import_names: 35}'))
      unformatted_code = textwrap.dedent("""\
          from a_very_long_or_indented_module_name_yada_yada import (long_argument_1,
                                                                     long_argument_2)
          """)
      expected_formatted_code = textwrap.dedent("""\
          from a_very_long_or_indented_module_name_yada_yada import (
              long_argument_1, long_argument_2)
          """)
      uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
      self.assertCodeEqual(expected_formatted_code,
                           reformatter.Reformat(uwlines))
    finally:
      style.SetGlobalStyle(style.CreatePEP8Style())

    try:
      style.SetGlobalStyle(
          style.CreateStyleFromConfig('{based_on_style: chromium, '
                                      'split_before_logical_operator: True}'))
      code = textwrap.dedent("""\
          class foo():

            def __eq__(self, other):
              return (isinstance(other, type(self))
                      and self.xxxxxxxxxxx == other.xxxxxxxxxxx
                      and self.xxxxxxxx == other.xxxxxxxx
                      and self.aaaaaaaaaaaa == other.aaaaaaaaaaaa
                      and self.bbbbbbbbbbb == other.bbbbbbbbbbb
                      and self.ccccccccccccccccc == other.ccccccccccccccccc
                      and self.ddddddddddddddddddddddd == other.ddddddddddddddddddddddd
                      and self.eeeeeeeeeeee == other.eeeeeeeeeeee
                      and self.ffffffffffffff == other.time_completed
                      and self.gggggg == other.gggggg and self.hhh == other.hhh
                      and len(self.iiiiiiii) == len(other.iiiiiiii)
                      and all(jjjjjjj in other.iiiiiiii for jjjjjjj in self.iiiiiiii))
          """)
      uwlines = yapf_test_helper.ParseAndUnwrap(code)
      self.assertCodeEqual(code, reformatter.Reformat(uwlines))
    finally:
      style.SetGlobalStyle(style.CreateChromiumStyle())

  def testB22527411(self):
    unformatted_code = textwrap.dedent("""\
        def f():
          if True:
            aaaaaa.bbbbbbbbbbbbbbbbbbbb[-1].cccccccccccccc.ddd().eeeeeeee(ffffffffffffff)
        """)
    expected_formatted_code = textwrap.dedent("""\
        def f():
          if True:
            aaaaaa.bbbbbbbbbbbbbbbbbbbb[-1].cccccccccccccc.ddd().eeeeeeee(
                ffffffffffffff)
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB20849933(self):
    unformatted_code = textwrap.dedent("""\
        def main(unused_argv):
          if True:
            aaaaaaaa = {
                'xxx': '%s/cccccc/ddddddddddddddddddd.jar' %
                       (eeeeee.FFFFFFFFFFFFFFFFFF),
            }
        """)
    expected_formatted_code = textwrap.dedent("""\
        def main(unused_argv):
          if True:
            aaaaaaaa = {
                'xxx':
                    '%s/cccccc/ddddddddddddddddddd.jar' % (eeeeee.FFFFFFFFFFFFFFFFFF),
            }
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB20813997(self):
    code = textwrap.dedent("""\
        def myfunc_1():
          myarray = numpy.zeros((2, 2, 2))
          print(myarray[:, 1, :])
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB20605036(self):
    code = textwrap.dedent("""\
        foo = {
            'aaaa': {
                # A comment for no particular reason.
                'xxxxxxxx': 'bbbbbbbbb',
                'yyyyyyyyyyyyyyyyyy': 'cccccccccccccccccccccccccccccc'
                                      'dddddddddddddddddddddddddddddddddddddddddd',
            }
        }
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB20562732(self):
    code = textwrap.dedent("""\
        foo = [
            # Comment about first list item
            'First item',
            # Comment about second list item
            'Second item',
        ]
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB20128830(self):
    code = textwrap.dedent("""\
        a = {
            'xxxxxxxxxxxxxxxxxxxx': {
                'aaaa':
                    'mmmmmmm',
                'bbbbb':
                    'mmmmmmmmmmmmmmmmmmmmm',
                'cccccccccc': [
                    'nnnnnnnnnnn',
                    'ooooooooooo',
                    'ppppppppppp',
                    'qqqqqqqqqqq',
                ],
            },
        }
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB20073838(self):
    code = textwrap.dedent("""\
        class DummyModel(object):

          def do_nothing(self, class_1_count):
            if True:
              class_0_count = num_votes - class_1_count
              return ('{class_0_name}={class_0_count}, {class_1_name}={class_1_count}'
                      .format(
                          class_0_name=self.class_0_name,
                          class_0_count=class_0_count,
                          class_1_name=self.class_1_name,
                          class_1_count=class_1_count))
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB19626808(self):
    code = textwrap.dedent("""\
        if True:
          aaaaaaaaaaaaaaaaaaaaaaa.bbbbbbbbb(
              'ccccccccccc', ddddddddd='eeeee').fffffffff([ggggggggggggggggggggg])
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB19547210(self):
    code = textwrap.dedent("""\
        while True:
          if True:
            if True:
              if True:
                if xxxxxxxxxxxx.yyyyyyy(aa).zzzzzzz() not in (
                    xxxxxxxxxxxx.yyyyyyyyyyyyyy.zzzzzzzz,
                    xxxxxxxxxxxx.yyyyyyyyyyyyyy.zzzzzzzz):
                  continue
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB19377034(self):
    code = textwrap.dedent("""\
        def f():
          if (aaaaaaaaaaaaaaa.start >= aaaaaaaaaaaaaaa.end or
              bbbbbbbbbbbbbbb.start >= bbbbbbbbbbbbbbb.end):
            return False
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB19372573(self):
    code = textwrap.dedent("""\
        def f():
            if a: return 42
            while True:
                if b: continue
                if c: break
            return 0
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    try:
      style.SetGlobalStyle(style.CreatePEP8Style())
      self.assertCodeEqual(code, reformatter.Reformat(uwlines))
    finally:
      style.SetGlobalStyle(style.CreateChromiumStyle())

  def testB19353268(self):
    code = textwrap.dedent("""\
        a = {1, 2, 3}[x]
        b = {'foo': 42, 'bar': 37}['foo']
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB19287512(self):
    unformatted_code = textwrap.dedent("""\
        class Foo(object):

          def bar(self):
            with xxxxxxxxxx.yyyyy(
                'aaaaaaa.bbbbbbbb.ccccccc.dddddddddddddddddddd.eeeeeeeeeee',
                fffffffffff=(aaaaaaa.bbbbbbbb.ccccccc.dddddddddddddddddddd
                             .Mmmmmmmmmmmmmmmmmm(-1, 'permission error'))):
              self.assertRaises(nnnnnnnnnnnnnnnn.ooooo, ppppp.qqqqqqqqqqqqqqqqq)
        """)
    expected_formatted_code = textwrap.dedent("""\
        class Foo(object):

          def bar(self):
            with xxxxxxxxxx.yyyyy(
                'aaaaaaa.bbbbbbbb.ccccccc.dddddddddddddddddddd.eeeeeeeeeee',
                fffffffffff=(
                    aaaaaaa.bbbbbbbb.ccccccc.dddddddddddddddddddd.Mmmmmmmmmmmmmmmmmm(
                        -1, 'permission error'))):
              self.assertRaises(nnnnnnnnnnnnnnnn.ooooo, ppppp.qqqqqqqqqqqqqqqqq)
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB19194420(self):
    code = textwrap.dedent("""\
        method.Set(
            'long argument goes here that causes the line to break',
            lambda arg2=0.5: arg2)
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB19073499(self):
    code = """\
instance = (
    aaaaaaa.bbbbbbb().ccccccccccccccccc().ddddddddddd({
        'aa': 'context!'
    }).eeeeeeeeeeeeeeeeeee({  # Inline comment about why fnord has the value 6.
        'fnord': 6
    }))
"""
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB18257115(self):
    code = textwrap.dedent("""\
        if True:
          if True:
            self._Test(aaaa, bbbbbbb.cccccccccc, dddddddd, eeeeeeeeeee,
                       [ffff, ggggggggggg, hhhhhhhhhhhh, iiiiii, jjjj])
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB18256666(self):
    code = textwrap.dedent("""\
        class Foo(object):

          def Bar(self):
            aaaaa.bbbbbbb(
                ccc='ddddddddddddddd',
                eeee='ffffffffffffffffffffff-%s-%s' % (gggg, int(time.time())),
                hhhhhh={
                    'iiiiiiiiiii': iiiiiiiiiii,
                    'jjjj': jjjj.jjjjj(),
                    'kkkkkkkkkkkk': kkkkkkkkkkkk,
                },
                llllllllll=mmmmmm.nnnnnnnnnnnnnnnn)
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB18256826(self):
    code = textwrap.dedent("""\
        if True:
          pass
        # A multiline comment.
        # Line two.
        elif False:
          pass

        if True:
          pass
          # A multiline comment.
          # Line two.
        elif False:
          pass
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB18255697(self):
    code = textwrap.dedent("""\
        AAAAAAAAAAAAAAA = {
            'XXXXXXXXXXXXXX': 4242,  # Inline comment
            # Next comment
            'YYYYYYYYYYYYYYYY': ['zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz'],
        }
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB17534869(self):
    unformatted_code = textwrap.dedent("""\
        if True:
          self.assertLess(abs(time.time()-aaaa.bbbbbbbbbbb(
                              datetime.datetime.now())), 1)
        """)
    expected_formatted_code = textwrap.dedent("""\
        if True:
          self.assertLess(
              abs(time.time() - aaaa.bbbbbbbbbbb(datetime.datetime.now())), 1)
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB17489866(self):
    unformatted_code = textwrap.dedent("""\
        def f():
          if True:
            if True:
              return aaaa.bbbbbbbbb(ccccccc=dddddddddddddd({('eeee', \
'ffffffff'): str(j)}))
        """)
    expected_formatted_code = textwrap.dedent("""\
        def f():
          if True:
            if True:
              return aaaa.bbbbbbbbb(
                  ccccccc=dddddddddddddd({
                      ('eeee', 'ffffffff'): str(j)
                  }))
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB17133019(self):
    unformatted_code = textwrap.dedent("""\
        class aaaaaaaaaaaaaa(object):

          def bbbbbbbbbb(self):
            with io.open("/dev/null", "rb"):
              with io.open(os.path.join(aaaaa.bbbbb.ccccccccccc,
                                        DDDDDDDDDDDDDDD,
                                        "eeeeeeeee ffffffffff"
                                       ), "rb") as gggggggggggggggggggg:
                print(gggggggggggggggggggg)
        """)
    expected_formatted_code = textwrap.dedent("""\
        class aaaaaaaaaaaaaa(object):

          def bbbbbbbbbb(self):
            with io.open("/dev/null", "rb"):
              with io.open(
                  os.path.join(aaaaa.bbbbb.ccccccccccc, DDDDDDDDDDDDDDD,
                               "eeeeeeeee ffffffffff"), "rb") as gggggggggggggggggggg:
                print(gggggggggggggggggggg)
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB17011869(self):
    unformatted_code = textwrap.dedent("""\
        '''blah......'''

        class SomeClass(object):
          '''blah.'''

          AAAAAAAAAAAA = {                        # Comment.
              'BBB': 1.0,
                'DDDDDDDD': 0.4811
                                      }
        """)
    expected_formatted_code = textwrap.dedent("""\
        '''blah......'''


        class SomeClass(object):
          '''blah.'''

          AAAAAAAAAAAA = {  # Comment.
              'BBB': 1.0,
              'DDDDDDDD': 0.4811
          }
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB16783631(self):
    unformatted_code = textwrap.dedent("""\
        if True:
          with aaaaaaaaaaaaaa.bbbbbbbbbbbbb.ccccccc(ddddddddddddd,
                                                      eeeeeeeee=self.fffffffffffff
                                                      )as gggg:
            pass
        """)
    expected_formatted_code = textwrap.dedent("""\
        if True:
          with aaaaaaaaaaaaaa.bbbbbbbbbbbbb.ccccccc(
              ddddddddddddd, eeeeeeeee=self.fffffffffffff) as gggg:
            pass
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB16572361(self):
    unformatted_code = textwrap.dedent("""\
        def foo(self):
         def bar(my_dict_name):
          self.my_dict_name['foo-bar-baz-biz-boo-baa-baa'].IncrementBy.assert_called_once_with('foo_bar_baz_boo')
        """)
    expected_formatted_code = textwrap.dedent("""\
        def foo(self):

          def bar(my_dict_name):
            self.my_dict_name[
                'foo-bar-baz-biz-boo-baa-baa'].IncrementBy.assert_called_once_with(
                    'foo_bar_baz_boo')
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB15884241(self):
    unformatted_code = textwrap.dedent("""\
        if 1:
          if 1:
            for row in AAAA:
              self.create(aaaaaaaa="/aaa/bbbb/cccc/dddddd/eeeeeeeeeeeeeeeeeeeeeeeeee/%s" % row [0].replace(".foo", ".bar"), aaaaa=bbb[1], ccccc=bbb[2], dddd=bbb[3], eeeeeeeeeee=[s.strip() for s in bbb[4].split(",")], ffffffff=[s.strip() for s in bbb[5].split(",")], gggggg=bbb[6])
        """)
    expected_formatted_code = textwrap.dedent("""\
        if 1:
          if 1:
            for row in AAAA:
              self.create(
                  aaaaaaaa="/aaa/bbbb/cccc/dddddd/eeeeeeeeeeeeeeeeeeeeeeeeee/%s" %
                  row[0].replace(".foo", ".bar"),
                  aaaaa=bbb[1],
                  ccccc=bbb[2],
                  dddd=bbb[3],
                  eeeeeeeeeee=[s.strip() for s in bbb[4].split(",")],
                  ffffffff=[s.strip() for s in bbb[5].split(",")],
                  gggggg=bbb[6])
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB15697268(self):
    unformatted_code = textwrap.dedent("""\
        def main(unused_argv):
          ARBITRARY_CONSTANT_A = 10
          an_array_with_an_exceedingly_long_name = range(ARBITRARY_CONSTANT_A + 1)
          ok = an_array_with_an_exceedingly_long_name[:ARBITRARY_CONSTANT_A]
          bad_slice = map(math.sqrt, an_array_with_an_exceedingly_long_name[:ARBITRARY_CONSTANT_A])
          a_long_name_slicing = an_array_with_an_exceedingly_long_name[:ARBITRARY_CONSTANT_A]
          bad_slice = ("I am a crazy, no good, string whats too long, etc." + " no really ")[:ARBITRARY_CONSTANT_A]
        """)
    expected_formatted_code = textwrap.dedent("""\
        def main(unused_argv):
          ARBITRARY_CONSTANT_A = 10
          an_array_with_an_exceedingly_long_name = range(ARBITRARY_CONSTANT_A + 1)
          ok = an_array_with_an_exceedingly_long_name[:ARBITRARY_CONSTANT_A]
          bad_slice = map(math.sqrt,
                          an_array_with_an_exceedingly_long_name[:ARBITRARY_CONSTANT_A])
          a_long_name_slicing = an_array_with_an_exceedingly_long_name[:
                                                                       ARBITRARY_CONSTANT_A]
          bad_slice = ("I am a crazy, no good, string whats too long, etc." +
                       " no really ")[:ARBITRARY_CONSTANT_A]
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB15597568(self):
    unformatted_code = textwrap.dedent("""\
        if True:
          if True:
            if True:
              print(("Return code was %d" + (", and the process timed out." if did_time_out else ".")) % errorcode)
        """)
    expected_formatted_code = textwrap.dedent("""\
        if True:
          if True:
            if True:
              print(("Return code was %d" + (", and the process timed out."
                                             if did_time_out else ".")) % errorcode)
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB15542157(self):
    unformatted_code = textwrap.dedent("""\
        aaaaaaaaaaaa = bbbb.ccccccccccccccc(dddddd.eeeeeeeeeeeeee, ffffffffffffffffff, gggggg.hhhhhhhhhhhhhhhhh)
        """)
    expected_formatted_code = textwrap.dedent("""\
        aaaaaaaaaaaa = bbbb.ccccccccccccccc(dddddd.eeeeeeeeeeeeee, ffffffffffffffffff,
                                            gggggg.hhhhhhhhhhhhhhhhh)
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB15438132(self):
    unformatted_code = textwrap.dedent("""\
        if aaaaaaa.bbbbbbbbbb:
           cccccc.dddddddddd(eeeeeeeeeee=fffffffffffff.gggggggggggggggggg)
           if hhhhhh.iiiii.jjjjjjjjjjjjj:
             # This is a comment in the middle of it all.
             kkkkkkk.llllllllll.mmmmmmmmmmmmm = True
           if (aaaaaa.bbbbb.ccccccccccccc != ddddddd.eeeeeeeeee.fffffffffffff or
               eeeeee.fffff.ggggggggggggggggggggggggggg() != hhhhhhh.iiiiiiiiii.jjjjjjjjjjjj):
             aaaaaaaa.bbbbbbbbbbbb(
                 aaaaaa.bbbbb.cc,
                 dddddddddddd=eeeeeeeeeeeeeeeeeee.fffffffffffffffff(
                     gggggg.hh,
                     iiiiiiiiiiiiiiiiiii.jjjjjjjjjj.kkkkkkk,
                     lllll.mm),
                 nnnnnnnnnn=ooooooo.pppppppppp)
        """)
    expected_formatted_code = textwrap.dedent("""\
        if aaaaaaa.bbbbbbbbbb:
          cccccc.dddddddddd(eeeeeeeeeee=fffffffffffff.gggggggggggggggggg)
          if hhhhhh.iiiii.jjjjjjjjjjjjj:
            # This is a comment in the middle of it all.
            kkkkkkk.llllllllll.mmmmmmmmmmmmm = True
          if (aaaaaa.bbbbb.ccccccccccccc != ddddddd.eeeeeeeeee.fffffffffffff or
              eeeeee.fffff.ggggggggggggggggggggggggggg() !=
              hhhhhhh.iiiiiiiiii.jjjjjjjjjjjj):
            aaaaaaaa.bbbbbbbbbbbb(
                aaaaaa.bbbbb.cc,
                dddddddddddd=eeeeeeeeeeeeeeeeeee.fffffffffffffffff(
                    gggggg.hh, iiiiiiiiiiiiiiiiiii.jjjjjjjjjj.kkkkkkk, lllll.mm),
                nnnnnnnnnn=ooooooo.pppppppppp)
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB14468247(self):
    unformatted_code = """\
call(a=1,
    b=2,
)
"""
    expected_formatted_code = """\
call(
    a=1,
    b=2,
)
"""
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB14406499(self):
    unformatted_code = textwrap.dedent("""\
        def foo1(parameter_1, parameter_2, parameter_3, parameter_4, \
parameter_5, parameter_6): pass
        """)
    expected_formatted_code = textwrap.dedent("""\
        def foo1(parameter_1, parameter_2, parameter_3, parameter_4, parameter_5,
                 parameter_6):
          pass
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB13900309(self):
    unformatted_code = textwrap.dedent("""\
        self.aaaaaaaaaaa(  # A comment in the middle of it all.
               948.0/3600, self.bbb.ccccccccccccccccccccc(dddddddddddddddd.eeee, True))
        """)
    expected_formatted_code = textwrap.dedent("""\
        self.aaaaaaaaaaa(  # A comment in the middle of it all.
            948.0 / 3600, self.bbb.ccccccccccccccccccccc(dddddddddddddddd.eeee, True))
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

    code = textwrap.dedent("""\
        aaaaaaaaaa.bbbbbbbbbbbbbbbbbbbbbbbb.cccccccccccccccccccccccccccccc(
            DC_1, (CL - 50, CL), AAAAAAAA, BBBBBBBBBBBBBBBB, 98.0,
            CCCCCCC).ddddddddd(  # Look! A comment is here.
                AAAAAAAA - (20 * 60 - 5))
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

    unformatted_code = textwrap.dedent("""\
        aaaaaaaaaaaaaaaaaaaaaaaa.bbbbbbbbbbbbb.ccccccccccccccccccccccccc().dddddddddddddddddddddddddd(1, 2, 3, 4)
        """)
    expected_formatted_code = textwrap.dedent("""\
        aaaaaaaaaaaaaaaaaaaaaaaa.bbbbbbbbbbbbb.ccccccccccccccccccccccccc(
        ).dddddddddddddddddddddddddd(1, 2, 3, 4)
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

    unformatted_code = textwrap.dedent("""\
        aaaaaaaaaaaaaaaaaaaaaaaa.bbbbbbbbbbbbb.ccccccccccccccccccccccccc(x).dddddddddddddddddddddddddd(1, 2, 3, 4)
        """)
    expected_formatted_code = textwrap.dedent("""\
        aaaaaaaaaaaaaaaaaaaaaaaa.bbbbbbbbbbbbb.ccccccccccccccccccccccccc(
            x).dddddddddddddddddddddddddd(1, 2, 3, 4)
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

    unformatted_code = textwrap.dedent("""\
        aaaaaaaaaaaaaaaaaaaaaaaa(xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx).dddddddddddddddddddddddddd(1, 2, 3, 4)
        """)
    expected_formatted_code = textwrap.dedent("""\
        aaaaaaaaaaaaaaaaaaaaaaaa(
            xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx).dddddddddddddddddddddddddd(1, 2, 3, 4)
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

    unformatted_code = textwrap.dedent("""\
        aaaaaaaaaaaaaaaaaaaaaaaa().bbbbbbbbbbbbbbbbbbbbbbbb().ccccccccccccccccccc().\
dddddddddddddddddd().eeeeeeeeeeeeeeeeeeeee().fffffffffffffffff().gggggggggggggggggg()
        """)
    expected_formatted_code = textwrap.dedent("""\
        aaaaaaaaaaaaaaaaaaaaaaaa().bbbbbbbbbbbbbbbbbbbbbbbb().ccccccccccccccccccc(
        ).dddddddddddddddddd().eeeeeeeeeeeeeeeeeeeee().fffffffffffffffff(
        ).gggggggggggggggggg()
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB67935687(self):
    code = textwrap.dedent("""\
        Fetch(
            Raw('monarch.BorgTask', '/union/row_operator_action_delay'),
            {'borg_user': self.borg_user})
    """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

    unformatted_code = textwrap.dedent("""\
        shelf_renderer.expand_text = text.translate_to_unicode(
            expand_text % {
                'creator': creator
            })
        """)
    expected_formatted_code = textwrap.dedent("""\
        shelf_renderer.expand_text = text.translate_to_unicode(
            expand_text % {'creator': creator})
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))


if __name__ == '__main__':
  unittest.main()
# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Basic tests for yapf.reformatter."""

import textwrap
import unittest

from yapf.yapflib import reformatter
from yapf.yapflib import style

from yapftests import yapf_test_helper


class BasicReformatterTest(yapf_test_helper.YAPFTest):

  @classmethod
  def setUpClass(cls):
    style.SetGlobalStyle(style.CreateChromiumStyle())

  def testSimple(self):
    unformatted_code = textwrap.dedent("""\
        if a+b:
            pass
        """)
    expected_formatted_code = textwrap.dedent("""\
        if a + b:
          pass
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testSimpleFunctions(self):
    unformatted_code = textwrap.dedent("""\
        def g():
          pass

        def f():
          pass
        """)
    expected_formatted_code = textwrap.dedent("""\
        def g():
          pass


        def f():
          pass
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testSimpleFunctionsWithTrailingComments(self):
    unformatted_code = textwrap.dedent("""\
        def g():  # Trailing comment
          if (xxxxxxxxxxxx.yyyyyyyy(zzzzzzzzzzzzz[0]) == 'aaaaaaaaaaa' and
              xxxxxxxxxxxx.yyyyyyyy(zzzzzzzzzzzzz[0].mmmmmmmm[0]) == 'bbbbbbb'):
            pass

        def f(  # Intermediate comment
        ):
          if (xxxxxxxxxxxx.yyyyyyyy(zzzzzzzzzzzzz[0]) == 'aaaaaaaaaaa' and
              xxxxxxxxxxxx.yyyyyyyy(zzzzzzzzzzzzz[0].mmmmmmmm[0]) == 'bbbbbbb'):
            pass
        """)
    expected_formatted_code = textwrap.dedent("""\
        def g():  # Trailing comment
          if (xxxxxxxxxxxx.yyyyyyyy(zzzzzzzzzzzzz[0]) == 'aaaaaaaaaaa' and
              xxxxxxxxxxxx.yyyyyyyy(zzzzzzzzzzzzz[0].mmmmmmmm[0]) == 'bbbbbbb'):
            pass


        def f(  # Intermediate comment
        ):
          if (xxxxxxxxxxxx.yyyyyyyy(zzzzzzzzzzzzz[0]) == 'aaaaaaaaaaa' and
              xxxxxxxxxxxx.yyyyyyyy(zzzzzzzzzzzzz[0].mmmmmmmm[0]) == 'bbbbbbb'):
            pass
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testBlankLinesAtEndOfFile(self):
    unformatted_code = textwrap.dedent("""\
        def foobar(): # foo
         pass



        """)
    expected_formatted_code = textwrap.dedent("""\
        def foobar():  # foo
          pass
    """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

    unformatted_code = textwrap.dedent("""\
        x = {  'a':37,'b':42,

        'c':927}

        """)
    expected_formatted_code = textwrap.dedent("""\
        x = {'a': 37, 'b': 42, 'c': 927}
    """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testMultipleUgliness(self):
    unformatted_code = textwrap.dedent("""\
        x = {  'a':37,'b':42,

        'c':927}

        y = 'hello ''world'
        z = 'hello '+'world'
        a = 'hello {}'.format('world')
        class foo  (     object  ):
          def f    (self   ):
            return       37*-+2
          def g(self, x,y=42):
              return y
        def f  (   a ) :
          return      37+-+a[42-x :  y**3]
        """)
    expected_formatted_code = textwrap.dedent("""\
        x = {'a': 37, 'b': 42, 'c': 927}

        y = 'hello ' 'world'
        z = 'hello ' + 'world'
        a = 'hello {}'.format('world')


        class foo(object):

          def f(self):
            return 37 * -+2

          def g(self, x, y=42):
            return y


        def f(a):
          return 37 + -+a[42 - x:y**3]
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testComments(self):
    unformatted_code = textwrap.dedent("""\
        class Foo(object):
          pass

        # Attached comment
        class Bar(object):
          pass

        global_assignment = 42

        # Comment attached to class with decorator.
        # Comment attached to class with decorator.
        @noop
        @noop
        class Baz(object):
          pass

        # Intermediate comment

        class Qux(object):
          pass
        """)
    expected_formatted_code = textwrap.dedent("""\
        class Foo(object):
          pass


        # Attached comment
        class Bar(object):
          pass


        global_assignment = 42


        # Comment attached to class with decorator.
        # Comment attached to class with decorator.
        @noop
        @noop
        class Baz(object):
          pass


        # Intermediate comment


        class Qux(object):
          pass
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testSingleComment(self):
    code = textwrap.dedent("""\
        # Thing 1
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testCommentsWithTrailingSpaces(self):
    unformatted_code = textwrap.dedent("""\
        # Thing 1    
        # Thing 2    
        """)
    expected_formatted_code = textwrap.dedent("""\
        # Thing 1
        # Thing 2
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testCommentsInDataLiteral(self):
    code = textwrap.dedent("""\
        def f():
          return collections.OrderedDict({
              # First comment.
              'fnord': 37,

              # Second comment.
              # Continuation of second comment.
              'bork': 42,

              # Ending comment.
          })
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testEndingWhitespaceAfterSimpleStatement(self):
    code = textwrap.dedent("""\
        import foo as bar
        # Thing 1
        # Thing 2
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testDocstrings(self):
    unformatted_code = textwrap.dedent('''\
        u"""Module-level docstring."""
        import os
        class Foo(object):

          """Class-level docstring."""
          # A comment for qux.
          def qux(self):


            """Function-level docstring.

            A multiline function docstring.
            """
            print('hello {}'.format('world'))
            return 42
        ''')
    expected_formatted_code = textwrap.dedent('''\
        u"""Module-level docstring."""
        import os


        class Foo(object):
          """Class-level docstring."""

          # A comment for qux.
          def qux(self):
            """Function-level docstring.

            A multiline function docstring.
            """
            print('hello {}'.format('world'))
            return 42
        ''')
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testDocstringAndMultilineComment(self):
    unformatted_code = textwrap.dedent('''\
        """Hello world"""
        # A multiline
        # comment
        class bar(object):
          """class docstring"""
          # class multiline
          # comment
          def foo(self):
            """Another docstring."""
            # Another multiline
            # comment
            pass
        ''')
    expected_formatted_code = textwrap.dedent('''\
        """Hello world"""


        # A multiline
        # comment
        class bar(object):
          """class docstring"""

          # class multiline
          # comment
          def foo(self):
            """Another docstring."""
            # Another multiline
            # comment
            pass
        ''')
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testMultilineDocstringAndMultilineComment(self):
    unformatted_code = textwrap.dedent('''\
        """Hello world

        RIP Dennis Richie.
        """
        # A multiline
        # comment
        class bar(object):
          """class docstring

          A classy class.
          """
          # class multiline
          # comment
          def foo(self):
            """Another docstring.

            A functional function.
            """
            # Another multiline
            # comment
            pass
        ''')
    expected_formatted_code = textwrap.dedent('''\
        """Hello world

        RIP Dennis Richie.
        """


        # A multiline
        # comment
        class bar(object):
          """class docstring

          A classy class.
          """

          # class multiline
          # comment
          def foo(self):
            """Another docstring.

            A functional function.
            """
            # Another multiline
            # comment
            pass
        ''')
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testTupleCommaBeforeLastParen(self):
    unformatted_code = textwrap.dedent("""\
        a = ( 1, )
        """)
    expected_formatted_code = textwrap.dedent("""\
        a = (1,)
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testNoBreakOutsideOfBracket(self):
    # FIXME(morbo): How this is formatted is not correct. But it's syntactically
    # correct.
    unformatted_code = textwrap.dedent("""\
        def f():
          assert port >= minimum, \
'Unexpected port %d when minimum was %d.' % (port, minimum)
        """)
    expected_formatted_code = textwrap.dedent("""\
        def f():
          assert port >= minimum, 'Unexpected port %d when minimum was %d.' % (port,
                                                                               minimum)
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testBlankLinesBeforeDecorators(self):
    unformatted_code = textwrap.dedent("""\
        @foo()
        class A(object):
          @bar()
          @baz()
          def x(self):
            pass
        """)
    expected_formatted_code = textwrap.dedent("""\
        @foo()
        class A(object):

          @bar()
          @baz()
          def x(self):
            pass
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testCommentBetweenDecorators(self):
    unformatted_code = textwrap.dedent("""\
        @foo()
        # frob
        @bar
        def x  (self):
            pass
        """)
    expected_formatted_code = textwrap.dedent("""\
        @foo()
        # frob
        @bar
        def x(self):
          pass
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testListComprehension(self):
    unformatted_code = textwrap.dedent("""\
        def given(y):
            [k for k in ()
              if k in y]
        """)
    expected_formatted_code = textwrap.dedent("""\
        def given(y):
          [k for k in () if k in y]
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testListComprehensionPreferOneLine(self):
    unformatted_code = textwrap.dedent("""\
        def given(y):
            long_variable_name = [
                long_var_name + 1
                for long_var_name in ()
                if long_var_name == 2]
        """)
    expected_formatted_code = textwrap.dedent("""\
        def given(y):
          long_variable_name = [
              long_var_name + 1 for long_var_name in () if long_var_name == 2
          ]
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testListComprehensionPreferOneLineOverArithmeticSplit(self):
    unformatted_code = textwrap.dedent("""\
        def given(used_identifiers):
          return (sum(len(identifier)
                      for identifier in used_identifiers) / len(used_identifiers))
        """)
    expected_formatted_code = textwrap.dedent("""\
        def given(used_identifiers):
          return (sum(len(identifier) for identifier in used_identifiers) /
                  len(used_identifiers))
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testListComprehensionPreferThreeLinesForLineWrap(self):
    unformatted_code = textwrap.dedent("""\
        def given(y):
            long_variable_name = [
                long_var_name + 1
                for long_var_name, number_two in ()
                if long_var_name == 2 and number_two == 3]
        """)
    expected_formatted_code = textwrap.dedent("""\
        def given(y):
          long_variable_name = [
              long_var_name + 1
              for long_var_name, number_two in ()
              if long_var_name == 2 and number_two == 3
          ]
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testListComprehensionPreferNoBreakForTrivialExpression(self):
    unformatted_code = textwrap.dedent("""\
        def given(y):
            long_variable_name = [
                long_var_name
                for long_var_name, number_two in ()
                if long_var_name == 2 and number_two == 3]
        """)
    expected_formatted_code = textwrap.dedent("""\
        def given(y):
          long_variable_name = [
              long_var_name for long_var_name, number_two in ()
              if long_var_name == 2 and number_two == 3
          ]
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testOpeningAndClosingBrackets(self):
    unformatted_code = """\
foo( (1, ) )
foo( ( 1, 2, 3  ) )
foo( ( 1, 2, 3, ) )
"""
    expected_formatted_code = """\
foo((1,))
foo((1, 2, 3))
foo((
    1,
    2,
    3,
))
"""
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testSingleLineFunctions(self):
    unformatted_code = textwrap.dedent("""\
        def foo():  return 42
        """)
    expected_formatted_code = textwrap.dedent("""\
        def foo():
          return 42
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testNoQueueSeletionInMiddleOfLine(self):
    # If the queue isn't properly constructed, then a token in the middle of the
    # line may be selected as the one with least penalty. The tokens after that
    # one are then splatted at the end of the line with no formatting.
    unformatted_code = """\
find_symbol(node.type) + "< " + " ".join(find_pattern(n) for n in node.child) + " >"
"""
    expected_formatted_code = """\
find_symbol(node.type) + "< " + " ".join(
    find_pattern(n) for n in node.child) + " >"
"""
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testNoSpacesBetweenSubscriptsAndCalls(self):
    unformatted_code = textwrap.dedent("""\
        aaaaaaaaaa = bbbbbbbb.ccccccccc() [42] (a, 2)
        """)
    expected_formatted_code = textwrap.dedent("""\
        aaaaaaaaaa = bbbbbbbb.ccccccccc()[42](a, 2)
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testNoSpacesBetweenOpeningBracketAndStartingOperator(self):
    # Unary operator.
    unformatted_code = textwrap.dedent("""\
        aaaaaaaaaa = bbbbbbbb.ccccccccc[ -1 ]( -42 )
        """)
    expected_formatted_code = textwrap.dedent("""\
        aaaaaaaaaa = bbbbbbbb.ccccccccc[-1](-42)
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

    # Varargs and kwargs.
    unformatted_code = textwrap.dedent("""\
        aaaaaaaaaa = bbbbbbbb.ccccccccc( *varargs )
        aaaaaaaaaa = bbbbbbbb.ccccccccc( **kwargs )
        """)
    expected_formatted_code = textwrap.dedent("""\
        aaaaaaaaaa = bbbbbbbb.ccccccccc(*varargs)
        aaaaaaaaaa = bbbbbbbb.ccccccccc(**kwargs)
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testMultilineCommentReformatted(self):
    unformatted_code = textwrap.dedent("""\
        if True:
            # This is a multiline
            # comment.
            pass
        """)
    expected_formatted_code = textwrap.dedent("""\
        if True:
          # This is a multiline
          # comment.
          pass
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testDictionaryMakerFormatting(self):
    unformatted_code = textwrap.dedent("""\
        _PYTHON_STATEMENTS = frozenset({
            lambda x, y: 'simple_stmt': 'small_stmt', 'expr_stmt': 'print_stmt', 'del_stmt':
            'pass_stmt', lambda: 'break_stmt': 'continue_stmt', 'return_stmt': 'raise_stmt',
            'yield_stmt': 'import_stmt', lambda: 'global_stmt': 'exec_stmt', 'assert_stmt':
            'if_stmt', 'while_stmt': 'for_stmt',
        })
        """)
    expected_formatted_code = textwrap.dedent("""\
        _PYTHON_STATEMENTS = frozenset({
            lambda x, y: 'simple_stmt': 'small_stmt',
            'expr_stmt': 'print_stmt',
            'del_stmt': 'pass_stmt',
            lambda: 'break_stmt': 'continue_stmt',
            'return_stmt': 'raise_stmt',
            'yield_stmt': 'import_stmt',
            lambda: 'global_stmt': 'exec_stmt',
            'assert_stmt': 'if_stmt',
            'while_stmt': 'for_stmt',
        })
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testSimpleMultilineCode(self):
    unformatted_code = textwrap.dedent("""\
        if True:
          aaaaaaaaaaaaaa.bbbbbbbbbbbbbb.ccccccc(zzzzzzzzzzzz, \
xxxxxxxxxxx, yyyyyyyyyyyy, vvvvvvvvv)
          aaaaaaaaaaaaaa.bbbbbbbbbbbbbb.ccccccc(zzzzzzzzzzzz, \
xxxxxxxxxxx, yyyyyyyyyyyy, vvvvvvvvv)
        """)
    expected_formatted_code = textwrap.dedent("""\
        if True:
          aaaaaaaaaaaaaa.bbbbbbbbbbbbbb.ccccccc(zzzzzzzzzzzz, xxxxxxxxxxx, yyyyyyyyyyyy,
                                                vvvvvvvvv)
          aaaaaaaaaaaaaa.bbbbbbbbbbbbbb.ccccccc(zzzzzzzzzzzz, xxxxxxxxxxx, yyyyyyyyyyyy,
                                                vvvvvvvvv)
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testMultilineComment(self):
    code = textwrap.dedent("""\
        if Foo:
          # Hello world
          # Yo man.
          # Yo man.
          # Yo man.
          # Yo man.
          a = 42
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testMultilineString(self):
    code = textwrap.dedent("""\
        code = textwrap.dedent('''\
            if Foo:
              # Hello world
              # Yo man.
              # Yo man.
              # Yo man.
              # Yo man.
              a = 42
            ''')
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

    unformatted_code = textwrap.dedent('''\
        def f():
            email_text += """<html>This is a really long docstring that goes over the column limit and is multi-line.<br><br>
        <b>Czar: </b>"""+despot["Nicholas"]+"""<br>
        <b>Minion: </b>"""+serf["Dmitri"]+"""<br>
        <b>Residence: </b>"""+palace["Winter"]+"""<br>
        </body>
        </html>"""
        ''')
    expected_formatted_code = textwrap.dedent('''\
        def f():
          email_text += """<html>This is a really long docstring that goes over the column limit and is multi-line.<br><br>
        <b>Czar: </b>""" + despot["Nicholas"] + """<br>
        <b>Minion: </b>""" + serf["Dmitri"] + """<br>
        <b>Residence: </b>""" + palace["Winter"] + """<br>
        </body>
        </html>"""
        ''')
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testSimpleMultilineWithComments(self):
    code = textwrap.dedent("""\
        if (  # This is the first comment
            a and  # This is the second comment
            # This is the third comment
            b):  # A trailing comment
          # Whoa! A normal comment!!
          pass  # Another trailing comment
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testMatchingParenSplittingMatching(self):
    unformatted_code = textwrap.dedent("""\
        def f():
          raise RuntimeError('unable to find insertion point for target node',
                             (target,))
        """)
    expected_formatted_code = textwrap.dedent("""\
        def f():
          raise RuntimeError('unable to find insertion point for target node',
                             (target,))
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testContinuationIndent(self):
    unformatted_code = textwrap.dedent('''\
        class F:
          def _ProcessArgLists(self, node):
            """Common method for processing argument lists."""
            for child in node.children:
              if isinstance(child, pytree.Leaf):
                self._SetTokenSubtype(
                    child, subtype=_ARGLIST_TOKEN_TO_SUBTYPE.get(
                        child.value, format_token.Subtype.NONE))
        ''')
    expected_formatted_code = textwrap.dedent('''\
        class F:

          def _ProcessArgLists(self, node):
            """Common method for processing argument lists."""
            for child in node.children:
              if isinstance(child, pytree.Leaf):
                self._SetTokenSubtype(
                    child,
                    subtype=_ARGLIST_TOKEN_TO_SUBTYPE.get(child.value,
                                                          format_token.Subtype.NONE))
        ''')
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testTrailingCommaAndBracket(self):
    unformatted_code = textwrap.dedent('''\
        a = { 42, }
        b = ( 42, )
        c = [ 42, ]
        ''')
    expected_formatted_code = textwrap.dedent('''\
        a = {
            42,
        }
        b = (42,)
        c = [
            42,
        ]
        ''')
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testI18n(self):
    code = textwrap.dedent("""\
        N_('Some years ago - never mind how long precisely - having little or no money in my purse, and nothing particular to interest me on shore, I thought I would sail about a little and see the watery part of the world.')  # A comment is here.
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

    code = textwrap.dedent("""\
        foo('Fake function call')  #. Some years ago - never mind how long precisely - having little or no money in my purse, and nothing particular to interest me on shore, I thought I would sail about a little and see the watery part of the world.
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testI18nCommentsInDataLiteral(self):
    code = textwrap.dedent("""\
        def f():
          return collections.OrderedDict({
              #. First i18n comment.
              'bork': 'foo',

              #. Second i18n comment.
              'snork': 'bar#.*=\\\\0',
          })
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testClosingBracketIndent(self):
    code = textwrap.dedent('''\
        def f():

          def g():
            while (xxxxxxxxxxxxxxxxxxxxx(yyyyyyyyyyyyy[zzzzz]) == 'aaaaaaaaaaa' and
                   xxxxxxxxxxxxxxxxxxxxx(
                       yyyyyyyyyyyyy[zzzzz].aaaaaaaa[0]) == 'bbbbbbb'):
              pass
        ''')
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testClosingBracketsInlinedInCall(self):
    unformatted_code = textwrap.dedent("""\
        class Foo(object):

          def bar(self):
            self.aaaaaaaa = xxxxxxxxxxxxxxxxxxx.yyyyyyyyyyyyy(
                self.cccccc.ddddddddd.eeeeeeee,
                options={
                    "forkforkfork": 1,
                    "borkborkbork": 2,
                    "corkcorkcork": 3,
                    "horkhorkhork": 4,
                    "porkporkpork": 5,
                    })
        """)
    expected_formatted_code = textwrap.dedent("""\
        class Foo(object):

          def bar(self):
            self.aaaaaaaa = xxxxxxxxxxxxxxxxxxx.yyyyyyyyyyyyy(
                self.cccccc.ddddddddd.eeeeeeee,
                options={
                    "forkforkfork": 1,
                    "borkborkbork": 2,
                    "corkcorkcork": 3,
                    "horkhorkhork": 4,
                    "porkporkpork": 5,
                })
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testLineWrapInForExpression(self):
    code = textwrap.dedent("""\
        class A:

          def x(self, node, name, n=1):
            for i, child in enumerate(
                itertools.ifilter(lambda c: pytree_utils.NodeName(c) == name,
                                  node.pre_order())):
              pass
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testFunctionCallContinuationLine(self):
    code = """\
class foo:

  def bar(self, node, name, n=1):
    if True:
      if True:
        return [(aaaaaaaaaa,
                 bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb(
                     cccc, ddddddddddddddddddddddddddddddddddddd))]
"""
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testI18nNonFormatting(self):
    code = textwrap.dedent("""\
        class F(object):

          def __init__(self, fieldname,
                       #. Error message indicating an invalid e-mail address.
                       message=N_('Please check your email address.'), **kwargs):
            pass
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testNoSpaceBetweenUnaryOpAndOpeningParen(self):
    code = textwrap.dedent("""\
        if ~(a or b):
          pass
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testCommentBeforeFuncDef(self):
    code = textwrap.dedent("""\
        class Foo(object):

          a = 42

          # This is a comment.
          def __init__(self,
                       xxxxxxx,
                       yyyyy=0,
                       zzzzzzz=None,
                       aaaaaaaaaaaaaaaaaa=False,
                       bbbbbbbbbbbbbbb=False):
            pass
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testExcessLineCountWithDefaultKeywords(self):
    unformatted_code = textwrap.dedent("""\
        class Fnord(object):
          def Moo(self):
            aaaaaaaaaaaaaaaa = self._bbbbbbbbbbbbbbbbbbbbbbb(
                ccccccccccccc=ccccccccccccc, ddddddd=ddddddd, eeee=eeee,
                fffff=fffff, ggggggg=ggggggg, hhhhhhhhhhhhh=hhhhhhhhhhhhh,
                iiiiiii=iiiiiiiiiiiiii)
        """)
    expected_formatted_code = textwrap.dedent("""\
        class Fnord(object):

          def Moo(self):
            aaaaaaaaaaaaaaaa = self._bbbbbbbbbbbbbbbbbbbbbbb(
                ccccccccccccc=ccccccccccccc,
                ddddddd=ddddddd,
                eeee=eeee,
                fffff=fffff,
                ggggggg=ggggggg,
                hhhhhhhhhhhhh=hhhhhhhhhhhhh,
                iiiiiii=iiiiiiiiiiiiii)
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testSpaceAfterNotOperator(self):
    code = textwrap.dedent("""\
        if not (this and that):
          pass
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testNoPenaltySplitting(self):
    code = textwrap.dedent("""\
        def f():
          if True:
            if True:
              python_files.extend(
                  os.path.join(filename, f)
                  for f in os.listdir(filename)
                  if IsPythonFile(os.path.join(filename, f)))
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testExpressionPenalties(self):
    code = textwrap.dedent("""\
      def f():
        if ((left.value == '(' and right.value == ')') or
            (left.value == '[' and right.value == ']') or
            (left.value == '{' and right.value == '}')):
          return False
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testLineDepthOfSingleLineStatement(self):
    unformatted_code = textwrap.dedent("""\
        while True: continue
        for x in range(3): continue
        try: a = 42
        except: b = 42
        with open(a) as fd: a = fd.read()
        """)
    expected_formatted_code = textwrap.dedent("""\
        while True:
          continue
        for x in range(3):
          continue
        try:
          a = 42
        except:
          b = 42
        with open(a) as fd:
          a = fd.read()
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testSplitListWithTerminatingComma(self):
    unformatted_code = textwrap.dedent("""\
        FOO = ['bar', 'baz', 'mux', 'qux', 'quux', 'quuux', 'quuuux',
          'quuuuux', 'quuuuuux', 'quuuuuuux', lambda a, b: 37,]
        """)
    expected_formatted_code = textwrap.dedent("""\
        FOO = [
            'bar',
            'baz',
            'mux',
            'qux',
            'quux',
            'quuux',
            'quuuux',
            'quuuuux',
            'quuuuuux',
            'quuuuuuux',
            lambda a, b: 37,
        ]
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testSplitListWithInterspersedComments(self):
    code = textwrap.dedent("""\
        FOO = [
            'bar',  # bar
            'baz',  # baz
            'mux',  # mux
            'qux',  # qux
            'quux',  # quux
            'quuux',  # quuux
            'quuuux',  # quuuux
            'quuuuux',  # quuuuux
            'quuuuuux',  # quuuuuux
            'quuuuuuux',  # quuuuuuux
            lambda a, b: 37  # lambda
        ]
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testRelativeImportStatements(self):
    code = textwrap.dedent("""\
        from ... import bork
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testSingleLineList(self):
    # A list on a single line should prefer to remain contiguous.
    unformatted_code = textwrap.dedent("""\
        bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb = aaaaaaaaaaa(
            ("...", "."), "..",
            ".............................................."
        )
        """)
    expected_formatted_code = textwrap.dedent("""\
        bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb = aaaaaaaaaaa(
            ("...", "."), "..", "..............................................")
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testBlankLinesBeforeFunctionsNotInColumnZero(self):
    unformatted_code = textwrap.dedent("""\
        import signal


        try:
          signal.SIGALRM
          # ..................................................................
          # ...............................................................


          def timeout(seconds=1):
            pass
        except:
          pass
        """)
    expected_formatted_code = textwrap.dedent("""\
        import signal

        try:
          signal.SIGALRM

          # ..................................................................
          # ...............................................................


          def timeout(seconds=1):
            pass
        except:
          pass
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testNoKeywordArgumentBreakage(self):
    code = textwrap.dedent("""\
        class A(object):

          def b(self):
            if self.aaaaaaaaaaaaaaaaaaaa not in self.bbbbbbbbbb(
                cccccccccccccccccccc=True):
              pass
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testTrailerOnSingleLine(self):
    code = """\
urlpatterns = patterns('', url(r'^$', 'homepage_view'),
                       url(r'^/login/$', 'login_view'),
                       url(r'^/login/$', 'logout_view'),
                       url(r'^/user/(?P<username>\\w+)/$', 'profile_view'))
"""
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testIfConditionalParens(self):
    code = textwrap.dedent("""\
        class Foo:

          def bar():
            if True:
              if (child.type == grammar_token.NAME and
                  child.value in substatement_names):
                pass
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testContinuationMarkers(self):
    code = textwrap.dedent("""\
        text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec a diam lectus. "\\
               "Sed sit amet ipsum mauris. Maecenas congue ligula ac quam viverra nec consectetur "\\
               "ante hendrerit. Donec et mollis dolor. Praesent et diam eget libero egestas mattis "\\
               "sit amet vitae augue. Nam tincidunt congue enim, ut porta lorem lacinia consectetur. "\\
               "Donec ut libero sed arcu vehicula ultricies a non tortor. Lorem ipsum dolor sit amet"
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

    code = textwrap.dedent("""\
        from __future__ import nested_scopes, generators, division, absolute_import, with_statement, \\
            print_function, unicode_literals
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

    code = textwrap.dedent("""\
        if aaaaaaaaa == 42 and bbbbbbbbbbbbbb == 42 and \\
           cccccccc == 42:
          pass
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testCommentsWithContinuationMarkers(self):
    code = textwrap.dedent("""\
        def fn(arg):
          v = fn2(key1=True,
                  #c1
                  key2=arg)\\
                        .fn3()
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testMultipleContinuationMarkers(self):
    code = textwrap.dedent("""\
        xyz = \\
            \\
            some_thing()
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testContinuationMarkerAfterStringWithContinuation(self):
    code = """\
s = 'foo \\
    bar' \\
    .format()
"""
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testEmptyContainers(self):
    code = textwrap.dedent("""\
        flags.DEFINE_list(
            'output_dirs', [],
            'Lorem ipsum dolor sit amet, consetetur adipiscing elit. Donec a diam lectus. '
            'Sed sit amet ipsum mauris. Maecenas congue.')
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testSplitStringsIfSurroundedByParens(self):
    unformatted_code = textwrap.dedent("""\
        a = foo.bar({'xxxxxxxxxxxxxxxxxxxxxxx' 'yyyyyyyyyyyyyyyyyyyyyyyyyy': baz[42]} + 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa' 'bbbbbbbbbbbbbbbbbbbbbbbbbb' 'cccccccccccccccccccccccccccccccc' 'ddddddddddddddddddddddddddddd')
        """)
    expected_formatted_code = textwrap.dedent("""\
        a = foo.bar({
            'xxxxxxxxxxxxxxxxxxxxxxx'
            'yyyyyyyyyyyyyyyyyyyyyyyyyy': baz[42]
        } + 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
                    'bbbbbbbbbbbbbbbbbbbbbbbbbb'
                    'cccccccccccccccccccccccccccccccc'
                    'ddddddddddddddddddddddddddddd')
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

    code = textwrap.dedent("""\
        a = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa' \
'bbbbbbbbbbbbbbbbbbbbbbbbbb' 'cccccccccccccccccccccccccccccccc' \
'ddddddddddddddddddddddddddddd'
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testMultilineShebang(self):
    code = textwrap.dedent("""\
        #!/bin/sh
        if "true" : '''\'
        then

        export FOO=123
        exec /usr/bin/env python "$0" "$@"

        exit 127
        fi
        '''

        import os

        assert os.environ['FOO'] == '123'
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testNoSplittingAroundTermOperators(self):
    code = textwrap.dedent("""\
        a_very_long_function_call_yada_yada_etc_etc_etc(long_arg1,
                                                        long_arg2 / long_arg3)
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testNoSplittingWithinSubscriptList(self):
    code = textwrap.dedent("""\
        somequitelongvariablename.somemember[(a, b)] = {
            'somelongkey': 1,
            'someotherlongkey': 2
        }
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testExcessCharacters(self):
    code = textwrap.dedent("""\
        class foo:

          def bar(self):
            self.write(s=[
                '%s%s %s' % ('many of really', 'long strings', '+ just makes up 81')
            ])
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

    unformatted_code = textwrap.dedent("""\
        def _():
          if True:
            if True:
              if contract == allow_contract and attr_dict.get(if_attribute) == has_value:
                return True
        """)
    expected_code = textwrap.dedent("""\
        def _():
          if True:
            if True:
              if contract == allow_contract and attr_dict.get(
                  if_attribute) == has_value:
                return True
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertEqual(expected_code, reformatter.Reformat(uwlines))

  def testDictSetGenerator(self):
    code = textwrap.dedent("""\
        foo = {
            variable: 'hello world. How are you today?'
            for variable in fnord
            if variable != 37
        }
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testUnaryOpInDictionaryValue(self):
    code = textwrap.dedent("""\
        beta = "123"

        test = {'alpha': beta[-1]}

        print(beta[-1])
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testUnaryNotOperator(self):
    code = textwrap.dedent("""\
        if True:
          if True:
            if True:
              if True:
                remote_checksum = self.get_checksum(conn, tmp, dest, inject,
                                                    not directory_prepended, source)
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testRelaxArraySubscriptAffinity(self):
    code = textwrap.dedent("""\
        class A(object):

          def f(self, aaaaaaaaa, bbbbbbbbbbbbb, row):
            if True:
              if True:
                if True:
                  if True:
                    if row[4] is None or row[5] is None:
                      bbbbbbbbbbbbb['..............'] = row[
                          5] if row[5] is not None else 5
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testFunctionCallInDict(self):
    code = "a = {'a': b(c=d, **e)}\n"
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testFunctionCallInNestedDict(self):
    code = "a = {'a': {'a': {'a': b(c=d, **e)}}}\n"
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testUnbreakableNot(self):
    code = textwrap.dedent("""\
        def test():
          if not "Foooooooooooooooooooooooooooooo" or "Foooooooooooooooooooooooooooooo" == "Foooooooooooooooooooooooooooooo":
            pass
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testSplitListWithComment(self):
    code = textwrap.dedent("""\
      a = [
          'a',
          'b',
          'c'  # hello world
      ]
      """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testOverColumnLimit(self):
    unformatted_code = textwrap.dedent("""\
      class Test:

        def testSomething(self):
          expected = {
              ('aaaaaaaaaaaaa', 'bbbb'): 'ccccccccccccccccccccccccccccccccccccccccccc',
              ('aaaaaaaaaaaaa', 'bbbb'): 'ccccccccccccccccccccccccccccccccccccccccccc',
              ('aaaaaaaaaaaaa', 'bbbb'): 'ccccccccccccccccccccccccccccccccccccccccccc',
          }
        """)
    expected_formatted_code = textwrap.dedent("""\
      class Test:

        def testSomething(self):
          expected = {
              ('aaaaaaaaaaaaa', 'bbbb'):
                  'ccccccccccccccccccccccccccccccccccccccccccc',
              ('aaaaaaaaaaaaa', 'bbbb'):
                  'ccccccccccccccccccccccccccccccccccccccccccc',
              ('aaaaaaaaaaaaa', 'bbbb'):
                  'ccccccccccccccccccccccccccccccccccccccccccc',
          }
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testEndingComment(self):
    code = textwrap.dedent("""\
      a = f(
          a="something",
          b="something requiring comment which is quite long",  # comment about b (pushes line over 79)
          c="something else, about which comment doesn't make sense")
      """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testContinuationSpaceRetention(self):
    code = textwrap.dedent("""\
      def fn():
        return module \\
               .method(Object(data,
                   fn2(arg)
               ))
      """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testIfExpressionWithFunctionCall(self):
    code = textwrap.dedent("""\
      if x or z.y(
          a,
          c,
          aaaaaaaaaaaaaaaaaaaaa=aaaaaaaaaaaaaaaaaa,
          bbbbbbbbbbbbbbbbbbbbb=bbbbbbbbbbbbbbbbbb):
        pass
      """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testUnformattedAfterMultilineString(self):
    code = textwrap.dedent("""\
      def foo():
        com_text = \\
      '''
      TEST
      ''' % (input_fname, output_fname)
      """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testNoSpacesAroundKeywordDefaultValues(self):
    code = textwrap.dedent("""\
      sources = {
          'json': request.get_json(silent=True) or {},
          'json2': request.get_json(silent=True),
      }
      json = request.get_json(silent=True) or {}
      """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testNoSplittingBeforeEndingSubscriptBracket(self):
    unformatted_code = textwrap.dedent("""\
        if True:
          if True:
            status = cf.describe_stacks(StackName=stackname)[u'Stacks'][0][u'StackStatus']
        """)
    expected_formatted_code = textwrap.dedent("""\
        if True:
          if True:
            status = cf.describe_stacks(
                StackName=stackname)[u'Stacks'][0][u'StackStatus']
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testNoSplittingOnSingleArgument(self):
    unformatted_code = textwrap.dedent("""\
        xxxxxxxxxxxxxx = (re.search(r'(\\d+\\.\\d+\\.\\d+\\.)\\d+',
                                    aaaaaaa.bbbbbbbbbbbb).group(1) +
                          re.search(r'\\d+\\.\\d+\\.\\d+\\.(\\d+)',
                                    ccccccc).group(1))
        xxxxxxxxxxxxxx = (re.search(r'(\\d+\\.\\d+\\.\\d+\\.)\\d+',
                                    aaaaaaa.bbbbbbbbbbbb).group(a.b) +
                          re.search(r'\\d+\\.\\d+\\.\\d+\\.(\\d+)',
                                    ccccccc).group(c.d))
        """)
    expected_formatted_code = textwrap.dedent("""\
        xxxxxxxxxxxxxx = (
            re.search(r'(\\d+\\.\\d+\\.\\d+\\.)\\d+', aaaaaaa.bbbbbbbbbbbb).group(1) +
            re.search(r'\\d+\\.\\d+\\.\\d+\\.(\\d+)', ccccccc).group(1))
        xxxxxxxxxxxxxx = (
            re.search(r'(\\d+\\.\\d+\\.\\d+\\.)\\d+', aaaaaaa.bbbbbbbbbbbb).group(a.b) +
            re.search(r'\\d+\\.\\d+\\.\\d+\\.(\\d+)', ccccccc).group(c.d))
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testSplittingArraysSensibly(self):
    unformatted_code = textwrap.dedent("""\
        while True:
          while True:
            aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa = list['bbbbbbbbbbbbbbbbbbbbbbbbb'].split(',')
            aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa = list('bbbbbbbbbbbbbbbbbbbbbbbbb').split(',')
        """)
    expected_formatted_code = textwrap.dedent("""\
        while True:
          while True:
            aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa = list[
                'bbbbbbbbbbbbbbbbbbbbbbbbb'].split(',')
            aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa = list(
                'bbbbbbbbbbbbbbbbbbbbbbbbb').split(',')
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testComprehensionForAndIf(self):
    unformatted_code = textwrap.dedent("""\
        class f:

          def __repr__(self):
            tokens_repr = ','.join(['{0}({1!r})'.format(tok.name, tok.value) for tok in self._tokens])
        """)
    expected_formatted_code = textwrap.dedent("""\
        class f:

          def __repr__(self):
            tokens_repr = ','.join(
                ['{0}({1!r})'.format(tok.name, tok.value) for tok in self._tokens])
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testFunctionCallArguments(self):
    unformatted_code = textwrap.dedent("""\
        def f():
          if True:
            pytree_utils.InsertNodesBefore(_CreateCommentsFromPrefix(
                comment_prefix, comment_lineno, comment_column,
                standalone=True), ancestor_at_indent)
            pytree_utils.InsertNodesBefore(_CreateCommentsFromPrefix(
                comment_prefix, comment_lineno, comment_column,
                standalone=True))
        """)
    expected_formatted_code = textwrap.dedent("""\
        def f():
          if True:
            pytree_utils.InsertNodesBefore(
                _CreateCommentsFromPrefix(
                    comment_prefix, comment_lineno, comment_column, standalone=True),
                ancestor_at_indent)
            pytree_utils.InsertNodesBefore(
                _CreateCommentsFromPrefix(
                    comment_prefix, comment_lineno, comment_column, standalone=True))
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testBinaryOperators(self):
    unformatted_code = textwrap.dedent("""\
        a = b ** 37
        c = (20 ** -3) / (_GRID_ROWS ** (code_length - 10))
        """)
    expected_formatted_code = textwrap.dedent("""\
        a = b**37
        c = (20**-3) / (_GRID_ROWS**(code_length - 10))
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

    code = textwrap.dedent("""\
      def f():
        if True:
          if (self.stack[-1].split_before_closing_bracket and
              # FIXME(morbo): Use the 'matching_bracket' instead of this.
              # FIXME(morbo): Don't forget about tuples!
              current.value in ']}'):
            pass
      """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testContiguousList(self):
    code = textwrap.dedent("""\
      [retval1, retval2] = a_very_long_function(argument_1, argument2, argument_3,
                                                argument_4)
      """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testArgsAndKwargsFormatting(self):
    code = textwrap.dedent("""\
      a(a=aaaaaaaaaaaaaaaaaaaaa,
        b=aaaaaaaaaaaaaaaaaaaaaaaa,
        c=aaaaaaaaaaaaaaaaaa,
        *d,
        **e)
      """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

    code = textwrap.dedent("""\
      def foo():
        return [
            Bar(xxx='some string',
                yyy='another long string',
                zzz='a third long string')
        ]
      """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testCommentColumnLimitOverflow(self):
    code = textwrap.dedent("""\
      def f():
        if True:
          TaskManager.get_tags = MagicMock(
              name='get_tags_mock',
              return_value=[157031694470475],
              # side_effect=[(157031694470475), (157031694470475),],
          )
      """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testMultilineLambdas(self):
    try:
      style.SetGlobalStyle(
          style.CreateStyleFromConfig(
              '{based_on_style: chromium, allow_multiline_lambdas: true}'))
      unformatted_code = textwrap.dedent("""\
          class SomeClass(object):
            do_something = True

            def succeeded(self, dddddddddddddd):
              d = defer.succeed(None)

              if self.do_something:
                d.addCallback(lambda _: self.aaaaaa.bbbbbbbbbbbbbbbb.cccccccccccccccccccccccccccccccc(dddddddddddddd))
              return d
          """)
      expected_formatted_code = textwrap.dedent("""\
          class SomeClass(object):
            do_something = True

            def succeeded(self, dddddddddddddd):
              d = defer.succeed(None)

              if self.do_something:
                d.addCallback(lambda _: self.aaaaaa.bbbbbbbbbbbbbbbb.
                              cccccccccccccccccccccccccccccccc(dddddddddddddd))
              return d
          """)
      uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
      self.assertCodeEqual(expected_formatted_code,
                           reformatter.Reformat(uwlines))
    finally:
      style.SetGlobalStyle(style.CreateChromiumStyle())

  def testMultilineDictionaryKeys(self):
    try:
      style.SetGlobalStyle(
          style.CreateStyleFromConfig('{based_on_style: chromium, '
                                      'allow_multiline_dictionary_keys: true}'))
      unformatted_code = textwrap.dedent("""\
          MAP_WITH_LONG_KEYS = {
              ('lorem ipsum', 'dolor sit amet'):
                  1,
              ('consectetur adipiscing elit.', 'Vestibulum mauris justo, ornare eget dolor eget'):
                  2,
              ('vehicula convallis nulla. Vestibulum dictum nisl in malesuada finibus.',):
                  3
          }
          """)
      expected_formatted_code = textwrap.dedent("""\
          MAP_WITH_LONG_KEYS = {
              ('lorem ipsum', 'dolor sit amet'):
                  1,
              ('consectetur adipiscing elit.',
               'Vestibulum mauris justo, ornare eget dolor eget'):
                  2,
              ('vehicula convallis nulla. Vestibulum dictum nisl in malesuada finibus.',):
                  3
          }
          """)
      uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
      self.assertCodeEqual(expected_formatted_code,
                           reformatter.Reformat(uwlines))
    finally:
      style.SetGlobalStyle(style.CreateChromiumStyle())

  def testStableDictionaryFormatting(self):
    try:
      style.SetGlobalStyle(
          style.CreateStyleFromConfig(
              '{based_on_style: pep8, indent_width: 2, '
              'continuation_indent_width: 4, indent_dictionary_value: True}'))
      code = textwrap.dedent("""\
          class A(object):
            def method(self):
              filters = {
                  'expressions': [{
                      'field': {
                          'search_field': {
                              'user_field': 'latest_party__number_of_guests'
                          },
                      }
                  }]
              }
          """)
      uwlines = yapf_test_helper.ParseAndUnwrap(code)
      reformatted_code = reformatter.Reformat(uwlines)
      self.assertCodeEqual(code, reformatted_code)

      uwlines = yapf_test_helper.ParseAndUnwrap(reformatted_code)
      reformatted_code = reformatter.Reformat(uwlines)
      self.assertCodeEqual(code, reformatted_code)
    finally:
      style.SetGlobalStyle(style.CreateChromiumStyle())

  def testStableInlinedDictionaryFormatting(self):
    try:
      style.SetGlobalStyle(style.CreatePEP8Style())
      unformatted_code = textwrap.dedent("""\
          def _():
              url = "http://{0}/axis-cgi/admin/param.cgi?{1}".format(
                  value, urllib.urlencode({'action': 'update', 'parameter': value}))
          """)
      expected_formatted_code = textwrap.dedent("""\
          def _():
              url = "http://{0}/axis-cgi/admin/param.cgi?{1}".format(
                  value, urllib.urlencode({
                      'action': 'update',
                      'parameter': value
                  }))
          """)

      uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
      reformatted_code = reformatter.Reformat(uwlines)
      self.assertCodeEqual(expected_formatted_code, reformatted_code)

      uwlines = yapf_test_helper.ParseAndUnwrap(reformatted_code)
      reformatted_code = reformatter.Reformat(uwlines)
      self.assertCodeEqual(expected_formatted_code, reformatted_code)
    finally:
      style.SetGlobalStyle(style.CreateChromiumStyle())

  def testDontSplitKeywordValueArguments(self):
    unformatted_code = textwrap.dedent("""\
        def mark_game_scored(gid):
          _connect.execute(_games.update().where(_games.c.gid == gid).values(
              scored=True))
        """)
    expected_formatted_code = textwrap.dedent("""\
        def mark_game_scored(gid):
          _connect.execute(
              _games.update().where(_games.c.gid == gid).values(scored=True))
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testDontAddBlankLineAfterMultilineString(self):
    code = textwrap.dedent("""\
      query = '''SELECT id 
      FROM table 
      WHERE day in {}'''
      days = ",".join(days)
      """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testFormattingListComprehensions(self):
    code = textwrap.dedent("""\
      def a():
        if True:
          if True:
            if True:
              columns = [
                  x for x, y in self._heap_this_is_very_long if x.route[0] == choice
              ]
              self._heap = [x for x in self._heap if x.route and x.route[0] == choice]
      """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testNoSplittingWhenBinPacking(self):
    try:
      style.SetGlobalStyle(
          style.CreateStyleFromConfig(
              '{based_on_style: pep8, indent_width: 2, '
              'continuation_indent_width: 4, indent_dictionary_value: True, '
              'dedent_closing_brackets: True, '
              'split_before_named_assigns: False}'))
      code = textwrap.dedent("""\
          a_very_long_function_name(
              long_argument_name_1=1,
              long_argument_name_2=2,
              long_argument_name_3=3,
              long_argument_name_4=4,
          )

          a_very_long_function_name(
              long_argument_name_1=1, long_argument_name_2=2, long_argument_name_3=3,
              long_argument_name_4=4
          )
          """)
      uwlines = yapf_test_helper.ParseAndUnwrap(code)
      reformatted_code = reformatter.Reformat(uwlines)
      self.assertCodeEqual(code, reformatted_code)

      uwlines = yapf_test_helper.ParseAndUnwrap(reformatted_code)
      reformatted_code = reformatter.Reformat(uwlines)
      self.assertCodeEqual(code, reformatted_code)
    finally:
      style.SetGlobalStyle(style.CreateChromiumStyle())

  def testNotSplittingAfterSubscript(self):
    unformatted_code = textwrap.dedent("""\
        if not aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.b(c == d[
                'eeeeee']).ffffff():
          pass
        """)
    expected_formatted_code = textwrap.dedent("""\
        if not aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.b(
            c == d['eeeeee']).ffffff():
          pass
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testSplittingOneArgumentList(self):
    unformatted_code = textwrap.dedent("""\
        def _():
          if True:
            if True:
              if True:
                if True:
                  if True:
                    boxes[id_] = np.concatenate((points.min(axis=0), qoints.max(axis=0)))
        """)
    expected_formatted_code = textwrap.dedent("""\
        def _():
          if True:
            if True:
              if True:
                if True:
                  if True:
                    boxes[id_] = np.concatenate((points.min(axis=0),
                                                 qoints.max(axis=0)))
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testSplittingBeforeFirstElementListArgument(self):
    unformatted_code = textwrap.dedent("""\
        class _():
          @classmethod
          def _pack_results_for_constraint_or(cls, combination, constraints):
            if True:
              if True:
                if True:
                  return cls._create_investigation_result(
                          (
                                  clue for clue in combination if not clue == Verifier.UNMATCHED
                          ), constraints, InvestigationResult.OR
                  )
        """)
    expected_formatted_code = textwrap.dedent("""\
        class _():

          @classmethod
          def _pack_results_for_constraint_or(cls, combination, constraints):
            if True:
              if True:
                if True:
                  return cls._create_investigation_result(
                      (clue for clue in combination if not clue == Verifier.UNMATCHED),
                      constraints, InvestigationResult.OR)
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testSplittingArgumentsTerminatedByComma(self):
    try:
      style.SetGlobalStyle(
          style.CreateStyleFromConfig(
              '{based_on_style: chromium, '
              'split_arguments_when_comma_terminated: True}'))
      unformatted_code = textwrap.dedent("""\
          function_name(argument_name_1=1, argument_name_2=2, argument_name_3=3)

          function_name(argument_name_1=1, argument_name_2=2, argument_name_3=3,)

          a_very_long_function_name(long_argument_name_1=1, long_argument_name_2=2, long_argument_name_3=3, long_argument_name_4=4)

          a_very_long_function_name(long_argument_name_1, long_argument_name_2, long_argument_name_3, long_argument_name_4,)

          r =f0 (1,  2,3,)
          """)
      expected_formatted_code = textwrap.dedent("""\
          function_name(argument_name_1=1, argument_name_2=2, argument_name_3=3)

          function_name(
              argument_name_1=1,
              argument_name_2=2,
              argument_name_3=3,
          )

          a_very_long_function_name(
              long_argument_name_1=1,
              long_argument_name_2=2,
              long_argument_name_3=3,
              long_argument_name_4=4)

          a_very_long_function_name(
              long_argument_name_1,
              long_argument_name_2,
              long_argument_name_3,
              long_argument_name_4,
          )

          r = f0(
              1,
              2,
              3,
          )
          """)
      uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
      reformatted_code = reformatter.Reformat(uwlines)
      self.assertCodeEqual(expected_formatted_code, reformatted_code)

      uwlines = yapf_test_helper.ParseAndUnwrap(reformatted_code)
      reformatted_code = reformatter.Reformat(uwlines)
      self.assertCodeEqual(expected_formatted_code, reformatted_code)
    finally:
      style.SetGlobalStyle(style.CreateChromiumStyle())

  def testImportAsList(self):
    code = textwrap.dedent("""\
        from toto import titi, tata, tutu  # noqa
        from toto import titi, tata, tutu
        from toto import (titi, tata, tutu)
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testDictionaryValuesOnOwnLines(self):
    unformatted_code = textwrap.dedent("""\
        a = {
        'aaaaaaaaaaaaaaaaaaaaaaaa':
            Check('ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ', '=', True),
        'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbb':
            Check('YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY', '=', True),
        'ccccccccccccccc':
            Check('XXXXXXXXXXXXXXXXXXX', '!=', 'SUSPENDED'),
        'dddddddddddddddddddddddddddddd':
            Check('WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW', '=', False),
        'eeeeeeeeeeeeeeeeeeeeeeeeeeeee':
            Check('VVVVVVVVVVVVVVVVVVVVVVVVVVVVVV', '=', False),
        'ffffffffffffffffffffffffff':
            Check('UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU', '=', True),
        'ggggggggggggggggg':
            Check('TTTTTTTTTTTTTTTTTTTTTTTTTTTTTT', '=', True),
        'hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh':
            Check('SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS', '=', True),
        'iiiiiiiiiiiiiiiiiiiiiiii':
            Check('RRRRRRRRRRRRRRRRRRRRRRRRRRR', '=', True),
        'jjjjjjjjjjjjjjjjjjjjjjjjjj':
            Check('QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ', '=', False),
        }
        """)
    expected_formatted_code = textwrap.dedent("""\
        a = {
            'aaaaaaaaaaaaaaaaaaaaaaaa':
                Check('ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ', '=', True),
            'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbb':
                Check('YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY', '=', True),
            'ccccccccccccccc':
                Check('XXXXXXXXXXXXXXXXXXX', '!=', 'SUSPENDED'),
            'dddddddddddddddddddddddddddddd':
                Check('WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW', '=', False),
            'eeeeeeeeeeeeeeeeeeeeeeeeeeeee':
                Check('VVVVVVVVVVVVVVVVVVVVVVVVVVVVVV', '=', False),
            'ffffffffffffffffffffffffff':
                Check('UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU', '=', True),
            'ggggggggggggggggg':
                Check('TTTTTTTTTTTTTTTTTTTTTTTTTTTTTT', '=', True),
            'hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh':
                Check('SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS', '=', True),
            'iiiiiiiiiiiiiiiiiiiiiiii':
                Check('RRRRRRRRRRRRRRRRRRRRRRRRRRR', '=', True),
            'jjjjjjjjjjjjjjjjjjjjjjjjjj':
                Check('QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ', '=', False),
        }
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testDictionaryOnOwnLine(self):
    unformatted_code = textwrap.dedent("""\
        doc = test_utils.CreateTestDocumentViaController(
            content={ 'a': 'b' },
            branch_key=branch.key,
            collection_key=collection.key)
        """)
    expected_formatted_code = textwrap.dedent("""\
        doc = test_utils.CreateTestDocumentViaController(
            content={'a': 'b'}, branch_key=branch.key, collection_key=collection.key)
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

    unformatted_code = textwrap.dedent("""\
        doc = test_utils.CreateTestDocumentViaController(
            content={ 'a': 'b' },
            branch_key=branch.key,
            collection_key=collection.key,
            collection_key2=collection.key2)
        """)
    expected_formatted_code = textwrap.dedent("""\
        doc = test_utils.CreateTestDocumentViaController(
            content={'a': 'b'},
            branch_key=branch.key,
            collection_key=collection.key,
            collection_key2=collection.key2)
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testNestedListsInDictionary(self):
    unformatted_code = textwrap.dedent("""\
        _A = {
            'cccccccccc': ('^^1',),
            'rrrrrrrrrrrrrrrrrrrrrrrrr': ('^7913',  # AAAAAAAAAAAAAA.
                                         ),
            'eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee': ('^6242',  # BBBBBBBBBBBBBBB.
                                                  ),
            'vvvvvvvvvvvvvvvvvvv': ('^27959',  # CCCCCCCCCCCCCCCCCC.
                                    '^19746',  # DDDDDDDDDDDDDDDDDDDDDDD.
                                    '^22907',  # EEEEEEEEEEEEEEEEEEEEEEEE.
                                    '^21098',  # FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF.
                                    '^22826',  # GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG.
                                    '^22769',  # HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH.
                                    '^22935',  # IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII.
                                    '^3982',  # JJJJJJJJJJJJJ.
                                   ),
            'uuuuuuuuuuuu': ('^19745',  # LLLLLLLLLLLLLLLLLLLLLLLLLL.
                             '^21324',  # MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM.
                             '^22831',  # NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN.
                             '^17081',  # OOOOOOOOOOOOOOOOOOOOO.
                            ),
            'eeeeeeeeeeeeee': (
                '^9416',  # Reporter email. Not necessarily the reporter.
                '^^3',  # This appears to be the raw email field.
            ),
            'cccccccccc': ('^21109',  # PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP.
                          ),
        }
        """)
    expected_formatted_code = textwrap.dedent("""\
        _A = {
            'cccccccccc': ('^^1',),
            'rrrrrrrrrrrrrrrrrrrrrrrrr': (
                '^7913',  # AAAAAAAAAAAAAA.
            ),
            'eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee': (
                '^6242',  # BBBBBBBBBBBBBBB.
            ),
            'vvvvvvvvvvvvvvvvvvv': (
                '^27959',  # CCCCCCCCCCCCCCCCCC.
                '^19746',  # DDDDDDDDDDDDDDDDDDDDDDD.
                '^22907',  # EEEEEEEEEEEEEEEEEEEEEEEE.
                '^21098',  # FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF.
                '^22826',  # GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG.
                '^22769',  # HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH.
                '^22935',  # IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII.
                '^3982',  # JJJJJJJJJJJJJ.
            ),
            'uuuuuuuuuuuu': (
                '^19745',  # LLLLLLLLLLLLLLLLLLLLLLLLLL.
                '^21324',  # MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM.
                '^22831',  # NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN.
                '^17081',  # OOOOOOOOOOOOOOOOOOOOO.
            ),
            'eeeeeeeeeeeeee': (
                '^9416',  # Reporter email. Not necessarily the reporter.
                '^^3',  # This appears to be the raw email field.
            ),
            'cccccccccc': (
                '^21109',  # PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP.
            ),
        }
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testNestedDictionary(self):
    unformatted_code = textwrap.dedent("""\
        class _():
          def _():
            breadcrumbs = [{'name': 'Admin',
                            'url': url_for(".home")},
                           {'title': title},]
            breadcrumbs = [{'name': 'Admin',
                            'url': url_for(".home")},
                           {'title': title}]
        """)
    expected_formatted_code = textwrap.dedent("""\
        class _():
          def _():
            breadcrumbs = [
                {
                    'name': 'Admin',
                    'url': url_for(".home")
                },
                {
                    'title': title
                },
            ]
            breadcrumbs = [{'name': 'Admin', 'url': url_for(".home")}, {'title': title}]
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testDictionaryElementsOnOneLine(self):
    code = textwrap.dedent("""\
        class _():

          @mock.patch.dict(
              os.environ,
              {'HTTP_' + xsrf._XSRF_TOKEN_HEADER.replace('-', '_'): 'atoken'})
          def _():
            pass


        AAAAAAAAAAAAAAAAAAAAAAAA = {
            Environment.XXXXXXXXXX: 'some text more text even more tex',
            Environment.YYYYYYY: 'some text more text even more text yet ag',
            Environment.ZZZZZZZZZZZ: 'some text more text even mor etext yet again tex',
        }
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testNotInParams(self):
    unformatted_code = textwrap.dedent("""\
        list("a long line to break the line. a long line to break the brk a long lin", not True)
        """)
    expected_code = textwrap.dedent("""\
        list("a long line to break the line. a long line to break the brk a long lin",
             not True)
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertEqual(expected_code, reformatter.Reformat(uwlines))

  def testNamedAssignNotAtEndOfLine(self):
    unformatted_code = textwrap.dedent("""\
        def _():
          if True:
            with py3compat.open_with_encoding(filename, mode='w',
                                              encoding=encoding) as fd:
              pass
        """)
    expected_code = textwrap.dedent("""\
        def _():
          if True:
            with py3compat.open_with_encoding(
                filename, mode='w', encoding=encoding) as fd:
              pass
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertEqual(expected_code, reformatter.Reformat(uwlines))

  def testBlankLineBeforeClassDocstring(self):
    unformatted_code = textwrap.dedent('''\
        class A:

          """Does something.

          Also, here are some details.
          """

          def __init__(self):
            pass
        ''')
    expected_code = textwrap.dedent('''\
        class A:
          """Does something.

          Also, here are some details.
          """

          def __init__(self):
            pass
        ''')
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertEqual(expected_code, reformatter.Reformat(uwlines))

    try:
      style.SetGlobalStyle(
          style.CreateStyleFromConfig(
              '{based_on_style: chromium, '
              'blank_line_before_class_docstring: True}'))
      unformatted_code = textwrap.dedent('''\
          class A:

            """Does something.

            Also, here are some details.
            """

            def __init__(self):
              pass
          ''')
      expected_formatted_code = textwrap.dedent('''\
          class A:

            """Does something.

            Also, here are some details.
            """

            def __init__(self):
              pass
          ''')
      uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
      self.assertCodeEqual(expected_formatted_code,
                           reformatter.Reformat(uwlines))
    finally:
      style.SetGlobalStyle(style.CreateChromiumStyle())

  def testTupleCohesion(self):
    unformatted_code = textwrap.dedent("""\
        def f():
          this_is_a_very_long_function_name(an_extremely_long_variable_name, (
              'a string that may be too long %s' % 'M15'))
        """)
    expected_code = textwrap.dedent("""\
        def f():
          this_is_a_very_long_function_name(
              an_extremely_long_variable_name,
              ('a string that may be too long %s' % 'M15'))
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertEqual(expected_code, reformatter.Reformat(uwlines))

  def testSubscriptExpression(self):
    code = textwrap.dedent("""\
        foo = d[not a]
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testListWithFunctionCalls(self):
    unformatted_code = textwrap.dedent("""\
        def foo():
          return [
              Bar(
                  xxx='some string',
                  yyy='another long string',
                  zzz='a third long string'), Bar(
                      xxx='some string',
                      yyy='another long string',
                      zzz='a third long string')
          ]
        """)
    expected_code = textwrap.dedent("""\
        def foo():
          return [
              Bar(xxx='some string',
                  yyy='another long string',
                  zzz='a third long string'),
              Bar(xxx='some string',
                  yyy='another long string',
                  zzz='a third long string')
          ]
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertEqual(expected_code, reformatter.Reformat(uwlines))

  def testEllipses(self):
    unformatted_code = textwrap.dedent("""\
        X=...
        Y = X if ... else X
        """)
    expected_code = textwrap.dedent("""\
        X = ...
        Y = X if ... else X
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertEqual(expected_code, reformatter.Reformat(uwlines))

  def testSplittingBeforeFirstArgumentOnFunctionCall(self):
    """Tests split_before_first_argument on a function call."""
    try:
      style.SetGlobalStyle(
          style.CreateStyleFromConfig(
              '{based_on_style: chromium, split_before_first_argument: True}'))
      unformatted_code = textwrap.dedent("""\
          a_very_long_function_name("long string with formatting {0:s}".format(
              "mystring"))
          """)
      expected_formatted_code = textwrap.dedent("""\
          a_very_long_function_name(
              "long string with formatting {0:s}".format("mystring"))
          """)
      uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
      self.assertCodeEqual(expected_formatted_code,
                           reformatter.Reformat(uwlines))
    finally:
      style.SetGlobalStyle(style.CreateChromiumStyle())

  def testSplittingBeforeFirstArgumentOnFunctionDefinition(self):
    """Tests split_before_first_argument on a function definition."""
    try:
      style.SetGlobalStyle(
          style.CreateStyleFromConfig(
              '{based_on_style: chromium, split_before_first_argument: True}'))
      unformatted_code = textwrap.dedent("""\
          def _GetNumberOfSecondsFromElements(year, month, day, hours,
                                              minutes, seconds, microseconds):
            return
          """)
      expected_formatted_code = textwrap.dedent("""\
          def _GetNumberOfSecondsFromElements(
              year, month, day, hours, minutes, seconds, microseconds):
            return
          """)
      uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
      self.assertCodeEqual(expected_formatted_code,
                           reformatter.Reformat(uwlines))
    finally:
      style.SetGlobalStyle(style.CreateChromiumStyle())

  def testSplittingBeforeFirstArgumentOnCompoundStatement(self):
    """Tests split_before_first_argument on a compound statement."""
    try:
      style.SetGlobalStyle(
          style.CreateStyleFromConfig(
              '{based_on_style: chromium, split_before_first_argument: True}'))
      unformatted_code = textwrap.dedent("""\
          if (long_argument_name_1 == 1 or
              long_argument_name_2 == 2 or
              long_argument_name_3 == 3 or
              long_argument_name_4 == 4):
            pass
          """)
      expected_formatted_code = textwrap.dedent("""\
          if (long_argument_name_1 == 1 or long_argument_name_2 == 2 or
              long_argument_name_3 == 3 or long_argument_name_4 == 4):
            pass
          """)
      uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
      self.assertCodeEqual(expected_formatted_code,
                           reformatter.Reformat(uwlines))
    finally:
      style.SetGlobalStyle(style.CreateChromiumStyle())

  def testCoalesceBracketsOnDict(self):
    """Tests coalesce_brackets on a dictionary."""
    try:
      style.SetGlobalStyle(
          style.CreateStyleFromConfig(
              '{based_on_style: chromium, coalesce_brackets: True}'))
      unformatted_code = textwrap.dedent("""\
          date_time_values = (
              {
                  u'year': year,
                  u'month': month,
                  u'day_of_month': day_of_month,
                  u'hours': hours,
                  u'minutes': minutes,
                  u'seconds': seconds
              }
          )
          """)
      expected_formatted_code = textwrap.dedent("""\
          date_time_values = ({
              u'year': year,
              u'month': month,
              u'day_of_month': day_of_month,
              u'hours': hours,
              u'minutes': minutes,
              u'seconds': seconds
          })
          """)
      uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
      self.assertCodeEqual(expected_formatted_code,
                           reformatter.Reformat(uwlines))
    finally:
      style.SetGlobalStyle(style.CreateChromiumStyle())

  def testSplitAfterComment(self):
    try:
      style.SetGlobalStyle(
          style.CreateStyleFromConfig(
              '{based_on_style: chromium, coalesce_brackets: True, '
              'dedent_closing_brackets: true}'))
      code = textwrap.dedent("""\
          if __name__ == "__main__":
            with another_resource:
              account = {
                  "validUntil":
                      int(time() + (6 * 7 * 24 * 60 * 60))  # in 6 weeks time
              }
          """)
      uwlines = yapf_test_helper.ParseAndUnwrap(code)
      self.assertCodeEqual(code, reformatter.Reformat(uwlines))
    finally:
      style.SetGlobalStyle(style.CreateChromiumStyle())

  def testAsyncAsNonKeyword(self):
    try:
      style.SetGlobalStyle(style.CreatePEP8Style())

      # In Python 2, async may be used as a non-keyword identifier.
      code = textwrap.dedent("""\
          from util import async


          class A(object):
              def foo(self):
                  async.run()

              def bar(self):
                  pass
          """)
      uwlines = yapf_test_helper.ParseAndUnwrap(code)
      self.assertCodeEqual(code, reformatter.Reformat(uwlines, verify=False))
    finally:
      style.SetGlobalStyle(style.CreateChromiumStyle())


if __name__ == '__main__':
  unittest.main()

# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Buganizer tests for yapf.reformatter."""

import textwrap
import unittest

from yapf.yapflib import reformatter
from yapf.yapflib import style

from yapftests import yapf_test_helper


class BuganizerFixes(yapf_test_helper.YAPFTest):

  @classmethod
  def setUpClass(cls):
    style.SetGlobalStyle(style.CreateChromiumStyle())

  def testB67935450(self):
    unformatted_code = """\
def _():
  return (
      (Gauge(
          metric='aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
          group_by=group_by + ['metric:process_name'],
          metric_filter={'metric:process_name': process_name_re}),
       Gauge(
           metric='bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb',
           group_by=group_by + ['metric:process_name'],
           metric_filter={'metric:process_name': process_name_re}))
      | expr.Join(
          left_name='start', left_default=0, right_name='end', right_default=0)
      | m.Point(
          m.Cond(m.VAL['end'] != 0, m.VAL['end'], k.TimestampMicros() /
                 1000000L) - m.Cond(m.VAL['start'] != 0, m.VAL['start'],
                                    m.TimestampMicros() / 1000000L)))
"""
    expected_formatted_code = """\
def _():
  return (
      (Gauge(
          metric='aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
          group_by=group_by + ['metric:process_name'],
          metric_filter={'metric:process_name': process_name_re}),
       Gauge(
           metric='bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb',
           group_by=group_by + ['metric:process_name'],
           metric_filter={'metric:process_name': process_name_re}))
      | expr.Join(
          left_name='start', left_default=0, right_name='end', right_default=0)
      | m.Point(
          m.Cond(m.VAL['end'] != 0, m.VAL['end'],
                 k.TimestampMicros() / 1000000L) -
          m.Cond(m.VAL['start'] != 0, m.VAL['start'],
                 m.TimestampMicros() / 1000000L)))
"""
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB66011084(self):
    unformatted_code = """\
X = {
"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa":  # Comment 1.
([] if True else [ # Comment 2.
    "bbbbbbbbbbbbbbbbbbb",  # Comment 3.
    "cccccccccccccccccccccccc", # Comment 4.
    "ddddddddddddddddddddddddd", # Comment 5.
    "eeeeeeeeeeeeeeeeeeeeeeeeeeeeeee", # Comment 6.
    "fffffffffffffffffffffffffffffff", # Comment 7.
    "ggggggggggggggggggggggggggg", # Comment 8.
    "hhhhhhhhhhhhhhhhhh",  # Comment 9.
]),
}
"""
    expected_formatted_code = """\
X = {
    "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa":  # Comment 1.
        ([] if True else [  # Comment 2.
            "bbbbbbbbbbbbbbbbbbb",  # Comment 3.
            "cccccccccccccccccccccccc",  # Comment 4.
            "ddddddddddddddddddddddddd",  # Comment 5.
            "eeeeeeeeeeeeeeeeeeeeeeeeeeeeeee",  # Comment 6.
            "fffffffffffffffffffffffffffffff",  # Comment 7.
            "ggggggggggggggggggggggggggg",  # Comment 8.
            "hhhhhhhhhhhhhhhhhh",  # Comment 9.
        ]),
}
"""
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB67455376(self):
    unformatted_code = """\
sponge_ids.extend(invocation.id() for invocation in self._client.GetInvocationsByLabels(labels))
"""
    expected_formatted_code = """\
sponge_ids.extend(invocation.id()
                  for invocation in self._client.GetInvocationsByLabels(labels))
"""
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB35210351(self):
    unformatted_code = """\
def _():
  config.AnotherRuleThing(
      'the_title_to_the_thing_here',
      {'monitorname': 'firefly',
       'service': ACCOUNTING_THING,
       'severity': 'the_bug',
       'monarch_module_name': alerts.TheLabel(qa_module_regexp, invert=True)},
      fanout,
      alerts.AlertUsToSomething(
          GetTheAlertToIt('the_title_to_the_thing_here'),
          GetNotificationTemplate('your_email_here')))
"""
    expected_formatted_code = """\
def _():
  config.AnotherRuleThing(
      'the_title_to_the_thing_here', {
          'monitorname': 'firefly',
          'service': ACCOUNTING_THING,
          'severity': 'the_bug',
          'monarch_module_name': alerts.TheLabel(qa_module_regexp, invert=True)
      }, fanout,
      alerts.AlertUsToSomething(
          GetTheAlertToIt('the_title_to_the_thing_here'),
          GetNotificationTemplate('your_email_here')))
"""
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB34774905(self):
    unformatted_code = """\
x=[VarExprType(ir_name=IrName( value='x',
expr_type=UnresolvedAttrExprType( atom=UnknownExprType(), attr_name=IrName(
    value='x', expr_type=UnknownExprType(), usage='UNKNOWN', fqn=None,
    astn=None), usage='REF'), usage='ATTR', fqn='<attr>.x', astn=None))]
"""
    expected_formatted_code = """\
x = [
    VarExprType(
        ir_name=IrName(
            value='x',
            expr_type=UnresolvedAttrExprType(
                atom=UnknownExprType(),
                attr_name=IrName(
                    value='x',
                    expr_type=UnknownExprType(),
                    usage='UNKNOWN',
                    fqn=None,
                    astn=None),
                usage='REF'),
            usage='ATTR',
            fqn='<attr>.x',
            astn=None))
]
"""
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB65176185(self):
    code = """\
xx = zip(*[(a, b) for (a, b, c) in yy])
"""
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB35210166(self):
    unformatted_code = """\
def _():
  query = (
      m.Fetch(n.Raw('monarch.BorgTask', '/proc/container/memory/usage'), { 'borg_user': borguser, 'borg_job': jobname })
      | o.Window(m.Align('5m')) | p.GroupBy(['borg_user', 'borg_job', 'borg_cell'], q.Mean()))
"""
    expected_formatted_code = """\
def _():
  query = (
      m.Fetch(
          n.Raw('monarch.BorgTask', '/proc/container/memory/usage'), {
              'borg_user': borguser,
              'borg_job': jobname
          })
      | o.Window(m.Align('5m'))
      | p.GroupBy(['borg_user', 'borg_job', 'borg_cell'], q.Mean()))
"""
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB32167774(self):
    unformatted_code = """\
X = (
    'is_official',
    'is_cover',
    'is_remix',
    'is_instrumental',
    'is_live',
    'has_lyrics',
    'is_album',
    'is_compilation',)
"""
    expected_formatted_code = """\
X = (
    'is_official',
    'is_cover',
    'is_remix',
    'is_instrumental',
    'is_live',
    'has_lyrics',
    'is_album',
    'is_compilation',
)
"""
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB66912275(self):
    unformatted_code = """\
def _():
  with self.assertRaisesRegexp(errors.HttpError, 'Invalid'):
    patch_op = api_client.forwardingRules().patch(
        project=project_id,
        region=region,
        forwardingRule=rule_name,
        body={'fingerprint': base64.urlsafe_b64encode('invalid_fingerprint')}).execute()
"""
    expected_formatted_code = """\
def _():
  with self.assertRaisesRegexp(errors.HttpError, 'Invalid'):
    patch_op = api_client.forwardingRules().patch(
        project=project_id,
        region=region,
        forwardingRule=rule_name,
        body={
            'fingerprint': base64.urlsafe_b64encode('invalid_fingerprint')
        }).execute()
"""
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB67312284(self):
    code = """\
def _():
  self.assertEqual(
      [u'to be published 2', u'to be published 1', u'to be published 0'],
      [el.text for el in page.first_column_tds])
"""
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB65241516(self):
    unformatted_code = """\
checkpoint_files = gfile.Glob(os.path.join(TrainTraceDir(unit_key, "*", "*"), embedding_model.CHECKPOINT_FILENAME + "-*"))
"""
    expected_formatted_code = """\
checkpoint_files = gfile.Glob(
    os.path.join(
        TrainTraceDir(unit_key, "*", "*"),
        embedding_model.CHECKPOINT_FILENAME + "-*"))
"""
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB37460004(self):
    code = textwrap.dedent("""\
        assert all(s not in (_SENTINEL, None) for s in nested_schemas
                  ), 'Nested schemas should never contain None/_SENTINEL'
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB36806207(self):
    code = """\
def _():
  linearity_data = [[row] for row in [
      "%.1f mm" % (np.mean(linearity_values["pos_error"]) * 1000.0),
      "%.1f mm" % (np.max(linearity_values["pos_error"]) * 1000.0),
      "%.1f mm" % (np.mean(linearity_values["pos_error_chunk_mean"]) * 1000.0),
      "%.1f mm" % (np.max(linearity_values["pos_error_chunk_max"]) * 1000.0),
      "%.1f deg" % math.degrees(np.mean(linearity_values["rot_noise"])),
      "%.1f deg" % math.degrees(np.max(linearity_values["rot_noise"])),
      "%.1f deg" % math.degrees(np.mean(linearity_values["rot_drift"])),
      "%.1f deg" % math.degrees(np.max(linearity_values["rot_drift"])),
      "%.1f%%" % (np.max(linearity_values["pos_discontinuity"]) * 100.0),
      "%.1f%%" % (np.max(linearity_values["rot_discontinuity"]) * 100.0)
  ]]
"""
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB36215507(self):
    code = textwrap.dedent("""\
        class X():

          def _():
            aaaaaaaaaaaaa._bbbbbbbbbbbbbbbbbbbbbbbbbbbbbb(
                mmmmmmmmmmmmm, nnnnn, ooooooooo,
                _(ppppppppppppppppppppppppppppppppppppp),
                *(qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq),
                **(qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq))
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB35212469(self):
    unformatted_code = textwrap.dedent("""\
        def _():
          X = {
            'retain': {
                'loadtest':  # This is a comment in the middle of a dictionary entry
                    ('/some/path/to/a/file/that/is/needed/by/this/process')
              }
          }
        """)
    expected_formatted_code = textwrap.dedent("""\
        def _():
          X = {
              'retain': {
                  'loadtest':  # This is a comment in the middle of a dictionary entry
                      ('/some/path/to/a/file/that/is/needed/by/this/process')
              }
          }
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB31063453(self):
    unformatted_code = textwrap.dedent("""\
        def _():
          while ((not mpede_proc) or ((time_time() - last_modified) < FLAGS_boot_idle_timeout)):
            pass
        """)
    expected_formatted_code = textwrap.dedent("""\
        def _():
          while ((not mpede_proc) or
                 ((time_time() - last_modified) < FLAGS_boot_idle_timeout)):
            pass
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB35021894(self):
    unformatted_code = textwrap.dedent("""\
        def _():
          labelacl = Env(qa={
              'read': 'name/some-type-of-very-long-name-for-reading-perms',
              'modify': 'name/some-other-type-of-very-long-name-for-modifying'
          },
                         prod={
                            'read': 'name/some-type-of-very-long-name-for-reading-perms',
                            'modify': 'name/some-other-type-of-very-long-name-for-modifying'
                         })
        """)
    expected_formatted_code = textwrap.dedent("""\
        def _():
          labelacl = Env(
              qa={
                  'read': 'name/some-type-of-very-long-name-for-reading-perms',
                  'modify': 'name/some-other-type-of-very-long-name-for-modifying'
              },
              prod={
                  'read': 'name/some-type-of-very-long-name-for-reading-perms',
                  'modify': 'name/some-other-type-of-very-long-name-for-modifying'
              })
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB34682902(self):
    unformatted_code = textwrap.dedent("""\
        logging.info("Mean angular velocity norm: %.3f", np.linalg.norm(np.mean(ang_vel_arr, axis=0)))
        """)
    expected_formatted_code = textwrap.dedent("""\
        logging.info("Mean angular velocity norm: %.3f",
                     np.linalg.norm(np.mean(ang_vel_arr, axis=0)))
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB33842726(self):
    unformatted_code = textwrap.dedent("""\
        class _():
          def _():
            hints.append(('hg tag -f -l -r %s %s # %s' % (short(ctx.node(
            )), candidatetag, firstline))[:78])
        """)
    expected_formatted_code = textwrap.dedent("""\
        class _():
          def _():
            hints.append(('hg tag -f -l -r %s %s # %s' %
                          (short(ctx.node()), candidatetag, firstline))[:78])
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB32931780(self):
    unformatted_code = textwrap.dedent("""\
        environments = {
            'prod': {
                # this is a comment before the first entry.
                'entry one':
                    'an entry.',
                # this is the comment before the second entry.
                'entry number 2.':
                    'something',
                # this is the comment before the third entry and it's a doozy. So big!
                'who':
                    'allin',
                # This is an entry that has a dictionary in it. It's ugly
                'something': {
                    'page': ['this-is-a-page@xxxxxxxx.com', 'something-for-eml@xxxxxx.com'],
                    'bug': ['bugs-go-here5300@xxxxxx.com'],
                    'email': ['sometypeof-email@xxxxxx.com'],
                },
                # a short comment
                'yolo!!!!!':
                    'another-email-address@xxxxxx.com',
                # this entry has an implicit string concatenation
                'implicit':
                    'https://this-is-very-long.url-addr.com/'
                    '?something=something%20some%20more%20stuff..',
                # A more normal entry.
                '.....':
                    'this is an entry',
            }
        }
        """)
    expected_formatted_code = textwrap.dedent("""\
        environments = {
            'prod': {
                # this is a comment before the first entry.
                'entry one': 'an entry.',
                # this is the comment before the second entry.
                'entry number 2.': 'something',
                # this is the comment before the third entry and it's a doozy. So big!
                'who': 'allin',
                # This is an entry that has a dictionary in it. It's ugly
                'something': {
                    'page': [
                        'this-is-a-page@xxxxxxxx.com', 'something-for-eml@xxxxxx.com'
                    ],
                    'bug': ['bugs-go-here5300@xxxxxx.com'],
                    'email': ['sometypeof-email@xxxxxx.com'],
                },
                # a short comment
                'yolo!!!!!': 'another-email-address@xxxxxx.com',
                # this entry has an implicit string concatenation
                'implicit': 'https://this-is-very-long.url-addr.com/'
                            '?something=something%20some%20more%20stuff..',
                # A more normal entry.
                '.....': 'this is an entry',
            }
        }
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB33047408(self):
    code = textwrap.dedent("""\
        def _():
          for sort in (sorts or []):
            request['sorts'].append({
                'field': {
                    'user_field': sort
                },
                'order': 'ASCENDING'
            })
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB32714745(self):
    code = textwrap.dedent("""\
        class _():

          def _BlankDefinition():
            '''Return a generic blank dictionary for a new field.'''
            return {
                'type': '',
                'validation': '',
                'name': 'fieldname',
                'label': 'Field Label',
                'help': '',
                'initial': '',
                'required': False,
                'required_msg': 'Required',
                'invalid_msg': 'Please enter a valid value',
                'options': {
                    'regex': '',
                    'widget_attr': '',
                    'choices_checked': '',
                    'choices_count': '',
                    'choices': {}
                },
                'isnew': True,
                'dirty': False,
            }
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB32737279(self):
    unformatted_code = textwrap.dedent("""\
        here_is_a_dict = {
            'key':
            # Comment.
            'value'
        }
        """)
    expected_formatted_code = textwrap.dedent("""\
        here_is_a_dict = {
            'key':  # Comment.
                'value'
        }
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB32570937(self):
    code = textwrap.dedent("""\
      def _():
        if (job_message.ball not in ('*', ball) or
            job_message.call not in ('*', call) or
            job_message.mall not in ('*', job_name)):
          return False
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB31937033(self):
    code = textwrap.dedent("""\
        class _():

          def __init__(self, metric, fields_cb=None):
            self._fields_cb = fields_cb or (lambda *unused_args, **unused_kwargs: {})
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB31911533(self):
    code = """\
class _():

  @parameterized.NamedParameters(
      ('IncludingModInfoWithHeaderList', AAAA, aaaa),
      ('IncludingModInfoWithoutHeaderList', BBBB, bbbbb),
      ('ExcludingModInfoWithHeaderList', CCCCC, cccc),
      ('ExcludingModInfoWithoutHeaderList', DDDDD, ddddd),
  )
  def _():
    pass
"""
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB31847238(self):
    unformatted_code = textwrap.dedent("""\
        class _():

          def aaaaa(self, bbbbb, cccccccccccccc=None):  # TODO(who): pylint: disable=unused-argument
            return 1

          def xxxxx(self, yyyyy, zzzzzzzzzzzzzz=None):  # A normal comment that runs over the column limit.
            return 1
        """)
    expected_formatted_code = textwrap.dedent("""\
        class _():

          def aaaaa(self, bbbbb, cccccccccccccc=None):  # TODO(who): pylint: disable=unused-argument
            return 1

          def xxxxx(
              self, yyyyy,
              zzzzzzzzzzzzzz=None):  # A normal comment that runs over the column limit.
            return 1
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB30760569(self):
    unformatted_code = textwrap.dedent("""\
        {'1234567890123456789012345678901234567890123456789012345678901234567890':
             '1234567890123456789012345678901234567890'}
        """)
    expected_formatted_code = textwrap.dedent("""\
        {
            '1234567890123456789012345678901234567890123456789012345678901234567890':
                '1234567890123456789012345678901234567890'
        }
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB26034238(self):
    unformatted_code = textwrap.dedent("""\
        class Thing:

          def Function(self):
            thing.Scrape('/aaaaaaaaa/bbbbbbbbbb/ccccc/dddd/eeeeeeeeeeeeee/ffffffffffffff').AndReturn(42)
        """)
    expected_formatted_code = textwrap.dedent("""\
        class Thing:

          def Function(self):
            thing.Scrape(
                '/aaaaaaaaa/bbbbbbbbbb/ccccc/dddd/eeeeeeeeeeeeee/ffffffffffffff'
            ).AndReturn(42)
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB30536435(self):
    unformatted_code = textwrap.dedent("""\
        def main(unused_argv):
          if True:
            if True:
              aaaaaaaaaaa.comment('import-from[{}] {} {}'.format(
                  bbbbbbbbb.usage,
                  ccccccccc.within,
                  imports.ddddddddddddddddddd(name_item.ffffffffffffffff)))
        """)
    expected_formatted_code = textwrap.dedent("""\
        def main(unused_argv):
          if True:
            if True:
              aaaaaaaaaaa.comment('import-from[{}] {} {}'.format(
                  bbbbbbbbb.usage, ccccccccc.within,
                  imports.ddddddddddddddddddd(name_item.ffffffffffffffff)))
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB30442148(self):
    unformatted_code = textwrap.dedent("""\
        def lulz():
          return (some_long_module_name.SomeLongClassName.
                  some_long_attribute_name.some_long_method_name())
        """)
    expected_formatted_code = textwrap.dedent("""\
        def lulz():
          return (some_long_module_name.SomeLongClassName.some_long_attribute_name.
                  some_long_method_name())
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB26868213(self):
    unformatted_code = textwrap.dedent("""\
      def _():
        xxxxxxxxxxxxxxxxxxx = {
            'ssssss': {'ddddd': 'qqqqq',
                       'p90': aaaaaaaaaaaaaaaaa,
                       'p99': bbbbbbbbbbbbbbbbb,
                       'lllllllllllll': yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy(),},
            'bbbbbbbbbbbbbbbbbbbbbbbbbbbb': {
                'ddddd': 'bork bork bork bo',
                'p90': wwwwwwwwwwwwwwwww,
                'p99': wwwwwwwwwwwwwwwww,
                'lllllllllllll': None,  # use the default
            }
        }
        """)
    expected_formatted_code = textwrap.dedent("""\
      def _():
        xxxxxxxxxxxxxxxxxxx = {
            'ssssss': {
                'ddddd': 'qqqqq',
                'p90': aaaaaaaaaaaaaaaaa,
                'p99': bbbbbbbbbbbbbbbbb,
                'lllllllllllll': yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy(),
            },
            'bbbbbbbbbbbbbbbbbbbbbbbbbbbb': {
                'ddddd': 'bork bork bork bo',
                'p90': wwwwwwwwwwwwwwwww,
                'p99': wwwwwwwwwwwwwwwww,
                'lllllllllllll': None,  # use the default
            }
        }
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB30173198(self):
    code = textwrap.dedent("""\
        class _():

          def _():
            self.assertFalse(
                evaluation_runner.get_larps_in_eval_set('these_arent_the_larps'))
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB29908765(self):
    code = textwrap.dedent("""\
        class _():

          def __repr__(self):
            return '<session %s on %s>' % (self._id,
                                           self._stub._stub.rpc_channel().target())  # pylint:disable=protected-access
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB30087362(self):
    code = textwrap.dedent("""\
        def _():
          for s in sorted(env['foo']):
            bar()
            # This is a comment

          # This is another comment
          foo()
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB30087363(self):
    code = textwrap.dedent("""\
        if False:
          bar()
          # This is a comment
        # This is another comment
        elif True:
          foo()
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB29093579(self):
    unformatted_code = textwrap.dedent("""\
        def _():
          _xxxxxxxxxxxxxxx(aaaaaaaa, bbbbbbbbbbbbbb.cccccccccc[
              dddddddddddddddddddddddddddd.eeeeeeeeeeeeeeeeeeeeee.fffffffffffffffffffff])
        """)
    expected_formatted_code = textwrap.dedent("""\
        def _():
          _xxxxxxxxxxxxxxx(
              aaaaaaaa,
              bbbbbbbbbbbbbb.cccccccccc[dddddddddddddddddddddddddddd.
                                        eeeeeeeeeeeeeeeeeeeeee.fffffffffffffffffffff])
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB26382315(self):
    code = textwrap.dedent("""\
        @hello_world
        # This is a first comment

        # Comment
        def foo():
          pass
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB27616132(self):
    unformatted_code = textwrap.dedent("""\
        if True:
          query.fetch_page.assert_has_calls([
              mock.call(100,
                        start_cursor=None),
              mock.call(100,
                        start_cursor=cursor_1),
              mock.call(100,
                        start_cursor=cursor_2),
          ])
        """)
    expected_formatted_code = textwrap.dedent("""\
        if True:
          query.fetch_page.assert_has_calls([
              mock.call(100, start_cursor=None),
              mock.call(100, start_cursor=cursor_1),
              mock.call(100, start_cursor=cursor_2),
          ])
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB27590179(self):
    unformatted_code = textwrap.dedent("""\
        if True:
          if True:
            self.aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa = (
                { True:
                     self.bbb.cccccccccc(ddddddddddddddddddddddd.eeeeeeeeeeeeeeeeeeeeee),
                 False:
                     self.bbb.cccccccccc(ddddddddddddddddddddddd.eeeeeeeeeeeeeeeeeeeeee)
                })
        """)
    expected_formatted_code = textwrap.dedent("""\
        if True:
          if True:
            self.aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa = ({
                True:
                    self.bbb.cccccccccc(ddddddddddddddddddddddd.eeeeeeeeeeeeeeeeeeeeee),
                False:
                    self.bbb.cccccccccc(ddddddddddddddddddddddd.eeeeeeeeeeeeeeeeeeeeee)
            })
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB27266946(self):
    unformatted_code = textwrap.dedent("""\
        def _():
          aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa = (self.bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb.cccccccccccccccccccccccccccccccccccc)
        """)
    expected_formatted_code = textwrap.dedent("""\
        def _():
          aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa = (
              self.bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb.
              cccccccccccccccccccccccccccccccccccc)
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB25505359(self):
    code = textwrap.dedent("""\
        _EXAMPLE = {
            'aaaaaaaaaaaaaa': [{
                'bbbb': 'cccccccccccccccccccccc',
                'dddddddddddd': []
            }, {
                'bbbb': 'ccccccccccccccccccc',
                'dddddddddddd': []
            }]
        }
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB25324261(self):
    code = textwrap.dedent("""\
        aaaaaaaaa = set(bbbb.cccc
                        for ddd in eeeeee.fffffffffff.gggggggggggggggg
                        for cccc in ddd.specification)
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB25136704(self):
    code = textwrap.dedent("""\
        class f:

          def test(self):
            self.bbbbbbb[0]['aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', {
                'xxxxxx': 'yyyyyy'
            }] = cccccc.ddd('1m', '10x1+1')
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB25165602(self):
    code = textwrap.dedent("""\
        def f():
          ids = {u: i for u, i in zip(self.aaaaa, xrange(42, 42 + len(self.aaaaaa)))}
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB25157123(self):
    code = textwrap.dedent("""\
        def ListArgs():
          FairlyLongMethodName([relatively_long_identifier_for_a_list],
                               another_argument_with_a_long_identifier)
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB25136820(self):
    unformatted_code = textwrap.dedent("""\
        def foo():
          return collections.OrderedDict({
              # Preceding comment.
              'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa':
              '$bbbbbbbbbbbbbbbbbbbbbbbb',
          })
        """)
    expected_formatted_code = textwrap.dedent("""\
        def foo():
          return collections.OrderedDict({
              # Preceding comment.
              'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa':
                  '$bbbbbbbbbbbbbbbbbbbbbbbb',
          })
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB25131481(self):
    unformatted_code = textwrap.dedent("""\
        APPARENT_ACTIONS = ('command_type', {
            'materialize': lambda x: some_type_of_function('materialize ' + x.command_def),
            '#': lambda x: x  # do nothing
        })
        """)
    expected_formatted_code = textwrap.dedent("""\
        APPARENT_ACTIONS = (
            'command_type',
            {
                'materialize':
                    lambda x: some_type_of_function('materialize ' + x.command_def),
                '#':
                    lambda x: x  # do nothing
            })
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB23445244(self):
    unformatted_code = textwrap.dedent("""\
        def foo():
          if True:
            return xxxxxxxxxxxxxxxx(
                command,
                extra_env={
                    "OOOOOOOOOOOOOOOOOOOOO": FLAGS.zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz,
                    "PPPPPPPPPPPPPPPPPPPPP":
                        FLAGS.aaaaaaaaaaaaaa + FLAGS.bbbbbbbbbbbbbbbbbbb,
                })
        """)
    expected_formatted_code = textwrap.dedent("""\
        def foo():
          if True:
            return xxxxxxxxxxxxxxxx(
                command,
                extra_env={
                    "OOOOOOOOOOOOOOOOOOOOO":
                        FLAGS.zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz,
                    "PPPPPPPPPPPPPPPPPPPPP":
                        FLAGS.aaaaaaaaaaaaaa + FLAGS.bbbbbbbbbbbbbbbbbbb,
                })
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB20559654(self):
    unformatted_code = textwrap.dedent("""\
      class A(object):

        def foo(self):
          unused_error, result = server.Query(
              ['AA BBBB CCC DDD EEEEEEEE X YY ZZZZ FFF EEE AAAAAAAA'],
              aaaaaaaaaaa=True, bbbbbbbb=None)
        """)
    expected_formatted_code = textwrap.dedent("""\
      class A(object):

        def foo(self):
          unused_error, result = server.Query(
              ['AA BBBB CCC DDD EEEEEEEE X YY ZZZZ FFF EEE AAAAAAAA'],
              aaaaaaaaaaa=True,
              bbbbbbbb=None)
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB23943842(self):
    unformatted_code = textwrap.dedent("""\
        class F():
          def f():
            self.assertDictEqual(
                accounts, {
                    'foo':
                    {'account': 'foo',
                     'lines': 'l1\\nl2\\nl3\\n1 line(s) were elided.'},
                    'bar': {'account': 'bar',
                            'lines': 'l5\\nl6\\nl7'},
                    'wiz': {'account': 'wiz',
                            'lines': 'l8'}
                })
        """)
    expected_formatted_code = textwrap.dedent("""\
        class F():

          def f():
            self.assertDictEqual(
                accounts, {
                    'foo': {
                        'account': 'foo',
                        'lines': 'l1\\nl2\\nl3\\n1 line(s) were elided.'
                    },
                    'bar': {
                        'account': 'bar',
                        'lines': 'l5\\nl6\\nl7'
                    },
                    'wiz': {
                        'account': 'wiz',
                        'lines': 'l8'
                    }
                })
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB20551180(self):
    unformatted_code = textwrap.dedent("""\
        def foo():
          if True:
            return (struct.pack('aaaa', bbbbbbbbbb, ccccccccccccccc, dddddddd) + eeeeeee)
        """)
    expected_formatted_code = textwrap.dedent("""\
        def foo():
          if True:
            return (
                struct.pack('aaaa', bbbbbbbbbb, ccccccccccccccc, dddddddd) + eeeeeee)
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB23944849(self):
    unformatted_code = textwrap.dedent("""\
        class A(object):
          def xxxxxxxxx(self, aaaaaaa, bbbbbbb=ccccccccccc, dddddd=300, eeeeeeeeeeeeee=None, fffffffffffffff=0):
            pass
        """)
    expected_formatted_code = textwrap.dedent("""\
        class A(object):

          def xxxxxxxxx(self,
                        aaaaaaa,
                        bbbbbbb=ccccccccccc,
                        dddddd=300,
                        eeeeeeeeeeeeee=None,
                        fffffffffffffff=0):
            pass
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB23935890(self):
    unformatted_code = textwrap.dedent("""\
        class F():
          def functioni(self, aaaaaaa, bbbbbbb, cccccc, dddddddddddddd, eeeeeeeeeeeeeee):
            pass
        """)
    expected_formatted_code = textwrap.dedent("""\
        class F():

          def functioni(self, aaaaaaa, bbbbbbb, cccccc, dddddddddddddd,
                        eeeeeeeeeeeeeee):
            pass
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB28414371(self):
    code = textwrap.dedent("""\
        def _():
          return ((m.fffff(
              m.rrr('mmmmmmmmmmmmmmmm', 'ssssssssssssssssssssssssss'), ffffffffffffffff)
                   | m.wwwwww(m.ddddd('1h'))
                   | m.ggggggg(bbbbbbbbbbbbbbb)
                   | m.ppppp(
                       (1 - m.ffffffffffffffff(llllllllllllllllllllll * 1000000, m.vvv))
                       * m.ddddddddddddddddd(m.vvv)),
                   m.fffff(
                       m.rrr('mmmmmmmmmmmmmmmm', 'sssssssssssssssssssssss'),
                       dict(
                           ffffffffffffffff, **{
                               'mmmmmm:ssssss':
                                   m.rrrrrrrrrrr('|'.join(iiiiiiiiiiiiii), iiiiii=True)
                           }))
                   | m.wwwwww(m.rrrr('1h'))
                   | m.ggggggg(bbbbbbbbbbbbbbb))
                  | m.jjjj()
                  | m.ppppp(m.vvv[0] + m.vvv[1]))
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB20127686(self):
    code = textwrap.dedent("""\
        def f():
          if True:
            return ((m.fffff(
                m.rrr('xxxxxxxxxxxxxxxx',
                      'yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy'),
                mmmmmmmm)
                     | m.wwwwww(m.rrrr(self.tttttttttt, self.mmmmmmmmmmmmmmmmmmmmm))
                     | m.ggggggg(self.gggggggg, m.sss()), m.fffff('aaaaaaaaaaaaaaaa')
                     | m.wwwwww(m.ddddd(self.tttttttttt, self.mmmmmmmmmmmmmmmmmmmmm))
                     | m.ggggggg(self.gggggggg))
                    | m.jjjj()
                    | m.ppppp(m.VAL[0] / m.VAL[1]))
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB20016122(self):
    try:
      style.SetGlobalStyle(
          style.CreateStyleFromConfig(
              '{based_on_style: pep8, split_penalty_import_names: 35}'))
      unformatted_code = textwrap.dedent("""\
          from a_very_long_or_indented_module_name_yada_yada import (long_argument_1,
                                                                     long_argument_2)
          """)
      expected_formatted_code = textwrap.dedent("""\
          from a_very_long_or_indented_module_name_yada_yada import (
              long_argument_1, long_argument_2)
          """)
      uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
      self.assertCodeEqual(expected_formatted_code,
                           reformatter.Reformat(uwlines))
    finally:
      style.SetGlobalStyle(style.CreatePEP8Style())

    try:
      style.SetGlobalStyle(
          style.CreateStyleFromConfig('{based_on_style: chromium, '
                                      'split_before_logical_operator: True}'))
      code = textwrap.dedent("""\
          class foo():

            def __eq__(self, other):
              return (isinstance(other, type(self))
                      and self.xxxxxxxxxxx == other.xxxxxxxxxxx
                      and self.xxxxxxxx == other.xxxxxxxx
                      and self.aaaaaaaaaaaa == other.aaaaaaaaaaaa
                      and self.bbbbbbbbbbb == other.bbbbbbbbbbb
                      and self.ccccccccccccccccc == other.ccccccccccccccccc
                      and self.ddddddddddddddddddddddd == other.ddddddddddddddddddddddd
                      and self.eeeeeeeeeeee == other.eeeeeeeeeeee
                      and self.ffffffffffffff == other.time_completed
                      and self.gggggg == other.gggggg and self.hhh == other.hhh
                      and len(self.iiiiiiii) == len(other.iiiiiiii)
                      and all(jjjjjjj in other.iiiiiiii for jjjjjjj in self.iiiiiiii))
          """)
      uwlines = yapf_test_helper.ParseAndUnwrap(code)
      self.assertCodeEqual(code, reformatter.Reformat(uwlines))
    finally:
      style.SetGlobalStyle(style.CreateChromiumStyle())

  def testB22527411(self):
    unformatted_code = textwrap.dedent("""\
        def f():
          if True:
            aaaaaa.bbbbbbbbbbbbbbbbbbbb[-1].cccccccccccccc.ddd().eeeeeeee(ffffffffffffff)
        """)
    expected_formatted_code = textwrap.dedent("""\
        def f():
          if True:
            aaaaaa.bbbbbbbbbbbbbbbbbbbb[-1].cccccccccccccc.ddd().eeeeeeee(
                ffffffffffffff)
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB20849933(self):
    unformatted_code = textwrap.dedent("""\
        def main(unused_argv):
          if True:
            aaaaaaaa = {
                'xxx': '%s/cccccc/ddddddddddddddddddd.jar' %
                       (eeeeee.FFFFFFFFFFFFFFFFFF),
            }
        """)
    expected_formatted_code = textwrap.dedent("""\
        def main(unused_argv):
          if True:
            aaaaaaaa = {
                'xxx':
                    '%s/cccccc/ddddddddddddddddddd.jar' % (eeeeee.FFFFFFFFFFFFFFFFFF),
            }
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB20813997(self):
    code = textwrap.dedent("""\
        def myfunc_1():
          myarray = numpy.zeros((2, 2, 2))
          print(myarray[:, 1, :])
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB20605036(self):
    code = textwrap.dedent("""\
        foo = {
            'aaaa': {
                # A comment for no particular reason.
                'xxxxxxxx': 'bbbbbbbbb',
                'yyyyyyyyyyyyyyyyyy': 'cccccccccccccccccccccccccccccc'
                                      'dddddddddddddddddddddddddddddddddddddddddd',
            }
        }
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB20562732(self):
    code = textwrap.dedent("""\
        foo = [
            # Comment about first list item
            'First item',
            # Comment about second list item
            'Second item',
        ]
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB20128830(self):
    code = textwrap.dedent("""\
        a = {
            'xxxxxxxxxxxxxxxxxxxx': {
                'aaaa':
                    'mmmmmmm',
                'bbbbb':
                    'mmmmmmmmmmmmmmmmmmmmm',
                'cccccccccc': [
                    'nnnnnnnnnnn',
                    'ooooooooooo',
                    'ppppppppppp',
                    'qqqqqqqqqqq',
                ],
            },
        }
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB20073838(self):
    code = textwrap.dedent("""\
        class DummyModel(object):

          def do_nothing(self, class_1_count):
            if True:
              class_0_count = num_votes - class_1_count
              return ('{class_0_name}={class_0_count}, {class_1_name}={class_1_count}'
                      .format(
                          class_0_name=self.class_0_name,
                          class_0_count=class_0_count,
                          class_1_name=self.class_1_name,
                          class_1_count=class_1_count))
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB19626808(self):
    code = textwrap.dedent("""\
        if True:
          aaaaaaaaaaaaaaaaaaaaaaa.bbbbbbbbb(
              'ccccccccccc', ddddddddd='eeeee').fffffffff([ggggggggggggggggggggg])
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB19547210(self):
    code = textwrap.dedent("""\
        while True:
          if True:
            if True:
              if True:
                if xxxxxxxxxxxx.yyyyyyy(aa).zzzzzzz() not in (
                    xxxxxxxxxxxx.yyyyyyyyyyyyyy.zzzzzzzz,
                    xxxxxxxxxxxx.yyyyyyyyyyyyyy.zzzzzzzz):
                  continue
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB19377034(self):
    code = textwrap.dedent("""\
        def f():
          if (aaaaaaaaaaaaaaa.start >= aaaaaaaaaaaaaaa.end or
              bbbbbbbbbbbbbbb.start >= bbbbbbbbbbbbbbb.end):
            return False
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB19372573(self):
    code = textwrap.dedent("""\
        def f():
            if a: return 42
            while True:
                if b: continue
                if c: break
            return 0
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    try:
      style.SetGlobalStyle(style.CreatePEP8Style())
      self.assertCodeEqual(code, reformatter.Reformat(uwlines))
    finally:
      style.SetGlobalStyle(style.CreateChromiumStyle())

  def testB19353268(self):
    code = textwrap.dedent("""\
        a = {1, 2, 3}[x]
        b = {'foo': 42, 'bar': 37}['foo']
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB19287512(self):
    unformatted_code = textwrap.dedent("""\
        class Foo(object):

          def bar(self):
            with xxxxxxxxxx.yyyyy(
                'aaaaaaa.bbbbbbbb.ccccccc.dddddddddddddddddddd.eeeeeeeeeee',
                fffffffffff=(aaaaaaa.bbbbbbbb.ccccccc.dddddddddddddddddddd
                             .Mmmmmmmmmmmmmmmmmm(-1, 'permission error'))):
              self.assertRaises(nnnnnnnnnnnnnnnn.ooooo, ppppp.qqqqqqqqqqqqqqqqq)
        """)
    expected_formatted_code = textwrap.dedent("""\
        class Foo(object):

          def bar(self):
            with xxxxxxxxxx.yyyyy(
                'aaaaaaa.bbbbbbbb.ccccccc.dddddddddddddddddddd.eeeeeeeeeee',
                fffffffffff=(
                    aaaaaaa.bbbbbbbb.ccccccc.dddddddddddddddddddd.Mmmmmmmmmmmmmmmmmm(
                        -1, 'permission error'))):
              self.assertRaises(nnnnnnnnnnnnnnnn.ooooo, ppppp.qqqqqqqqqqqqqqqqq)
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB19194420(self):
    code = textwrap.dedent("""\
        method.Set(
            'long argument goes here that causes the line to break',
            lambda arg2=0.5: arg2)
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB19073499(self):
    code = """\
instance = (
    aaaaaaa.bbbbbbb().ccccccccccccccccc().ddddddddddd({
        'aa': 'context!'
    }).eeeeeeeeeeeeeeeeeee({  # Inline comment about why fnord has the value 6.
        'fnord': 6
    }))
"""
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB18257115(self):
    code = textwrap.dedent("""\
        if True:
          if True:
            self._Test(aaaa, bbbbbbb.cccccccccc, dddddddd, eeeeeeeeeee,
                       [ffff, ggggggggggg, hhhhhhhhhhhh, iiiiii, jjjj])
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB18256666(self):
    code = textwrap.dedent("""\
        class Foo(object):

          def Bar(self):
            aaaaa.bbbbbbb(
                ccc='ddddddddddddddd',
                eeee='ffffffffffffffffffffff-%s-%s' % (gggg, int(time.time())),
                hhhhhh={
                    'iiiiiiiiiii': iiiiiiiiiii,
                    'jjjj': jjjj.jjjjj(),
                    'kkkkkkkkkkkk': kkkkkkkkkkkk,
                },
                llllllllll=mmmmmm.nnnnnnnnnnnnnnnn)
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB18256826(self):
    code = textwrap.dedent("""\
        if True:
          pass
        # A multiline comment.
        # Line two.
        elif False:
          pass

        if True:
          pass
          # A multiline comment.
          # Line two.
        elif False:
          pass
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB18255697(self):
    code = textwrap.dedent("""\
        AAAAAAAAAAAAAAA = {
            'XXXXXXXXXXXXXX': 4242,  # Inline comment
            # Next comment
            'YYYYYYYYYYYYYYYY': ['zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz'],
        }
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB17534869(self):
    unformatted_code = textwrap.dedent("""\
        if True:
          self.assertLess(abs(time.time()-aaaa.bbbbbbbbbbb(
                              datetime.datetime.now())), 1)
        """)
    expected_formatted_code = textwrap.dedent("""\
        if True:
          self.assertLess(
              abs(time.time() - aaaa.bbbbbbbbbbb(datetime.datetime.now())), 1)
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB17489866(self):
    unformatted_code = textwrap.dedent("""\
        def f():
          if True:
            if True:
              return aaaa.bbbbbbbbb(ccccccc=dddddddddddddd({('eeee', \
'ffffffff'): str(j)}))
        """)
    expected_formatted_code = textwrap.dedent("""\
        def f():
          if True:
            if True:
              return aaaa.bbbbbbbbb(
                  ccccccc=dddddddddddddd({
                      ('eeee', 'ffffffff'): str(j)
                  }))
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB17133019(self):
    unformatted_code = textwrap.dedent("""\
        class aaaaaaaaaaaaaa(object):

          def bbbbbbbbbb(self):
            with io.open("/dev/null", "rb"):
              with io.open(os.path.join(aaaaa.bbbbb.ccccccccccc,
                                        DDDDDDDDDDDDDDD,
                                        "eeeeeeeee ffffffffff"
                                       ), "rb") as gggggggggggggggggggg:
                print(gggggggggggggggggggg)
        """)
    expected_formatted_code = textwrap.dedent("""\
        class aaaaaaaaaaaaaa(object):

          def bbbbbbbbbb(self):
            with io.open("/dev/null", "rb"):
              with io.open(
                  os.path.join(aaaaa.bbbbb.ccccccccccc, DDDDDDDDDDDDDDD,
                               "eeeeeeeee ffffffffff"), "rb") as gggggggggggggggggggg:
                print(gggggggggggggggggggg)
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB17011869(self):
    unformatted_code = textwrap.dedent("""\
        '''blah......'''

        class SomeClass(object):
          '''blah.'''

          AAAAAAAAAAAA = {                        # Comment.
              'BBB': 1.0,
                'DDDDDDDD': 0.4811
                                      }
        """)
    expected_formatted_code = textwrap.dedent("""\
        '''blah......'''


        class SomeClass(object):
          '''blah.'''

          AAAAAAAAAAAA = {  # Comment.
              'BBB': 1.0,
              'DDDDDDDD': 0.4811
          }
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB16783631(self):
    unformatted_code = textwrap.dedent("""\
        if True:
          with aaaaaaaaaaaaaa.bbbbbbbbbbbbb.ccccccc(ddddddddddddd,
                                                      eeeeeeeee=self.fffffffffffff
                                                      )as gggg:
            pass
        """)
    expected_formatted_code = textwrap.dedent("""\
        if True:
          with aaaaaaaaaaaaaa.bbbbbbbbbbbbb.ccccccc(
              ddddddddddddd, eeeeeeeee=self.fffffffffffff) as gggg:
            pass
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB16572361(self):
    unformatted_code = textwrap.dedent("""\
        def foo(self):
         def bar(my_dict_name):
          self.my_dict_name['foo-bar-baz-biz-boo-baa-baa'].IncrementBy.assert_called_once_with('foo_bar_baz_boo')
        """)
    expected_formatted_code = textwrap.dedent("""\
        def foo(self):

          def bar(my_dict_name):
            self.my_dict_name[
                'foo-bar-baz-biz-boo-baa-baa'].IncrementBy.assert_called_once_with(
                    'foo_bar_baz_boo')
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB15884241(self):
    unformatted_code = textwrap.dedent("""\
        if 1:
          if 1:
            for row in AAAA:
              self.create(aaaaaaaa="/aaa/bbbb/cccc/dddddd/eeeeeeeeeeeeeeeeeeeeeeeeee/%s" % row [0].replace(".foo", ".bar"), aaaaa=bbb[1], ccccc=bbb[2], dddd=bbb[3], eeeeeeeeeee=[s.strip() for s in bbb[4].split(",")], ffffffff=[s.strip() for s in bbb[5].split(",")], gggggg=bbb[6])
        """)
    expected_formatted_code = textwrap.dedent("""\
        if 1:
          if 1:
            for row in AAAA:
              self.create(
                  aaaaaaaa="/aaa/bbbb/cccc/dddddd/eeeeeeeeeeeeeeeeeeeeeeeeee/%s" %
                  row[0].replace(".foo", ".bar"),
                  aaaaa=bbb[1],
                  ccccc=bbb[2],
                  dddd=bbb[3],
                  eeeeeeeeeee=[s.strip() for s in bbb[4].split(",")],
                  ffffffff=[s.strip() for s in bbb[5].split(",")],
                  gggggg=bbb[6])
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB15697268(self):
    unformatted_code = textwrap.dedent("""\
        def main(unused_argv):
          ARBITRARY_CONSTANT_A = 10
          an_array_with_an_exceedingly_long_name = range(ARBITRARY_CONSTANT_A + 1)
          ok = an_array_with_an_exceedingly_long_name[:ARBITRARY_CONSTANT_A]
          bad_slice = map(math.sqrt, an_array_with_an_exceedingly_long_name[:ARBITRARY_CONSTANT_A])
          a_long_name_slicing = an_array_with_an_exceedingly_long_name[:ARBITRARY_CONSTANT_A]
          bad_slice = ("I am a crazy, no good, string whats too long, etc." + " no really ")[:ARBITRARY_CONSTANT_A]
        """)
    expected_formatted_code = textwrap.dedent("""\
        def main(unused_argv):
          ARBITRARY_CONSTANT_A = 10
          an_array_with_an_exceedingly_long_name = range(ARBITRARY_CONSTANT_A + 1)
          ok = an_array_with_an_exceedingly_long_name[:ARBITRARY_CONSTANT_A]
          bad_slice = map(math.sqrt,
                          an_array_with_an_exceedingly_long_name[:ARBITRARY_CONSTANT_A])
          a_long_name_slicing = an_array_with_an_exceedingly_long_name[:
                                                                       ARBITRARY_CONSTANT_A]
          bad_slice = ("I am a crazy, no good, string whats too long, etc." +
                       " no really ")[:ARBITRARY_CONSTANT_A]
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB15597568(self):
    unformatted_code = textwrap.dedent("""\
        if True:
          if True:
            if True:
              print(("Return code was %d" + (", and the process timed out." if did_time_out else ".")) % errorcode)
        """)
    expected_formatted_code = textwrap.dedent("""\
        if True:
          if True:
            if True:
              print(("Return code was %d" + (", and the process timed out."
                                             if did_time_out else ".")) % errorcode)
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB15542157(self):
    unformatted_code = textwrap.dedent("""\
        aaaaaaaaaaaa = bbbb.ccccccccccccccc(dddddd.eeeeeeeeeeeeee, ffffffffffffffffff, gggggg.hhhhhhhhhhhhhhhhh)
        """)
    expected_formatted_code = textwrap.dedent("""\
        aaaaaaaaaaaa = bbbb.ccccccccccccccc(dddddd.eeeeeeeeeeeeee, ffffffffffffffffff,
                                            gggggg.hhhhhhhhhhhhhhhhh)
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB15438132(self):
    unformatted_code = textwrap.dedent("""\
        if aaaaaaa.bbbbbbbbbb:
           cccccc.dddddddddd(eeeeeeeeeee=fffffffffffff.gggggggggggggggggg)
           if hhhhhh.iiiii.jjjjjjjjjjjjj:
             # This is a comment in the middle of it all.
             kkkkkkk.llllllllll.mmmmmmmmmmmmm = True
           if (aaaaaa.bbbbb.ccccccccccccc != ddddddd.eeeeeeeeee.fffffffffffff or
               eeeeee.fffff.ggggggggggggggggggggggggggg() != hhhhhhh.iiiiiiiiii.jjjjjjjjjjjj):
             aaaaaaaa.bbbbbbbbbbbb(
                 aaaaaa.bbbbb.cc,
                 dddddddddddd=eeeeeeeeeeeeeeeeeee.fffffffffffffffff(
                     gggggg.hh,
                     iiiiiiiiiiiiiiiiiii.jjjjjjjjjj.kkkkkkk,
                     lllll.mm),
                 nnnnnnnnnn=ooooooo.pppppppppp)
        """)
    expected_formatted_code = textwrap.dedent("""\
        if aaaaaaa.bbbbbbbbbb:
          cccccc.dddddddddd(eeeeeeeeeee=fffffffffffff.gggggggggggggggggg)
          if hhhhhh.iiiii.jjjjjjjjjjjjj:
            # This is a comment in the middle of it all.
            kkkkkkk.llllllllll.mmmmmmmmmmmmm = True
          if (aaaaaa.bbbbb.ccccccccccccc != ddddddd.eeeeeeeeee.fffffffffffff or
              eeeeee.fffff.ggggggggggggggggggggggggggg() !=
              hhhhhhh.iiiiiiiiii.jjjjjjjjjjjj):
            aaaaaaaa.bbbbbbbbbbbb(
                aaaaaa.bbbbb.cc,
                dddddddddddd=eeeeeeeeeeeeeeeeeee.fffffffffffffffff(
                    gggggg.hh, iiiiiiiiiiiiiiiiiii.jjjjjjjjjj.kkkkkkk, lllll.mm),
                nnnnnnnnnn=ooooooo.pppppppppp)
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB14468247(self):
    unformatted_code = """\
call(a=1,
    b=2,
)
"""
    expected_formatted_code = """\
call(
    a=1,
    b=2,
)
"""
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB14406499(self):
    unformatted_code = textwrap.dedent("""\
        def foo1(parameter_1, parameter_2, parameter_3, parameter_4, \
parameter_5, parameter_6): pass
        """)
    expected_formatted_code = textwrap.dedent("""\
        def foo1(parameter_1, parameter_2, parameter_3, parameter_4, parameter_5,
                 parameter_6):
          pass
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB13900309(self):
    unformatted_code = textwrap.dedent("""\
        self.aaaaaaaaaaa(  # A comment in the middle of it all.
               948.0/3600, self.bbb.ccccccccccccccccccccc(dddddddddddddddd.eeee, True))
        """)
    expected_formatted_code = textwrap.dedent("""\
        self.aaaaaaaaaaa(  # A comment in the middle of it all.
            948.0 / 3600, self.bbb.ccccccccccccccccccccc(dddddddddddddddd.eeee, True))
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

    code = textwrap.dedent("""\
        aaaaaaaaaa.bbbbbbbbbbbbbbbbbbbbbbbb.cccccccccccccccccccccccccccccc(
            DC_1, (CL - 50, CL), AAAAAAAA, BBBBBBBBBBBBBBBB, 98.0,
            CCCCCCC).ddddddddd(  # Look! A comment is here.
                AAAAAAAA - (20 * 60 - 5))
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

    unformatted_code = textwrap.dedent("""\
        aaaaaaaaaaaaaaaaaaaaaaaa.bbbbbbbbbbbbb.ccccccccccccccccccccccccc().dddddddddddddddddddddddddd(1, 2, 3, 4)
        """)
    expected_formatted_code = textwrap.dedent("""\
        aaaaaaaaaaaaaaaaaaaaaaaa.bbbbbbbbbbbbb.ccccccccccccccccccccccccc(
        ).dddddddddddddddddddddddddd(1, 2, 3, 4)
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

    unformatted_code = textwrap.dedent("""\
        aaaaaaaaaaaaaaaaaaaaaaaa.bbbbbbbbbbbbb.ccccccccccccccccccccccccc(x).dddddddddddddddddddddddddd(1, 2, 3, 4)
        """)
    expected_formatted_code = textwrap.dedent("""\
        aaaaaaaaaaaaaaaaaaaaaaaa.bbbbbbbbbbbbb.ccccccccccccccccccccccccc(
            x).dddddddddddddddddddddddddd(1, 2, 3, 4)
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

    unformatted_code = textwrap.dedent("""\
        aaaaaaaaaaaaaaaaaaaaaaaa(xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx).dddddddddddddddddddddddddd(1, 2, 3, 4)
        """)
    expected_formatted_code = textwrap.dedent("""\
        aaaaaaaaaaaaaaaaaaaaaaaa(
            xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx).dddddddddddddddddddddddddd(1, 2, 3, 4)
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

    unformatted_code = textwrap.dedent("""\
        aaaaaaaaaaaaaaaaaaaaaaaa().bbbbbbbbbbbbbbbbbbbbbbbb().ccccccccccccccccccc().\
dddddddddddddddddd().eeeeeeeeeeeeeeeeeeeee().fffffffffffffffff().gggggggggggggggggg()
        """)
    expected_formatted_code = textwrap.dedent("""\
        aaaaaaaaaaaaaaaaaaaaaaaa().bbbbbbbbbbbbbbbbbbbbbbbb().ccccccccccccccccccc(
        ).dddddddddddddddddd().eeeeeeeeeeeeeeeeeeeee().fffffffffffffffff(
        ).gggggggggggggggggg()
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB67935687(self):
    code = textwrap.dedent("""\
        Fetch(
            Raw('monarch.BorgTask', '/union/row_operator_action_delay'),
            {'borg_user': self.borg_user})
    """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

    unformatted_code = textwrap.dedent("""\
        shelf_renderer.expand_text = text.translate_to_unicode(
            expand_text % {
                'creator': creator
            })
        """)
    expected_formatted_code = textwrap.dedent("""\
        shelf_renderer.expand_text = text.translate_to_unicode(
            expand_text % {'creator': creator})
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))


if __name__ == '__main__':
  unittest.main()

# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Buganizer tests for yapf.reformatter."""

import textwrap
import unittest

from yapf.yapflib import reformatter
from yapf.yapflib import style

from yapftests import yapf_test_helper


class BuganizerFixes(yapf_test_helper.YAPFTest):

  @classmethod
  def setUpClass(cls):
    style.SetGlobalStyle(style.CreateChromiumStyle())

  def testB67935450(self):
    unformatted_code = """\
def _():
  return (
      (Gauge(
          metric='aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
          group_by=group_by + ['metric:process_name'],
          metric_filter={'metric:process_name': process_name_re}),
       Gauge(
           metric='bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb',
           group_by=group_by + ['metric:process_name'],
           metric_filter={'metric:process_name': process_name_re}))
      | expr.Join(
          left_name='start', left_default=0, right_name='end', right_default=0)
      | m.Point(
          m.Cond(m.VAL['end'] != 0, m.VAL['end'], k.TimestampMicros() /
                 1000000L) - m.Cond(m.VAL['start'] != 0, m.VAL['start'],
                                    m.TimestampMicros() / 1000000L)))
"""
    expected_formatted_code = """\
def _():
  return (
      (Gauge(
          metric='aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
          group_by=group_by + ['metric:process_name'],
          metric_filter={'metric:process_name': process_name_re}),
       Gauge(
           metric='bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb',
           group_by=group_by + ['metric:process_name'],
           metric_filter={'metric:process_name': process_name_re}))
      | expr.Join(
          left_name='start', left_default=0, right_name='end', right_default=0)
      | m.Point(
          m.Cond(m.VAL['end'] != 0, m.VAL['end'],
                 k.TimestampMicros() / 1000000L) -
          m.Cond(m.VAL['start'] != 0, m.VAL['start'],
                 m.TimestampMicros() / 1000000L)))
"""
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB66011084(self):
    unformatted_code = """\
X = {
"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa":  # Comment 1.
([] if True else [ # Comment 2.
    "bbbbbbbbbbbbbbbbbbb",  # Comment 3.
    "cccccccccccccccccccccccc", # Comment 4.
    "ddddddddddddddddddddddddd", # Comment 5.
    "eeeeeeeeeeeeeeeeeeeeeeeeeeeeeee", # Comment 6.
    "fffffffffffffffffffffffffffffff", # Comment 7.
    "ggggggggggggggggggggggggggg", # Comment 8.
    "hhhhhhhhhhhhhhhhhh",  # Comment 9.
]),
}
"""
    expected_formatted_code = """\
X = {
    "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa":  # Comment 1.
        ([] if True else [  # Comment 2.
            "bbbbbbbbbbbbbbbbbbb",  # Comment 3.
            "cccccccccccccccccccccccc",  # Comment 4.
            "ddddddddddddddddddddddddd",  # Comment 5.
            "eeeeeeeeeeeeeeeeeeeeeeeeeeeeeee",  # Comment 6.
            "fffffffffffffffffffffffffffffff",  # Comment 7.
            "ggggggggggggggggggggggggggg",  # Comment 8.
            "hhhhhhhhhhhhhhhhhh",  # Comment 9.
        ]),
}
"""
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB67455376(self):
    unformatted_code = """\
sponge_ids.extend(invocation.id() for invocation in self._client.GetInvocationsByLabels(labels))
"""
    expected_formatted_code = """\
sponge_ids.extend(invocation.id()
                  for invocation in self._client.GetInvocationsByLabels(labels))
"""
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB35210351(self):
    unformatted_code = """\
def _():
  config.AnotherRuleThing(
      'the_title_to_the_thing_here',
      {'monitorname': 'firefly',
       'service': ACCOUNTING_THING,
       'severity': 'the_bug',
       'monarch_module_name': alerts.TheLabel(qa_module_regexp, invert=True)},
      fanout,
      alerts.AlertUsToSomething(
          GetTheAlertToIt('the_title_to_the_thing_here'),
          GetNotificationTemplate('your_email_here')))
"""
    expected_formatted_code = """\
def _():
  config.AnotherRuleThing(
      'the_title_to_the_thing_here', {
          'monitorname': 'firefly',
          'service': ACCOUNTING_THING,
          'severity': 'the_bug',
          'monarch_module_name': alerts.TheLabel(qa_module_regexp, invert=True)
      }, fanout,
      alerts.AlertUsToSomething(
          GetTheAlertToIt('the_title_to_the_thing_here'),
          GetNotificationTemplate('your_email_here')))
"""
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB34774905(self):
    unformatted_code = """\
x=[VarExprType(ir_name=IrName( value='x',
expr_type=UnresolvedAttrExprType( atom=UnknownExprType(), attr_name=IrName(
    value='x', expr_type=UnknownExprType(), usage='UNKNOWN', fqn=None,
    astn=None), usage='REF'), usage='ATTR', fqn='<attr>.x', astn=None))]
"""
    expected_formatted_code = """\
x = [
    VarExprType(
        ir_name=IrName(
            value='x',
            expr_type=UnresolvedAttrExprType(
                atom=UnknownExprType(),
                attr_name=IrName(
                    value='x',
                    expr_type=UnknownExprType(),
                    usage='UNKNOWN',
                    fqn=None,
                    astn=None),
                usage='REF'),
            usage='ATTR',
            fqn='<attr>.x',
            astn=None))
]
"""
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB65176185(self):
    code = """\
xx = zip(*[(a, b) for (a, b, c) in yy])
"""
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB35210166(self):
    unformatted_code = """\
def _():
  query = (
      m.Fetch(n.Raw('monarch.BorgTask', '/proc/container/memory/usage'), { 'borg_user': borguser, 'borg_job': jobname })
      | o.Window(m.Align('5m')) | p.GroupBy(['borg_user', 'borg_job', 'borg_cell'], q.Mean()))
"""
    expected_formatted_code = """\
def _():
  query = (
      m.Fetch(
          n.Raw('monarch.BorgTask', '/proc/container/memory/usage'), {
              'borg_user': borguser,
              'borg_job': jobname
          })
      | o.Window(m.Align('5m'))
      | p.GroupBy(['borg_user', 'borg_job', 'borg_cell'], q.Mean()))
"""
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB32167774(self):
    unformatted_code = """\
X = (
    'is_official',
    'is_cover',
    'is_remix',
    'is_instrumental',
    'is_live',
    'has_lyrics',
    'is_album',
    'is_compilation',)
"""
    expected_formatted_code = """\
X = (
    'is_official',
    'is_cover',
    'is_remix',
    'is_instrumental',
    'is_live',
    'has_lyrics',
    'is_album',
    'is_compilation',
)
"""
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB66912275(self):
    unformatted_code = """\
def _():
  with self.assertRaisesRegexp(errors.HttpError, 'Invalid'):
    patch_op = api_client.forwardingRules().patch(
        project=project_id,
        region=region,
        forwardingRule=rule_name,
        body={'fingerprint': base64.urlsafe_b64encode('invalid_fingerprint')}).execute()
"""
    expected_formatted_code = """\
def _():
  with self.assertRaisesRegexp(errors.HttpError, 'Invalid'):
    patch_op = api_client.forwardingRules().patch(
        project=project_id,
        region=region,
        forwardingRule=rule_name,
        body={
            'fingerprint': base64.urlsafe_b64encode('invalid_fingerprint')
        }).execute()
"""
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB67312284(self):
    code = """\
def _():
  self.assertEqual(
      [u'to be published 2', u'to be published 1', u'to be published 0'],
      [el.text for el in page.first_column_tds])
"""
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB65241516(self):
    unformatted_code = """\
checkpoint_files = gfile.Glob(os.path.join(TrainTraceDir(unit_key, "*", "*"), embedding_model.CHECKPOINT_FILENAME + "-*"))
"""
    expected_formatted_code = """\
checkpoint_files = gfile.Glob(
    os.path.join(
        TrainTraceDir(unit_key, "*", "*"),
        embedding_model.CHECKPOINT_FILENAME + "-*"))
"""
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB37460004(self):
    code = textwrap.dedent("""\
        assert all(s not in (_SENTINEL, None) for s in nested_schemas
                  ), 'Nested schemas should never contain None/_SENTINEL'
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB36806207(self):
    code = """\
def _():
  linearity_data = [[row] for row in [
      "%.1f mm" % (np.mean(linearity_values["pos_error"]) * 1000.0),
      "%.1f mm" % (np.max(linearity_values["pos_error"]) * 1000.0),
      "%.1f mm" % (np.mean(linearity_values["pos_error_chunk_mean"]) * 1000.0),
      "%.1f mm" % (np.max(linearity_values["pos_error_chunk_max"]) * 1000.0),
      "%.1f deg" % math.degrees(np.mean(linearity_values["rot_noise"])),
      "%.1f deg" % math.degrees(np.max(linearity_values["rot_noise"])),
      "%.1f deg" % math.degrees(np.mean(linearity_values["rot_drift"])),
      "%.1f deg" % math.degrees(np.max(linearity_values["rot_drift"])),
      "%.1f%%" % (np.max(linearity_values["pos_discontinuity"]) * 100.0),
      "%.1f%%" % (np.max(linearity_values["rot_discontinuity"]) * 100.0)
  ]]
"""
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB36215507(self):
    code = textwrap.dedent("""\
        class X():

          def _():
            aaaaaaaaaaaaa._bbbbbbbbbbbbbbbbbbbbbbbbbbbbbb(
                mmmmmmmmmmmmm, nnnnn, ooooooooo,
                _(ppppppppppppppppppppppppppppppppppppp),
                *(qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq),
                **(qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq))
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB35212469(self):
    unformatted_code = textwrap.dedent("""\
        def _():
          X = {
            'retain': {
                'loadtest':  # This is a comment in the middle of a dictionary entry
                    ('/some/path/to/a/file/that/is/needed/by/this/process')
              }
          }
        """)
    expected_formatted_code = textwrap.dedent("""\
        def _():
          X = {
              'retain': {
                  'loadtest':  # This is a comment in the middle of a dictionary entry
                      ('/some/path/to/a/file/that/is/needed/by/this/process')
              }
          }
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB31063453(self):
    unformatted_code = textwrap.dedent("""\
        def _():
          while ((not mpede_proc) or ((time_time() - last_modified) < FLAGS_boot_idle_timeout)):
            pass
        """)
    expected_formatted_code = textwrap.dedent("""\
        def _():
          while ((not mpede_proc) or
                 ((time_time() - last_modified) < FLAGS_boot_idle_timeout)):
            pass
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB35021894(self):
    unformatted_code = textwrap.dedent("""\
        def _():
          labelacl = Env(qa={
              'read': 'name/some-type-of-very-long-name-for-reading-perms',
              'modify': 'name/some-other-type-of-very-long-name-for-modifying'
          },
                         prod={
                            'read': 'name/some-type-of-very-long-name-for-reading-perms',
                            'modify': 'name/some-other-type-of-very-long-name-for-modifying'
                         })
        """)
    expected_formatted_code = textwrap.dedent("""\
        def _():
          labelacl = Env(
              qa={
                  'read': 'name/some-type-of-very-long-name-for-reading-perms',
                  'modify': 'name/some-other-type-of-very-long-name-for-modifying'
              },
              prod={
                  'read': 'name/some-type-of-very-long-name-for-reading-perms',
                  'modify': 'name/some-other-type-of-very-long-name-for-modifying'
              })
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB34682902(self):
    unformatted_code = textwrap.dedent("""\
        logging.info("Mean angular velocity norm: %.3f", np.linalg.norm(np.mean(ang_vel_arr, axis=0)))
        """)
    expected_formatted_code = textwrap.dedent("""\
        logging.info("Mean angular velocity norm: %.3f",
                     np.linalg.norm(np.mean(ang_vel_arr, axis=0)))
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB33842726(self):
    unformatted_code = textwrap.dedent("""\
        class _():
          def _():
            hints.append(('hg tag -f -l -r %s %s # %s' % (short(ctx.node(
            )), candidatetag, firstline))[:78])
        """)
    expected_formatted_code = textwrap.dedent("""\
        class _():
          def _():
            hints.append(('hg tag -f -l -r %s %s # %s' %
                          (short(ctx.node()), candidatetag, firstline))[:78])
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB32931780(self):
    unformatted_code = textwrap.dedent("""\
        environments = {
            'prod': {
                # this is a comment before the first entry.
                'entry one':
                    'an entry.',
                # this is the comment before the second entry.
                'entry number 2.':
                    'something',
                # this is the comment before the third entry and it's a doozy. So big!
                'who':
                    'allin',
                # This is an entry that has a dictionary in it. It's ugly
                'something': {
                    'page': ['this-is-a-page@xxxxxxxx.com', 'something-for-eml@xxxxxx.com'],
                    'bug': ['bugs-go-here5300@xxxxxx.com'],
                    'email': ['sometypeof-email@xxxxxx.com'],
                },
                # a short comment
                'yolo!!!!!':
                    'another-email-address@xxxxxx.com',
                # this entry has an implicit string concatenation
                'implicit':
                    'https://this-is-very-long.url-addr.com/'
                    '?something=something%20some%20more%20stuff..',
                # A more normal entry.
                '.....':
                    'this is an entry',
            }
        }
        """)
    expected_formatted_code = textwrap.dedent("""\
        environments = {
            'prod': {
                # this is a comment before the first entry.
                'entry one': 'an entry.',
                # this is the comment before the second entry.
                'entry number 2.': 'something',
                # this is the comment before the third entry and it's a doozy. So big!
                'who': 'allin',
                # This is an entry that has a dictionary in it. It's ugly
                'something': {
                    'page': [
                        'this-is-a-page@xxxxxxxx.com', 'something-for-eml@xxxxxx.com'
                    ],
                    'bug': ['bugs-go-here5300@xxxxxx.com'],
                    'email': ['sometypeof-email@xxxxxx.com'],
                },
                # a short comment
                'yolo!!!!!': 'another-email-address@xxxxxx.com',
                # this entry has an implicit string concatenation
                'implicit': 'https://this-is-very-long.url-addr.com/'
                            '?something=something%20some%20more%20stuff..',
                # A more normal entry.
                '.....': 'this is an entry',
            }
        }
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB33047408(self):
    code = textwrap.dedent("""\
        def _():
          for sort in (sorts or []):
            request['sorts'].append({
                'field': {
                    'user_field': sort
                },
                'order': 'ASCENDING'
            })
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB32714745(self):
    code = textwrap.dedent("""\
        class _():

          def _BlankDefinition():
            '''Return a generic blank dictionary for a new field.'''
            return {
                'type': '',
                'validation': '',
                'name': 'fieldname',
                'label': 'Field Label',
                'help': '',
                'initial': '',
                'required': False,
                'required_msg': 'Required',
                'invalid_msg': 'Please enter a valid value',
                'options': {
                    'regex': '',
                    'widget_attr': '',
                    'choices_checked': '',
                    'choices_count': '',
                    'choices': {}
                },
                'isnew': True,
                'dirty': False,
            }
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB32737279(self):
    unformatted_code = textwrap.dedent("""\
        here_is_a_dict = {
            'key':
            # Comment.
            'value'
        }
        """)
    expected_formatted_code = textwrap.dedent("""\
        here_is_a_dict = {
            'key':  # Comment.
                'value'
        }
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB32570937(self):
    code = textwrap.dedent("""\
      def _():
        if (job_message.ball not in ('*', ball) or
            job_message.call not in ('*', call) or
            job_message.mall not in ('*', job_name)):
          return False
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB31937033(self):
    code = textwrap.dedent("""\
        class _():

          def __init__(self, metric, fields_cb=None):
            self._fields_cb = fields_cb or (lambda *unused_args, **unused_kwargs: {})
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB31911533(self):
    code = """\
class _():

  @parameterized.NamedParameters(
      ('IncludingModInfoWithHeaderList', AAAA, aaaa),
      ('IncludingModInfoWithoutHeaderList', BBBB, bbbbb),
      ('ExcludingModInfoWithHeaderList', CCCCC, cccc),
      ('ExcludingModInfoWithoutHeaderList', DDDDD, ddddd),
  )
  def _():
    pass
"""
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB31847238(self):
    unformatted_code = textwrap.dedent("""\
        class _():

          def aaaaa(self, bbbbb, cccccccccccccc=None):  # TODO(who): pylint: disable=unused-argument
            return 1

          def xxxxx(self, yyyyy, zzzzzzzzzzzzzz=None):  # A normal comment that runs over the column limit.
            return 1
        """)
    expected_formatted_code = textwrap.dedent("""\
        class _():

          def aaaaa(self, bbbbb, cccccccccccccc=None):  # TODO(who): pylint: disable=unused-argument
            return 1

          def xxxxx(
              self, yyyyy,
              zzzzzzzzzzzzzz=None):  # A normal comment that runs over the column limit.
            return 1
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB30760569(self):
    unformatted_code = textwrap.dedent("""\
        {'1234567890123456789012345678901234567890123456789012345678901234567890':
             '1234567890123456789012345678901234567890'}
        """)
    expected_formatted_code = textwrap.dedent("""\
        {
            '1234567890123456789012345678901234567890123456789012345678901234567890':
                '1234567890123456789012345678901234567890'
        }
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB26034238(self):
    unformatted_code = textwrap.dedent("""\
        class Thing:

          def Function(self):
            thing.Scrape('/aaaaaaaaa/bbbbbbbbbb/ccccc/dddd/eeeeeeeeeeeeee/ffffffffffffff').AndReturn(42)
        """)
    expected_formatted_code = textwrap.dedent("""\
        class Thing:

          def Function(self):
            thing.Scrape(
                '/aaaaaaaaa/bbbbbbbbbb/ccccc/dddd/eeeeeeeeeeeeee/ffffffffffffff'
            ).AndReturn(42)
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB30536435(self):
    unformatted_code = textwrap.dedent("""\
        def main(unused_argv):
          if True:
            if True:
              aaaaaaaaaaa.comment('import-from[{}] {} {}'.format(
                  bbbbbbbbb.usage,
                  ccccccccc.within,
                  imports.ddddddddddddddddddd(name_item.ffffffffffffffff)))
        """)
    expected_formatted_code = textwrap.dedent("""\
        def main(unused_argv):
          if True:
            if True:
              aaaaaaaaaaa.comment('import-from[{}] {} {}'.format(
                  bbbbbbbbb.usage, ccccccccc.within,
                  imports.ddddddddddddddddddd(name_item.ffffffffffffffff)))
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB30442148(self):
    unformatted_code = textwrap.dedent("""\
        def lulz():
          return (some_long_module_name.SomeLongClassName.
                  some_long_attribute_name.some_long_method_name())
        """)
    expected_formatted_code = textwrap.dedent("""\
        def lulz():
          return (some_long_module_name.SomeLongClassName.some_long_attribute_name.
                  some_long_method_name())
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB26868213(self):
    unformatted_code = textwrap.dedent("""\
      def _():
        xxxxxxxxxxxxxxxxxxx = {
            'ssssss': {'ddddd': 'qqqqq',
                       'p90': aaaaaaaaaaaaaaaaa,
                       'p99': bbbbbbbbbbbbbbbbb,
                       'lllllllllllll': yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy(),},
            'bbbbbbbbbbbbbbbbbbbbbbbbbbbb': {
                'ddddd': 'bork bork bork bo',
                'p90': wwwwwwwwwwwwwwwww,
                'p99': wwwwwwwwwwwwwwwww,
                'lllllllllllll': None,  # use the default
            }
        }
        """)
    expected_formatted_code = textwrap.dedent("""\
      def _():
        xxxxxxxxxxxxxxxxxxx = {
            'ssssss': {
                'ddddd': 'qqqqq',
                'p90': aaaaaaaaaaaaaaaaa,
                'p99': bbbbbbbbbbbbbbbbb,
                'lllllllllllll': yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy(),
            },
            'bbbbbbbbbbbbbbbbbbbbbbbbbbbb': {
                'ddddd': 'bork bork bork bo',
                'p90': wwwwwwwwwwwwwwwww,
                'p99': wwwwwwwwwwwwwwwww,
                'lllllllllllll': None,  # use the default
            }
        }
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB30173198(self):
    code = textwrap.dedent("""\
        class _():

          def _():
            self.assertFalse(
                evaluation_runner.get_larps_in_eval_set('these_arent_the_larps'))
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB29908765(self):
    code = textwrap.dedent("""\
        class _():

          def __repr__(self):
            return '<session %s on %s>' % (self._id,
                                           self._stub._stub.rpc_channel().target())  # pylint:disable=protected-access
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB30087362(self):
    code = textwrap.dedent("""\
        def _():
          for s in sorted(env['foo']):
            bar()
            # This is a comment

          # This is another comment
          foo()
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB30087363(self):
    code = textwrap.dedent("""\
        if False:
          bar()
          # This is a comment
        # This is another comment
        elif True:
          foo()
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB29093579(self):
    unformatted_code = textwrap.dedent("""\
        def _():
          _xxxxxxxxxxxxxxx(aaaaaaaa, bbbbbbbbbbbbbb.cccccccccc[
              dddddddddddddddddddddddddddd.eeeeeeeeeeeeeeeeeeeeee.fffffffffffffffffffff])
        """)
    expected_formatted_code = textwrap.dedent("""\
        def _():
          _xxxxxxxxxxxxxxx(
              aaaaaaaa,
              bbbbbbbbbbbbbb.cccccccccc[dddddddddddddddddddddddddddd.
                                        eeeeeeeeeeeeeeeeeeeeee.fffffffffffffffffffff])
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB26382315(self):
    code = textwrap.dedent("""\
        @hello_world
        # This is a first comment

        # Comment
        def foo():
          pass
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB27616132(self):
    unformatted_code = textwrap.dedent("""\
        if True:
          query.fetch_page.assert_has_calls([
              mock.call(100,
                        start_cursor=None),
              mock.call(100,
                        start_cursor=cursor_1),
              mock.call(100,
                        start_cursor=cursor_2),
          ])
        """)
    expected_formatted_code = textwrap.dedent("""\
        if True:
          query.fetch_page.assert_has_calls([
              mock.call(100, start_cursor=None),
              mock.call(100, start_cursor=cursor_1),
              mock.call(100, start_cursor=cursor_2),
          ])
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB27590179(self):
    unformatted_code = textwrap.dedent("""\
        if True:
          if True:
            self.aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa = (
                { True:
                     self.bbb.cccccccccc(ddddddddddddddddddddddd.eeeeeeeeeeeeeeeeeeeeee),
                 False:
                     self.bbb.cccccccccc(ddddddddddddddddddddddd.eeeeeeeeeeeeeeeeeeeeee)
                })
        """)
    expected_formatted_code = textwrap.dedent("""\
        if True:
          if True:
            self.aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa = ({
                True:
                    self.bbb.cccccccccc(ddddddddddddddddddddddd.eeeeeeeeeeeeeeeeeeeeee),
                False:
                    self.bbb.cccccccccc(ddddddddddddddddddddddd.eeeeeeeeeeeeeeeeeeeeee)
            })
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB27266946(self):
    unformatted_code = textwrap.dedent("""\
        def _():
          aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa = (self.bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb.cccccccccccccccccccccccccccccccccccc)
        """)
    expected_formatted_code = textwrap.dedent("""\
        def _():
          aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa = (
              self.bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb.
              cccccccccccccccccccccccccccccccccccc)
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB25505359(self):
    code = textwrap.dedent("""\
        _EXAMPLE = {
            'aaaaaaaaaaaaaa': [{
                'bbbb': 'cccccccccccccccccccccc',
                'dddddddddddd': []
            }, {
                'bbbb': 'ccccccccccccccccccc',
                'dddddddddddd': []
            }]
        }
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB25324261(self):
    code = textwrap.dedent("""\
        aaaaaaaaa = set(bbbb.cccc
                        for ddd in eeeeee.fffffffffff.gggggggggggggggg
                        for cccc in ddd.specification)
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB25136704(self):
    code = textwrap.dedent("""\
        class f:

          def test(self):
            self.bbbbbbb[0]['aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', {
                'xxxxxx': 'yyyyyy'
            }] = cccccc.ddd('1m', '10x1+1')
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB25165602(self):
    code = textwrap.dedent("""\
        def f():
          ids = {u: i for u, i in zip(self.aaaaa, xrange(42, 42 + len(self.aaaaaa)))}
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB25157123(self):
    code = textwrap.dedent("""\
        def ListArgs():
          FairlyLongMethodName([relatively_long_identifier_for_a_list],
                               another_argument_with_a_long_identifier)
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB25136820(self):
    unformatted_code = textwrap.dedent("""\
        def foo():
          return collections.OrderedDict({
              # Preceding comment.
              'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa':
              '$bbbbbbbbbbbbbbbbbbbbbbbb',
          })
        """)
    expected_formatted_code = textwrap.dedent("""\
        def foo():
          return collections.OrderedDict({
              # Preceding comment.
              'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa':
                  '$bbbbbbbbbbbbbbbbbbbbbbbb',
          })
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB25131481(self):
    unformatted_code = textwrap.dedent("""\
        APPARENT_ACTIONS = ('command_type', {
            'materialize': lambda x: some_type_of_function('materialize ' + x.command_def),
            '#': lambda x: x  # do nothing
        })
        """)
    expected_formatted_code = textwrap.dedent("""\
        APPARENT_ACTIONS = (
            'command_type',
            {
                'materialize':
                    lambda x: some_type_of_function('materialize ' + x.command_def),
                '#':
                    lambda x: x  # do nothing
            })
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB23445244(self):
    unformatted_code = textwrap.dedent("""\
        def foo():
          if True:
            return xxxxxxxxxxxxxxxx(
                command,
                extra_env={
                    "OOOOOOOOOOOOOOOOOOOOO": FLAGS.zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz,
                    "PPPPPPPPPPPPPPPPPPPPP":
                        FLAGS.aaaaaaaaaaaaaa + FLAGS.bbbbbbbbbbbbbbbbbbb,
                })
        """)
    expected_formatted_code = textwrap.dedent("""\
        def foo():
          if True:
            return xxxxxxxxxxxxxxxx(
                command,
                extra_env={
                    "OOOOOOOOOOOOOOOOOOOOO":
                        FLAGS.zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz,
                    "PPPPPPPPPPPPPPPPPPPPP":
                        FLAGS.aaaaaaaaaaaaaa + FLAGS.bbbbbbbbbbbbbbbbbbb,
                })
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB20559654(self):
    unformatted_code = textwrap.dedent("""\
      class A(object):

        def foo(self):
          unused_error, result = server.Query(
              ['AA BBBB CCC DDD EEEEEEEE X YY ZZZZ FFF EEE AAAAAAAA'],
              aaaaaaaaaaa=True, bbbbbbbb=None)
        """)
    expected_formatted_code = textwrap.dedent("""\
      class A(object):

        def foo(self):
          unused_error, result = server.Query(
              ['AA BBBB CCC DDD EEEEEEEE X YY ZZZZ FFF EEE AAAAAAAA'],
              aaaaaaaaaaa=True,
              bbbbbbbb=None)
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB23943842(self):
    unformatted_code = textwrap.dedent("""\
        class F():
          def f():
            self.assertDictEqual(
                accounts, {
                    'foo':
                    {'account': 'foo',
                     'lines': 'l1\\nl2\\nl3\\n1 line(s) were elided.'},
                    'bar': {'account': 'bar',
                            'lines': 'l5\\nl6\\nl7'},
                    'wiz': {'account': 'wiz',
                            'lines': 'l8'}
                })
        """)
    expected_formatted_code = textwrap.dedent("""\
        class F():

          def f():
            self.assertDictEqual(
                accounts, {
                    'foo': {
                        'account': 'foo',
                        'lines': 'l1\\nl2\\nl3\\n1 line(s) were elided.'
                    },
                    'bar': {
                        'account': 'bar',
                        'lines': 'l5\\nl6\\nl7'
                    },
                    'wiz': {
                        'account': 'wiz',
                        'lines': 'l8'
                    }
                })
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB20551180(self):
    unformatted_code = textwrap.dedent("""\
        def foo():
          if True:
            return (struct.pack('aaaa', bbbbbbbbbb, ccccccccccccccc, dddddddd) + eeeeeee)
        """)
    expected_formatted_code = textwrap.dedent("""\
        def foo():
          if True:
            return (
                struct.pack('aaaa', bbbbbbbbbb, ccccccccccccccc, dddddddd) + eeeeeee)
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB23944849(self):
    unformatted_code = textwrap.dedent("""\
        class A(object):
          def xxxxxxxxx(self, aaaaaaa, bbbbbbb=ccccccccccc, dddddd=300, eeeeeeeeeeeeee=None, fffffffffffffff=0):
            pass
        """)
    expected_formatted_code = textwrap.dedent("""\
        class A(object):

          def xxxxxxxxx(self,
                        aaaaaaa,
                        bbbbbbb=ccccccccccc,
                        dddddd=300,
                        eeeeeeeeeeeeee=None,
                        fffffffffffffff=0):
            pass
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB23935890(self):
    unformatted_code = textwrap.dedent("""\
        class F():
          def functioni(self, aaaaaaa, bbbbbbb, cccccc, dddddddddddddd, eeeeeeeeeeeeeee):
            pass
        """)
    expected_formatted_code = textwrap.dedent("""\
        class F():

          def functioni(self, aaaaaaa, bbbbbbb, cccccc, dddddddddddddd,
                        eeeeeeeeeeeeeee):
            pass
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB28414371(self):
    code = textwrap.dedent("""\
        def _():
          return ((m.fffff(
              m.rrr('mmmmmmmmmmmmmmmm', 'ssssssssssssssssssssssssss'), ffffffffffffffff)
                   | m.wwwwww(m.ddddd('1h'))
                   | m.ggggggg(bbbbbbbbbbbbbbb)
                   | m.ppppp(
                       (1 - m.ffffffffffffffff(llllllllllllllllllllll * 1000000, m.vvv))
                       * m.ddddddddddddddddd(m.vvv)),
                   m.fffff(
                       m.rrr('mmmmmmmmmmmmmmmm', 'sssssssssssssssssssssss'),
                       dict(
                           ffffffffffffffff, **{
                               'mmmmmm:ssssss':
                                   m.rrrrrrrrrrr('|'.join(iiiiiiiiiiiiii), iiiiii=True)
                           }))
                   | m.wwwwww(m.rrrr('1h'))
                   | m.ggggggg(bbbbbbbbbbbbbbb))
                  | m.jjjj()
                  | m.ppppp(m.vvv[0] + m.vvv[1]))
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB20127686(self):
    code = textwrap.dedent("""\
        def f():
          if True:
            return ((m.fffff(
                m.rrr('xxxxxxxxxxxxxxxx',
                      'yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy'),
                mmmmmmmm)
                     | m.wwwwww(m.rrrr(self.tttttttttt, self.mmmmmmmmmmmmmmmmmmmmm))
                     | m.ggggggg(self.gggggggg, m.sss()), m.fffff('aaaaaaaaaaaaaaaa')
                     | m.wwwwww(m.ddddd(self.tttttttttt, self.mmmmmmmmmmmmmmmmmmmmm))
                     | m.ggggggg(self.gggggggg))
                    | m.jjjj()
                    | m.ppppp(m.VAL[0] / m.VAL[1]))
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB20016122(self):
    try:
      style.SetGlobalStyle(
          style.CreateStyleFromConfig(
              '{based_on_style: pep8, split_penalty_import_names: 35}'))
      unformatted_code = textwrap.dedent("""\
          from a_very_long_or_indented_module_name_yada_yada import (long_argument_1,
                                                                     long_argument_2)
          """)
      expected_formatted_code = textwrap.dedent("""\
          from a_very_long_or_indented_module_name_yada_yada import (
              long_argument_1, long_argument_2)
          """)
      uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
      self.assertCodeEqual(expected_formatted_code,
                           reformatter.Reformat(uwlines))
    finally:
      style.SetGlobalStyle(style.CreatePEP8Style())

    try:
      style.SetGlobalStyle(
          style.CreateStyleFromConfig('{based_on_style: chromium, '
                                      'split_before_logical_operator: True}'))
      code = textwrap.dedent("""\
          class foo():

            def __eq__(self, other):
              return (isinstance(other, type(self))
                      and self.xxxxxxxxxxx == other.xxxxxxxxxxx
                      and self.xxxxxxxx == other.xxxxxxxx
                      and self.aaaaaaaaaaaa == other.aaaaaaaaaaaa
                      and self.bbbbbbbbbbb == other.bbbbbbbbbbb
                      and self.ccccccccccccccccc == other.ccccccccccccccccc
                      and self.ddddddddddddddddddddddd == other.ddddddddddddddddddddddd
                      and self.eeeeeeeeeeee == other.eeeeeeeeeeee
                      and self.ffffffffffffff == other.time_completed
                      and self.gggggg == other.gggggg and self.hhh == other.hhh
                      and len(self.iiiiiiii) == len(other.iiiiiiii)
                      and all(jjjjjjj in other.iiiiiiii for jjjjjjj in self.iiiiiiii))
          """)
      uwlines = yapf_test_helper.ParseAndUnwrap(code)
      self.assertCodeEqual(code, reformatter.Reformat(uwlines))
    finally:
      style.SetGlobalStyle(style.CreateChromiumStyle())

  def testB22527411(self):
    unformatted_code = textwrap.dedent("""\
        def f():
          if True:
            aaaaaa.bbbbbbbbbbbbbbbbbbbb[-1].cccccccccccccc.ddd().eeeeeeee(ffffffffffffff)
        """)
    expected_formatted_code = textwrap.dedent("""\
        def f():
          if True:
            aaaaaa.bbbbbbbbbbbbbbbbbbbb[-1].cccccccccccccc.ddd().eeeeeeee(
                ffffffffffffff)
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB20849933(self):
    unformatted_code = textwrap.dedent("""\
        def main(unused_argv):
          if True:
            aaaaaaaa = {
                'xxx': '%s/cccccc/ddddddddddddddddddd.jar' %
                       (eeeeee.FFFFFFFFFFFFFFFFFF),
            }
        """)
    expected_formatted_code = textwrap.dedent("""\
        def main(unused_argv):
          if True:
            aaaaaaaa = {
                'xxx':
                    '%s/cccccc/ddddddddddddddddddd.jar' % (eeeeee.FFFFFFFFFFFFFFFFFF),
            }
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB20813997(self):
    code = textwrap.dedent("""\
        def myfunc_1():
          myarray = numpy.zeros((2, 2, 2))
          print(myarray[:, 1, :])
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB20605036(self):
    code = textwrap.dedent("""\
        foo = {
            'aaaa': {
                # A comment for no particular reason.
                'xxxxxxxx': 'bbbbbbbbb',
                'yyyyyyyyyyyyyyyyyy': 'cccccccccccccccccccccccccccccc'
                                      'dddddddddddddddddddddddddddddddddddddddddd',
            }
        }
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB20562732(self):
    code = textwrap.dedent("""\
        foo = [
            # Comment about first list item
            'First item',
            # Comment about second list item
            'Second item',
        ]
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB20128830(self):
    code = textwrap.dedent("""\
        a = {
            'xxxxxxxxxxxxxxxxxxxx': {
                'aaaa':
                    'mmmmmmm',
                'bbbbb':
                    'mmmmmmmmmmmmmmmmmmmmm',
                'cccccccccc': [
                    'nnnnnnnnnnn',
                    'ooooooooooo',
                    'ppppppppppp',
                    'qqqqqqqqqqq',
                ],
            },
        }
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB20073838(self):
    code = textwrap.dedent("""\
        class DummyModel(object):

          def do_nothing(self, class_1_count):
            if True:
              class_0_count = num_votes - class_1_count
              return ('{class_0_name}={class_0_count}, {class_1_name}={class_1_count}'
                      .format(
                          class_0_name=self.class_0_name,
                          class_0_count=class_0_count,
                          class_1_name=self.class_1_name,
                          class_1_count=class_1_count))
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB19626808(self):
    code = textwrap.dedent("""\
        if True:
          aaaaaaaaaaaaaaaaaaaaaaa.bbbbbbbbb(
              'ccccccccccc', ddddddddd='eeeee').fffffffff([ggggggggggggggggggggg])
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB19547210(self):
    code = textwrap.dedent("""\
        while True:
          if True:
            if True:
              if True:
                if xxxxxxxxxxxx.yyyyyyy(aa).zzzzzzz() not in (
                    xxxxxxxxxxxx.yyyyyyyyyyyyyy.zzzzzzzz,
                    xxxxxxxxxxxx.yyyyyyyyyyyyyy.zzzzzzzz):
                  continue
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB19377034(self):
    code = textwrap.dedent("""\
        def f():
          if (aaaaaaaaaaaaaaa.start >= aaaaaaaaaaaaaaa.end or
              bbbbbbbbbbbbbbb.start >= bbbbbbbbbbbbbbb.end):
            return False
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB19372573(self):
    code = textwrap.dedent("""\
        def f():
            if a: return 42
            while True:
                if b: continue
                if c: break
            return 0
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    try:
      style.SetGlobalStyle(style.CreatePEP8Style())
      self.assertCodeEqual(code, reformatter.Reformat(uwlines))
    finally:
      style.SetGlobalStyle(style.CreateChromiumStyle())

  def testB19353268(self):
    code = textwrap.dedent("""\
        a = {1, 2, 3}[x]
        b = {'foo': 42, 'bar': 37}['foo']
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB19287512(self):
    unformatted_code = textwrap.dedent("""\
        class Foo(object):

          def bar(self):
            with xxxxxxxxxx.yyyyy(
                'aaaaaaa.bbbbbbbb.ccccccc.dddddddddddddddddddd.eeeeeeeeeee',
                fffffffffff=(aaaaaaa.bbbbbbbb.ccccccc.dddddddddddddddddddd
                             .Mmmmmmmmmmmmmmmmmm(-1, 'permission error'))):
              self.assertRaises(nnnnnnnnnnnnnnnn.ooooo, ppppp.qqqqqqqqqqqqqqqqq)
        """)
    expected_formatted_code = textwrap.dedent("""\
        class Foo(object):

          def bar(self):
            with xxxxxxxxxx.yyyyy(
                'aaaaaaa.bbbbbbbb.ccccccc.dddddddddddddddddddd.eeeeeeeeeee',
                fffffffffff=(
                    aaaaaaa.bbbbbbbb.ccccccc.dddddddddddddddddddd.Mmmmmmmmmmmmmmmmmm(
                        -1, 'permission error'))):
              self.assertRaises(nnnnnnnnnnnnnnnn.ooooo, ppppp.qqqqqqqqqqqqqqqqq)
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB19194420(self):
    code = textwrap.dedent("""\
        method.Set(
            'long argument goes here that causes the line to break',
            lambda arg2=0.5: arg2)
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB19073499(self):
    code = """\
instance = (
    aaaaaaa.bbbbbbb().ccccccccccccccccc().ddddddddddd({
        'aa': 'context!'
    }).eeeeeeeeeeeeeeeeeee({  # Inline comment about why fnord has the value 6.
        'fnord': 6
    }))
"""
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB18257115(self):
    code = textwrap.dedent("""\
        if True:
          if True:
            self._Test(aaaa, bbbbbbb.cccccccccc, dddddddd, eeeeeeeeeee,
                       [ffff, ggggggggggg, hhhhhhhhhhhh, iiiiii, jjjj])
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB18256666(self):
    code = textwrap.dedent("""\
        class Foo(object):

          def Bar(self):
            aaaaa.bbbbbbb(
                ccc='ddddddddddddddd',
                eeee='ffffffffffffffffffffff-%s-%s' % (gggg, int(time.time())),
                hhhhhh={
                    'iiiiiiiiiii': iiiiiiiiiii,
                    'jjjj': jjjj.jjjjj(),
                    'kkkkkkkkkkkk': kkkkkkkkkkkk,
                },
                llllllllll=mmmmmm.nnnnnnnnnnnnnnnn)
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB18256826(self):
    code = textwrap.dedent("""\
        if True:
          pass
        # A multiline comment.
        # Line two.
        elif False:
          pass

        if True:
          pass
          # A multiline comment.
          # Line two.
        elif False:
          pass
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB18255697(self):
    code = textwrap.dedent("""\
        AAAAAAAAAAAAAAA = {
            'XXXXXXXXXXXXXX': 4242,  # Inline comment
            # Next comment
            'YYYYYYYYYYYYYYYY': ['zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz'],
        }
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

  def testB17534869(self):
    unformatted_code = textwrap.dedent("""\
        if True:
          self.assertLess(abs(time.time()-aaaa.bbbbbbbbbbb(
                              datetime.datetime.now())), 1)
        """)
    expected_formatted_code = textwrap.dedent("""\
        if True:
          self.assertLess(
              abs(time.time() - aaaa.bbbbbbbbbbb(datetime.datetime.now())), 1)
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB17489866(self):
    unformatted_code = textwrap.dedent("""\
        def f():
          if True:
            if True:
              return aaaa.bbbbbbbbb(ccccccc=dddddddddddddd({('eeee', \
'ffffffff'): str(j)}))
        """)
    expected_formatted_code = textwrap.dedent("""\
        def f():
          if True:
            if True:
              return aaaa.bbbbbbbbb(
                  ccccccc=dddddddddddddd({
                      ('eeee', 'ffffffff'): str(j)
                  }))
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB17133019(self):
    unformatted_code = textwrap.dedent("""\
        class aaaaaaaaaaaaaa(object):

          def bbbbbbbbbb(self):
            with io.open("/dev/null", "rb"):
              with io.open(os.path.join(aaaaa.bbbbb.ccccccccccc,
                                        DDDDDDDDDDDDDDD,
                                        "eeeeeeeee ffffffffff"
                                       ), "rb") as gggggggggggggggggggg:
                print(gggggggggggggggggggg)
        """)
    expected_formatted_code = textwrap.dedent("""\
        class aaaaaaaaaaaaaa(object):

          def bbbbbbbbbb(self):
            with io.open("/dev/null", "rb"):
              with io.open(
                  os.path.join(aaaaa.bbbbb.ccccccccccc, DDDDDDDDDDDDDDD,
                               "eeeeeeeee ffffffffff"), "rb") as gggggggggggggggggggg:
                print(gggggggggggggggggggg)
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB17011869(self):
    unformatted_code = textwrap.dedent("""\
        '''blah......'''

        class SomeClass(object):
          '''blah.'''

          AAAAAAAAAAAA = {                        # Comment.
              'BBB': 1.0,
                'DDDDDDDD': 0.4811
                                      }
        """)
    expected_formatted_code = textwrap.dedent("""\
        '''blah......'''


        class SomeClass(object):
          '''blah.'''

          AAAAAAAAAAAA = {  # Comment.
              'BBB': 1.0,
              'DDDDDDDD': 0.4811
          }
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB16783631(self):
    unformatted_code = textwrap.dedent("""\
        if True:
          with aaaaaaaaaaaaaa.bbbbbbbbbbbbb.ccccccc(ddddddddddddd,
                                                      eeeeeeeee=self.fffffffffffff
                                                      )as gggg:
            pass
        """)
    expected_formatted_code = textwrap.dedent("""\
        if True:
          with aaaaaaaaaaaaaa.bbbbbbbbbbbbb.ccccccc(
              ddddddddddddd, eeeeeeeee=self.fffffffffffff) as gggg:
            pass
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB16572361(self):
    unformatted_code = textwrap.dedent("""\
        def foo(self):
         def bar(my_dict_name):
          self.my_dict_name['foo-bar-baz-biz-boo-baa-baa'].IncrementBy.assert_called_once_with('foo_bar_baz_boo')
        """)
    expected_formatted_code = textwrap.dedent("""\
        def foo(self):

          def bar(my_dict_name):
            self.my_dict_name[
                'foo-bar-baz-biz-boo-baa-baa'].IncrementBy.assert_called_once_with(
                    'foo_bar_baz_boo')
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB15884241(self):
    unformatted_code = textwrap.dedent("""\
        if 1:
          if 1:
            for row in AAAA:
              self.create(aaaaaaaa="/aaa/bbbb/cccc/dddddd/eeeeeeeeeeeeeeeeeeeeeeeeee/%s" % row [0].replace(".foo", ".bar"), aaaaa=bbb[1], ccccc=bbb[2], dddd=bbb[3], eeeeeeeeeee=[s.strip() for s in bbb[4].split(",")], ffffffff=[s.strip() for s in bbb[5].split(",")], gggggg=bbb[6])
        """)
    expected_formatted_code = textwrap.dedent("""\
        if 1:
          if 1:
            for row in AAAA:
              self.create(
                  aaaaaaaa="/aaa/bbbb/cccc/dddddd/eeeeeeeeeeeeeeeeeeeeeeeeee/%s" %
                  row[0].replace(".foo", ".bar"),
                  aaaaa=bbb[1],
                  ccccc=bbb[2],
                  dddd=bbb[3],
                  eeeeeeeeeee=[s.strip() for s in bbb[4].split(",")],
                  ffffffff=[s.strip() for s in bbb[5].split(",")],
                  gggggg=bbb[6])
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB15697268(self):
    unformatted_code = textwrap.dedent("""\
        def main(unused_argv):
          ARBITRARY_CONSTANT_A = 10
          an_array_with_an_exceedingly_long_name = range(ARBITRARY_CONSTANT_A + 1)
          ok = an_array_with_an_exceedingly_long_name[:ARBITRARY_CONSTANT_A]
          bad_slice = map(math.sqrt, an_array_with_an_exceedingly_long_name[:ARBITRARY_CONSTANT_A])
          a_long_name_slicing = an_array_with_an_exceedingly_long_name[:ARBITRARY_CONSTANT_A]
          bad_slice = ("I am a crazy, no good, string whats too long, etc." + " no really ")[:ARBITRARY_CONSTANT_A]
        """)
    expected_formatted_code = textwrap.dedent("""\
        def main(unused_argv):
          ARBITRARY_CONSTANT_A = 10
          an_array_with_an_exceedingly_long_name = range(ARBITRARY_CONSTANT_A + 1)
          ok = an_array_with_an_exceedingly_long_name[:ARBITRARY_CONSTANT_A]
          bad_slice = map(math.sqrt,
                          an_array_with_an_exceedingly_long_name[:ARBITRARY_CONSTANT_A])
          a_long_name_slicing = an_array_with_an_exceedingly_long_name[:
                                                                       ARBITRARY_CONSTANT_A]
          bad_slice = ("I am a crazy, no good, string whats too long, etc." +
                       " no really ")[:ARBITRARY_CONSTANT_A]
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB15597568(self):
    unformatted_code = textwrap.dedent("""\
        if True:
          if True:
            if True:
              print(("Return code was %d" + (", and the process timed out." if did_time_out else ".")) % errorcode)
        """)
    expected_formatted_code = textwrap.dedent("""\
        if True:
          if True:
            if True:
              print(("Return code was %d" + (", and the process timed out."
                                             if did_time_out else ".")) % errorcode)
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB15542157(self):
    unformatted_code = textwrap.dedent("""\
        aaaaaaaaaaaa = bbbb.ccccccccccccccc(dddddd.eeeeeeeeeeeeee, ffffffffffffffffff, gggggg.hhhhhhhhhhhhhhhhh)
        """)
    expected_formatted_code = textwrap.dedent("""\
        aaaaaaaaaaaa = bbbb.ccccccccccccccc(dddddd.eeeeeeeeeeeeee, ffffffffffffffffff,
                                            gggggg.hhhhhhhhhhhhhhhhh)
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB15438132(self):
    unformatted_code = textwrap.dedent("""\
        if aaaaaaa.bbbbbbbbbb:
           cccccc.dddddddddd(eeeeeeeeeee=fffffffffffff.gggggggggggggggggg)
           if hhhhhh.iiiii.jjjjjjjjjjjjj:
             # This is a comment in the middle of it all.
             kkkkkkk.llllllllll.mmmmmmmmmmmmm = True
           if (aaaaaa.bbbbb.ccccccccccccc != ddddddd.eeeeeeeeee.fffffffffffff or
               eeeeee.fffff.ggggggggggggggggggggggggggg() != hhhhhhh.iiiiiiiiii.jjjjjjjjjjjj):
             aaaaaaaa.bbbbbbbbbbbb(
                 aaaaaa.bbbbb.cc,
                 dddddddddddd=eeeeeeeeeeeeeeeeeee.fffffffffffffffff(
                     gggggg.hh,
                     iiiiiiiiiiiiiiiiiii.jjjjjjjjjj.kkkkkkk,
                     lllll.mm),
                 nnnnnnnnnn=ooooooo.pppppppppp)
        """)
    expected_formatted_code = textwrap.dedent("""\
        if aaaaaaa.bbbbbbbbbb:
          cccccc.dddddddddd(eeeeeeeeeee=fffffffffffff.gggggggggggggggggg)
          if hhhhhh.iiiii.jjjjjjjjjjjjj:
            # This is a comment in the middle of it all.
            kkkkkkk.llllllllll.mmmmmmmmmmmmm = True
          if (aaaaaa.bbbbb.ccccccccccccc != ddddddd.eeeeeeeeee.fffffffffffff or
              eeeeee.fffff.ggggggggggggggggggggggggggg() !=
              hhhhhhh.iiiiiiiiii.jjjjjjjjjjjj):
            aaaaaaaa.bbbbbbbbbbbb(
                aaaaaa.bbbbb.cc,
                dddddddddddd=eeeeeeeeeeeeeeeeeee.fffffffffffffffff(
                    gggggg.hh, iiiiiiiiiiiiiiiiiii.jjjjjjjjjj.kkkkkkk, lllll.mm),
                nnnnnnnnnn=ooooooo.pppppppppp)
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB14468247(self):
    unformatted_code = """\
call(a=1,
    b=2,
)
"""
    expected_formatted_code = """\
call(
    a=1,
    b=2,
)
"""
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB14406499(self):
    unformatted_code = textwrap.dedent("""\
        def foo1(parameter_1, parameter_2, parameter_3, parameter_4, \
parameter_5, parameter_6): pass
        """)
    expected_formatted_code = textwrap.dedent("""\
        def foo1(parameter_1, parameter_2, parameter_3, parameter_4, parameter_5,
                 parameter_6):
          pass
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB13900309(self):
    unformatted_code = textwrap.dedent("""\
        self.aaaaaaaaaaa(  # A comment in the middle of it all.
               948.0/3600, self.bbb.ccccccccccccccccccccc(dddddddddddddddd.eeee, True))
        """)
    expected_formatted_code = textwrap.dedent("""\
        self.aaaaaaaaaaa(  # A comment in the middle of it all.
            948.0 / 3600, self.bbb.ccccccccccccccccccccc(dddddddddddddddd.eeee, True))
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

    code = textwrap.dedent("""\
        aaaaaaaaaa.bbbbbbbbbbbbbbbbbbbbbbbb.cccccccccccccccccccccccccccccc(
            DC_1, (CL - 50, CL), AAAAAAAA, BBBBBBBBBBBBBBBB, 98.0,
            CCCCCCC).ddddddddd(  # Look! A comment is here.
                AAAAAAAA - (20 * 60 - 5))
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

    unformatted_code = textwrap.dedent("""\
        aaaaaaaaaaaaaaaaaaaaaaaa.bbbbbbbbbbbbb.ccccccccccccccccccccccccc().dddddddddddddddddddddddddd(1, 2, 3, 4)
        """)
    expected_formatted_code = textwrap.dedent("""\
        aaaaaaaaaaaaaaaaaaaaaaaa.bbbbbbbbbbbbb.ccccccccccccccccccccccccc(
        ).dddddddddddddddddddddddddd(1, 2, 3, 4)
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

    unformatted_code = textwrap.dedent("""\
        aaaaaaaaaaaaaaaaaaaaaaaa.bbbbbbbbbbbbb.ccccccccccccccccccccccccc(x).dddddddddddddddddddddddddd(1, 2, 3, 4)
        """)
    expected_formatted_code = textwrap.dedent("""\
        aaaaaaaaaaaaaaaaaaaaaaaa.bbbbbbbbbbbbb.ccccccccccccccccccccccccc(
            x).dddddddddddddddddddddddddd(1, 2, 3, 4)
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

    unformatted_code = textwrap.dedent("""\
        aaaaaaaaaaaaaaaaaaaaaaaa(xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx).dddddddddddddddddddddddddd(1, 2, 3, 4)
        """)
    expected_formatted_code = textwrap.dedent("""\
        aaaaaaaaaaaaaaaaaaaaaaaa(
            xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx).dddddddddddddddddddddddddd(1, 2, 3, 4)
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

    unformatted_code = textwrap.dedent("""\
        aaaaaaaaaaaaaaaaaaaaaaaa().bbbbbbbbbbbbbbbbbbbbbbbb().ccccccccccccccccccc().\
dddddddddddddddddd().eeeeeeeeeeeeeeeeeeeee().fffffffffffffffff().gggggggggggggggggg()
        """)
    expected_formatted_code = textwrap.dedent("""\
        aaaaaaaaaaaaaaaaaaaaaaaa().bbbbbbbbbbbbbbbbbbbbbbbb().ccccccccccccccccccc(
        ).dddddddddddddddddd().eeeeeeeeeeeeeeeeeeeee().fffffffffffffffff(
        ).gggggggggggggggggg()
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))

  def testB67935687(self):
    code = textwrap.dedent("""\
        Fetch(
            Raw('monarch.BorgTask', '/union/row_operator_action_delay'),
            {'borg_user': self.borg_user})
    """)
    uwlines = yapf_test_helper.ParseAndUnwrap(code)
    self.assertCodeEqual(code, reformatter.Reformat(uwlines))

    unformatted_code = textwrap.dedent("""\
        shelf_renderer.expand_text = text.translate_to_unicode(
            expand_text % {
                'creator': creator
            })
        """)
    expected_formatted_code = textwrap.dedent("""\
        shelf_renderer.expand_text = text.translate_to_unicode(
            expand_text % {'creator': creator})
        """)
    uwlines = yapf_test_helper.ParseAndUnwrap(unformatted_code)
    self.assertCodeEqual(expected_formatted_code, reformatter.Reformat(uwlines))


if __name__ == '__main__':
  unittest.main()

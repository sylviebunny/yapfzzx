# -*- coding: utf-8 -*-
# Copyright 2015 Google Inc. All Rights Reserved.
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
"""Tests for yapf.yapf."""

import io
import logging
import os
import shutil
import subprocess
import sys
import tempfile
import textwrap
import unittest

from yapf.yapflib import py3compat
from yapf.yapflib import style
from yapf.yapflib import yapf_api

from yapftests import utils

ROOT_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))

# Verification is turned off by default, but want to enable it for testing.
YAPF_BINARY = [sys.executable, '-m', 'yapf', '--verify', '--no-local-style']


class FormatCodeTest(unittest.TestCase):

  def _Check(self, unformatted_code, expected_formatted_code):
    formatted_code, _ = yapf_api.FormatCode(
        unformatted_code, style_config='chromium')
    self.assertEqual(expected_formatted_code, formatted_code)

  def testSimple(self):
    unformatted_code = textwrap.dedent("""\
        print('foo')
        """)
    self._Check(unformatted_code, unformatted_code)

  def testNoEndingNewline(self):
    unformatted_code = textwrap.dedent("""\
        if True:
          pass""")
    expected_formatted_code = textwrap.dedent("""\
        if True:
          pass
        """)
    self._Check(unformatted_code, expected_formatted_code)


class FormatFileTest(unittest.TestCase):

  def setUp(self):
    self.test_tmpdir = tempfile.mkdtemp()

  def tearDown(self):
    shutil.rmtree(self.test_tmpdir)

  def assertCodeEqual(self, expected_code, code):
    if code != expected_code:
      msg = 'Code format mismatch:\n'
      msg += 'Expected:\n >'
      msg += '\n > '.join(expected_code.splitlines())
      msg += '\nActual:\n >'
      msg += '\n > '.join(code.splitlines())
      # TODO(sbc): maybe using difflib here to produce easy to read deltas?
      self.fail(msg)

  def testFormatFile(self):
    unformatted_code = textwrap.dedent(u"""\
        if True:
         pass
        """)
    expected_formatted_code_pep8 = textwrap.dedent(u"""\
        if True:
            pass
        """)
    expected_formatted_code_chromium = textwrap.dedent(u"""\
        if True:
          pass
        """)
    with utils.TempFileContents(self.test_tmpdir, unformatted_code) as filepath:
      formatted_code, _, _ = yapf_api.FormatFile(filepath, style_config='pep8')
      self.assertCodeEqual(expected_formatted_code_pep8, formatted_code)

      formatted_code, _, _ = yapf_api.FormatFile(
          filepath, style_config='chromium')
      self.assertCodeEqual(expected_formatted_code_chromium, formatted_code)

  def testDisableLinesPattern(self):
    unformatted_code = textwrap.dedent(u"""\
        if a:    b

        # yapf: disable
        if f:    g

        if h:    i
        """)
    expected_formatted_code = textwrap.dedent(u"""\
        if a: b

        # yapf: disable
        if f:    g

        if h:    i
        """)
    with utils.TempFileContents(self.test_tmpdir, unformatted_code) as filepath:
      formatted_code, _, _ = yapf_api.FormatFile(filepath, style_config='pep8')
      self.assertCodeEqual(expected_formatted_code, formatted_code)

  def testDisableAndReenableLinesPattern(self):
    unformatted_code = textwrap.dedent(u"""\
        if a:    b

        # yapf: disable
        if f:    g
        # yapf: enable

        if h:    i
        """)
    expected_formatted_code = textwrap.dedent(u"""\
        if a: b

        # yapf: disable
        if f:    g
        # yapf: enable

        if h: i
        """)
    with utils.TempFileContents(self.test_tmpdir, unformatted_code) as filepath:
      formatted_code, _, _ = yapf_api.FormatFile(filepath, style_config='pep8')
      self.assertCodeEqual(expected_formatted_code, formatted_code)

  def testDisablePartOfMultilineComment(self):
    unformatted_code = textwrap.dedent(u"""\
        if a:    b

        # This is a multiline comment that disables YAPF.
        # yapf: disable
        if f:    g
        # yapf: enable
        # This is a multiline comment that enables YAPF.

        if h:    i
        """)

    expected_formatted_code = textwrap.dedent(u"""\
        if a: b

        # This is a multiline comment that disables YAPF.
        # yapf: disable
        if f:    g
        # yapf: enable
        # This is a multiline comment that enables YAPF.

        if h: i
        """)
    with utils.TempFileContents(self.test_tmpdir, unformatted_code) as filepath:
      formatted_code, _, _ = yapf_api.FormatFile(filepath, style_config='pep8')
      self.assertCodeEqual(expected_formatted_code, formatted_code)

    code = textwrap.dedent(u"""\
      def foo_function():
          # some comment
          # yapf: disable

          foo(
          bar,
          baz
          )

          # yapf: enable
      """)
    with utils.TempFileContents(self.test_tmpdir, code) as filepath:
      formatted_code, _, _ = yapf_api.FormatFile(filepath, style_config='pep8')
      self.assertCodeEqual(code, formatted_code)

  def testFormatFileLinesSelection(self):
    unformatted_code = textwrap.dedent(u"""\
        if a:    b

        if f:    g

        if h:    i
        """)
    expected_formatted_code_lines1and2 = textwrap.dedent(u"""\
        if a: b

        if f:    g

        if h:    i
        """)
    expected_formatted_code_lines3 = textwrap.dedent(u"""\
        if a:    b

        if f: g

        if h:    i
        """)
    with utils.TempFileContents(self.test_tmpdir, unformatted_code) as filepath:
      formatted_code, _, _ = yapf_api.FormatFile(
          filepath, style_config='pep8', lines=[(1, 2)])
      self.assertCodeEqual(expected_formatted_code_lines1and2, formatted_code)
      formatted_code, _, _ = yapf_api.FormatFile(
          filepath, style_config='pep8', lines=[(3, 3)])
      self.assertCodeEqual(expected_formatted_code_lines3, formatted_code)

  def testFormatFileDiff(self):
    unformatted_code = textwrap.dedent(u"""\
        if True:
         pass
        """)
    with utils.TempFileContents(self.test_tmpdir, unformatted_code) as filepath:
      diff, _, _ = yapf_api.FormatFile(filepath, print_diff=True)
      self.assertTrue(u'+  pass' in diff)

  def testFormatFileInPlace(self):
    unformatted_code = u'True==False\n'
    formatted_code = u'True == False\n'
    with utils.TempFileContents(self.test_tmpdir, unformatted_code) as filepath:
      result, _, _ = yapf_api.FormatFile(filepath, in_place=True)
      self.assertEqual(result, None)
      with open(filepath) as fd:
        if sys.version_info[0] <= 2:
          self.assertCodeEqual(formatted_code, fd.read().decode('ascii'))
        else:
          self.assertCodeEqual(formatted_code, fd.read())

      self.assertRaises(
          ValueError,
          yapf_api.FormatFile,
          filepath,
          in_place=True,
          print_diff=True)

  def testNoFile(self):
    stream = py3compat.StringIO()
    handler = logging.StreamHandler(stream)
    logger = logging.getLogger('mylogger')
    logger.addHandler(handler)
    self.assertRaises(
        IOError, yapf_api.FormatFile, 'not_a_file.py', logger=logger.error)
    self.assertEqual(stream.getvalue(),
                     "[Errno 2] No such file or directory: 'not_a_file.py'\n")

  def testCommentsUnformatted(self):
    code = textwrap.dedent(u"""\
        foo = [# A list of things
               # bork
            'one',
            # quark
            'two'] # yapf: disable
        """)
    with utils.TempFileContents(self.test_tmpdir, code) as filepath:
      formatted_code, _, _ = yapf_api.FormatFile(filepath, style_config='pep8')
      self.assertCodeEqual(code, formatted_code)

  def testDisabledHorizontalFormattingOnNewLine(self):
    code = textwrap.dedent(u"""\
        # yapf: disable
        a = [
        1]
        # yapf: enable
        """)
    with utils.TempFileContents(self.test_tmpdir, code) as filepath:
      formatted_code, _, _ = yapf_api.FormatFile(filepath, style_config='pep8')
      self.assertCodeEqual(code, formatted_code)

  def testSplittingSemicolonStatements(self):
    unformatted_code = textwrap.dedent(u"""\
        def f():
          x = y + 42 ; z = n * 42
          if True: a += 1 ; b += 1; c += 1
        """)
    expected_formatted_code = textwrap.dedent(u"""\
        def f():
            x = y + 42
            z = n * 42
            if True:
                a += 1
                b += 1
                c += 1
        """)
    with utils.TempFileContents(self.test_tmpdir, unformatted_code) as filepath:
      formatted_code, _, _ = yapf_api.FormatFile(filepath, style_config='pep8')
      self.assertCodeEqual(expected_formatted_code, formatted_code)

  def testSemicolonStatementsDisabled(self):
    unformatted_code = textwrap.dedent(u"""\
        def f():
          x = y + 42 ; z = n * 42  # yapf: disable
          if True: a += 1 ; b += 1; c += 1
        """)
    expected_formatted_code = textwrap.dedent(u"""\
        def f():
            x = y + 42 ; z = n * 42  # yapf: disable
            if True:
                a += 1
                b += 1
                c += 1
        """)
    with utils.TempFileContents(self.test_tmpdir, unformatted_code) as filepath:
      formatted_code, _, _ = yapf_api.FormatFile(filepath, style_config='pep8')
      self.assertCodeEqual(expected_formatted_code, formatted_code)

  def testDisabledSemiColonSeparatedStatements(self):
    code = textwrap.dedent(u"""\
        # yapf: disable
        if True: a ; b
        """)
    with utils.TempFileContents(self.test_tmpdir, code) as filepath:
      formatted_code, _, _ = yapf_api.FormatFile(filepath, style_config='pep8')
      self.assertCodeEqual(code, formatted_code)

  def testDisabledMultilineStringInDictionary(self):
    code = textwrap.dedent(u"""\
        # yapf: disable

        A = [
            {
                "aaaaaaaaaaaaaaaaaaa": '''
        bbbbbbbbbbb: "ccccccccccc"
        dddddddddddddd: 1
        eeeeeeee: 0
        ffffffffff: "ggggggg"
        ''',
            },
        ]
        """)
    with utils.TempFileContents(self.test_tmpdir, code) as filepath:
      formatted_code, _, _ = yapf_api.FormatFile(
          filepath, style_config='chromium')
      self.assertCodeEqual(code, formatted_code)

  def testDisabledWithPrecedingText(self):
    code = textwrap.dedent(u"""\
        # TODO(fix formatting): yapf: disable

        A = [
            {
                "aaaaaaaaaaaaaaaaaaa": '''
        bbbbbbbbbbb: "ccccccccccc"
        dddddddddddddd: 1
        eeeeeeee: 0
        ffffffffff: "ggggggg"
        ''',
            },
        ]
        """)
    with utils.TempFileContents(self.test_tmpdir, code) as filepath:
      formatted_code, _, _ = yapf_api.FormatFile(
          filepath, style_config='chromium')
      self.assertCodeEqual(code, formatted_code)

  def testCRLFLineEnding(self):
    code = u'class _():\r\n  pass\r\n'
    with utils.TempFileContents(self.test_tmpdir, code) as filepath:
      formatted_code, _, _ = yapf_api.FormatFile(
          filepath, style_config='chromium')
      self.assertCodeEqual(code, formatted_code)


class CommandLineTest(unittest.TestCase):
  """Test how calling yapf from the command line acts."""

  @classmethod
  def setUpClass(cls):
    cls.test_tmpdir = tempfile.mkdtemp()

  @classmethod
  def tearDownClass(cls):
    shutil.rmtree(cls.test_tmpdir)

  def assertYapfReformats(self,
                          unformatted,
                          expected,
                          extra_options=None,
                          env=None):
    """Check that yapf reformats the given code as expected.

    Invokes yapf in a subprocess, piping the unformatted code into its stdin.
    Checks that the formatted output is as expected.

    Arguments:
      unformatted: unformatted code - input to yapf
      expected: expected formatted code at the output of yapf
      extra_options: iterable of extra command-line options to pass to yapf
      env: dict of environment variables.
    """
    cmdline = YAPF_BINARY + (extra_options or [])
    p = subprocess.Popen(
        cmdline,
        stdout=subprocess.PIPE,
        stdin=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env)
    reformatted_code, stderrdata = p.communicate(unformatted.encode('utf-8'))
    self.assertEqual(stderrdata, b'')
    self.assertMultiLineEqual(reformatted_code.decode('utf-8'), expected)

  def testUnicodeEncodingPipedToFile(self):
    unformatted_code = textwrap.dedent(u"""\
        def foo():
            print('⇒')
        """)
    with utils.NamedTempFile(
        dirname=self.test_tmpdir, suffix='.py') as (out, _):
      with utils.TempFileContents(
          self.test_tmpdir, unformatted_code, suffix='.py') as filepath:
        subprocess.check_call(YAPF_BINARY + ['--diff', filepath], stdout=out)

  def testInPlaceReformatting(self):
    unformatted_code = textwrap.dedent(u"""\
        def foo():
          x = 37
        """)
    expected_formatted_code = textwrap.dedent("""\
        def foo():
            x = 37
        """)
    with utils.TempFileContents(
        self.test_tmpdir, unformatted_code, suffix='.py') as filepath:
      p = subprocess.Popen(YAPF_BINARY + ['--in-place', filepath])
      p.wait()
      with io.open(filepath, mode='r', newline='') as fd:
        reformatted_code = fd.read()
    self.assertEqual(reformatted_code, expected_formatted_code)

  def testInPlaceReformattingBlank(self):
    unformatted_code = u'\n\n'
    expected_formatted_code = u'\n'
    with utils.TempFileContents(
        self.test_tmpdir, unformatted_code, suffix='.py') as filepath:
      p = subprocess.Popen(YAPF_BINARY + ['--in-place', filepath])
      p.wait()
      with io.open(filepath, mode='r', encoding='utf-8', newline='') as fd:
        reformatted_code = fd.read()
    self.assertEqual(reformatted_code, expected_formatted_code)

  def testInPlaceReformattingEmpty(self):
    unformatted_code = u''
    expected_formatted_code = u''
    with utils.TempFileContents(
        self.test_tmpdir, unformatted_code, suffix='.py') as filepath:
      p = subprocess.Popen(YAPF_BINARY + ['--in-place', filepath])
      p.wait()
      with io.open(filepath, mode='r', encoding='utf-8', newline='') as fd:
        reformatted_code = fd.read()
    self.assertEqual(reformatted_code, expected_formatted_code)

  def testReadFromStdin(self):
    unformatted_code = textwrap.dedent("""\
        def foo():
          x = 37
        """)
    expected_formatted_code = textwrap.dedent("""\
        def foo():
            x = 37
        """)
    self.assertYapfReformats(unformatted_code, expected_formatted_code)

  def testReadFromStdinWithEscapedStrings(self):
    unformatted_code = textwrap.dedent("""\
        s =   "foo\\nbar"
        """)
    expected_formatted_code = textwrap.dedent("""\
        s = "foo\\nbar"
        """)
    self.assertYapfReformats(unformatted_code, expected_formatted_code)

  def testSetChromiumStyle(self):
    unformatted_code = textwrap.dedent("""\
        def foo(): # trail
            x = 37
        """)
    expected_formatted_code = textwrap.dedent("""\
        def foo():  # trail
          x = 37
        """)
    self.assertYapfReformats(
        unformatted_code,
        expected_formatted_code,
        extra_options=['--style=chromium'])

  def testSetCustomStyleBasedOnChromium(self):
    unformatted_code = textwrap.dedent("""\
        def foo(): # trail
            x = 37
        """)
    expected_formatted_code = textwrap.dedent("""\
        def foo():    # trail
          x = 37
        """)
    style_file = textwrap.dedent(u'''\
        [style]
        based_on_style = chromium
        SPACES_BEFORE_COMMENT = 4
        ''')
    with utils.TempFileContents(self.test_tmpdir, style_file) as stylepath:
      self.assertYapfReformats(
          unformatted_code,
          expected_formatted_code,
          extra_options=['--style={0}'.format(stylepath)])

  def testReadSingleLineCodeFromStdin(self):
    unformatted_code = textwrap.dedent("""\
        if True: pass
        """)
    expected_formatted_code = textwrap.dedent("""\
        if True: pass
        """)
    self.assertYapfReformats(unformatted_code, expected_formatted_code)

  def testEncodingVerification(self):
    unformatted_code = textwrap.dedent(u"""\
        '''The module docstring.'''
        # -*- coding: utf-8 -*-
        def f():
            x = 37
        """)

    with utils.NamedTempFile(
        suffix='.py', dirname=self.test_tmpdir) as (out, _):
      with utils.TempFileContents(
          self.test_tmpdir, unformatted_code, suffix='.py') as filepath:
        try:
          subprocess.check_call(YAPF_BINARY + ['--diff', filepath], stdout=out)
        except subprocess.CalledProcessError as e:
          self.assertEqual(e.returncode, 1)  # Indicates the text changed.

  def testReformattingSpecificLines(self):
    unformatted_code = textwrap.dedent("""\
        def h():
            if (xxxxxxxxxxxx.yyyyyyyy(zzzzzzzzzzzzz[0]) == 'aaaaaaaaaaa' and xxxxxxxxxxxx.yyyyyyyy(zzzzzzzzzzzzz[0].mmmmmmmm[0]) == 'bbbbbbb'):
                pass


        def g():
            if (xxxxxxxxxxxx.yyyyyyyy(zzzzzzzzzzzzz[0]) == 'aaaaaaaaaaa' and xxxxxxxxxxxx.yyyyyyyy(zzzzzzzzzzzzz[0].mmmmmmmm[0]) == 'bbbbbbb'):
                pass
        """)
    expected_formatted_code = textwrap.dedent("""\
        def h():
            if (xxxxxxxxxxxx.yyyyyyyy(zzzzzzzzzzzzz[0]) == 'aaaaaaaaaaa' and
                    xxxxxxxxxxxx.yyyyyyyy(zzzzzzzzzzzzz[0].mmmmmmmm[0]) == 'bbbbbbb'):
                pass


        def g():
            if (xxxxxxxxxxxx.yyyyyyyy(zzzzzzzzzzzzz[0]) == 'aaaaaaaaaaa' and xxxxxxxxxxxx.yyyyyyyy(zzzzzzzzzzzzz[0].mmmmmmmm[0]) == 'bbbbbbb'):
                pass
        """)
    # TODO(ambv): the `expected_formatted_code` here is not PEP8 compliant,
    # raising "E129 visually indented line with same indent as next logical
    # line" with flake8.
    self.assertYapfReformats(
        unformatted_code,
        expected_formatted_code,
        extra_options=['--lines', '1-2'])

  def testOmitFormattingLinesBeforeDisabledFunctionComment(self):
    unformatted_code = textwrap.dedent("""\
        import sys

        # Comment
        def some_func(x):
            x = ["badly" , "formatted","line" ]
        """)
    expected_formatted_code = textwrap.dedent("""\
        import sys

        # Comment
        def some_func(x):
            x = ["badly", "formatted", "line"]
        """)
    self.assertYapfReformats(
        unformatted_code,
        expected_formatted_code,
        extra_options=['--lines', '5-5'])

  def testReformattingSkippingLines(self):
    unformatted_code = textwrap.dedent("""\
        def h():
            if (xxxxxxxxxxxx.yyyyyyyy(zzzzzzzzzzzzz[0]) == 'aaaaaaaaaaa' and xxxxxxxxxxxx.yyyyyyyy(zzzzzzzzzzzzz[0].mmmmmmmm[0]) == 'bbbbbbb'):
                pass

        # yapf: disable
        def g():
            if (xxxxxxxxxxxx.yyyyyyyy(zzzzzzzzzzzzz[0]) == 'aaaaaaaaaaa' and xxxxxxxxxxxx.yyyyyyyy(zzzzzzzzzzzzz[0].mmmmmmmm[0]) == 'bbbbbbb'):
                pass
        # yapf: enable
        """)
    expected_formatted_code = textwrap.dedent("""\
        def h():
            if (xxxxxxxxxxxx.yyyyyyyy(zzzzzzzzzzzzz[0]) == 'aaaaaaaaaaa' and
                    xxxxxxxxxxxx.yyyyyyyy(zzzzzzzzzzzzz[0].mmmmmmmm[0]) == 'bbbbbbb'):
                pass


        # yapf: disable
        def g():
            if (xxxxxxxxxxxx.yyyyyyyy(zzzzzzzzzzzzz[0]) == 'aaaaaaaaaaa' and xxxxxxxxxxxx.yyyyyyyy(zzzzzzzzzzzzz[0].mmmmmmmm[0]) == 'bbbbbbb'):
                pass
        # yapf: enable
        """)
    self.assertYapfReformats(unformatted_code, expected_formatted_code)

  def testReformattingSkippingToEndOfFile(self):
    unformatted_code = textwrap.dedent("""\
        def h():
            if (xxxxxxxxxxxx.yyyyyyyy(zzzzzzzzzzzzz[0]) == 'aaaaaaaaaaa' and xxxxxxxxxxxx.yyyyyyyy(zzzzzzzzzzzzz[0].mmmmmmmm[0]) == 'bbbbbbb'):
                pass

        # yapf: disable
        def g():
            if (xxxxxxxxxxxx.yyyyyyyy(zzzzzzzzzzzzz[0]) == 'aaaaaaaaaaa' and xxxxxxxxxxxx.yyyyyyyy(zzzzzzzzzzzzz[0].mmmmmmmm[0]) == 'bbbbbbb'):
                pass

        def f():
            def e():
                while (xxxxxxxxxxxxxxxxxxxxx(yyyyyyyyyyyyy[zzzzz]) == 'aaaaaaaaaaa' and
                       xxxxxxxxxxxxxxxxxxxxx(yyyyyyyyyyyyy[zzzzz].aaaaaaaa[0]) ==
                       'bbbbbbb'):
                    pass
        """)
    expected_formatted_code = textwrap.dedent("""\
        def h():
            if (xxxxxxxxxxxx.yyyyyyyy(zzzzzzzzzzzzz[0]) == 'aaaaaaaaaaa' and
                    xxxxxxxxxxxx.yyyyyyyy(zzzzzzzzzzzzz[0].mmmmmmmm[0]) == 'bbbbbbb'):
                pass


        # yapf: disable
        def g():
            if (xxxxxxxxxxxx.yyyyyyyy(zzzzzzzzzzzzz[0]) == 'aaaaaaaaaaa' and xxxxxxxxxxxx.yyyyyyyy(zzzzzzzzzzzzz[0].mmmmmmmm[0]) == 'bbbbbbb'):
                pass

        def f():
            def e():
                while (xxxxxxxxxxxxxxxxxxxxx(yyyyyyyyyyyyy[zzzzz]) == 'aaaaaaaaaaa' and
                       xxxxxxxxxxxxxxxxxxxxx(yyyyyyyyyyyyy[zzzzz].aaaaaaaa[0]) ==
                       'bbbbbbb'):
                    pass
        """)
    self.assertYapfReformats(unformatted_code, expected_formatted_code)

  def testReformattingSkippingSingleLine(self):
    unformatted_code = textwrap.dedent("""\
        def h():
            if (xxxxxxxxxxxx.yyyyyyyy(zzzzzzzzzzzzz[0]) == 'aaaaaaaaaaa' and xxxxxxxxxxxx.yyyyyyyy(zzzzzzzzzzzzz[0].mmmmmmmm[0]) == 'bbbbbbb'):
                pass

        def g():
            if (xxxxxxxxxxxx.yyyyyyyy(zzzzzzzzzzzzz[0]) == 'aaaaaaaaaaa' and xxxxxxxxxxxx.yyyyyyyy(zzzzzzzzzzzzz[0].mmmmmmmm[0]) == 'bbbbbbb'):  # yapf: disable
                pass
        """)
    expected_formatted_code = textwrap.dedent("""\
        def h():
            if (xxxxxxxxxxxx.yyyyyyyy(zzzzzzzzzzzzz[0]) == 'aaaaaaaaaaa' and
                    xxxxxxxxxxxx.yyyyyyyy(zzzzzzzzzzzzz[0].mmmmmmmm[0]) == 'bbbbbbb'):
                pass


        def g():
            if (xxxxxxxxxxxx.yyyyyyyy(zzzzzzzzzzzzz[0]) == 'aaaaaaaaaaa' and xxxxxxxxxxxx.yyyyyyyy(zzzzzzzzzzzzz[0].mmmmmmmm[0]) == 'bbbbbbb'):  # yapf: disable
                pass
        """)
    self.assertYapfReformats(unformatted_code, expected_formatted_code)

  def testDisableWholeDataStructure(self):
    unformatted_code = textwrap.dedent("""\
        A = set([
            'hello',
            'world',
        ])  # yapf: disable
        """)
    expected_formatted_code = textwrap.dedent("""\
        A = set([
            'hello',
            'world',
        ])  # yapf: disable
        """)
    self.assertYapfReformats(unformatted_code, expected_formatted_code)

  def testDisableButAdjustIndentations(self):
    unformatted_code = textwrap.dedent("""\
        class SplitPenaltyTest(unittest.TestCase):
          def testUnbreakable(self):
            self._CheckPenalties(tree, [
            ])  # yapf: disable
        """)
    expected_formatted_code = textwrap.dedent("""\
        class SplitPenaltyTest(unittest.TestCase):
            def testUnbreakable(self):
                self._CheckPenalties(tree, [
                ])  # yapf: disable
        """)
    self.assertYapfReformats(unformatted_code, expected_formatted_code)

  def testRetainingHorizontalWhitespace(self):
    unformatted_code = textwrap.dedent("""\
        def h():
            if (xxxxxxxxxxxx.yyyyyyyy(zzzzzzzzzzzzz[0]) == 'aaaaaaaaaaa' and xxxxxxxxxxxx.yyyyyyyy(zzzzzzzzzzzzz[0].mmmmmmmm[0]) == 'bbbbbbb'):
                pass

        def g():
            if (xxxxxxxxxxxx.yyyyyyyy        (zzzzzzzzzzzzz  [0]) ==     'aaaaaaaaaaa' and    xxxxxxxxxxxx.yyyyyyyy(zzzzzzzzzzzzz[0].mmmmmmmm[0]) == 'bbbbbbb'):  # yapf: disable
                pass
        """)
    expected_formatted_code = textwrap.dedent("""\
        def h():
            if (xxxxxxxxxxxx.yyyyyyyy(zzzzzzzzzzzzz[0]) == 'aaaaaaaaaaa' and
                    xxxxxxxxxxxx.yyyyyyyy(zzzzzzzzzzzzz[0].mmmmmmmm[0]) == 'bbbbbbb'):
                pass


        def g():
            if (xxxxxxxxxxxx.yyyyyyyy        (zzzzzzzzzzzzz  [0]) ==     'aaaaaaaaaaa' and    xxxxxxxxxxxx.yyyyyyyy(zzzzzzzzzzzzz[0].mmmmmmmm[0]) == 'bbbbbbb'):  # yapf: disable
                pass
        """)
    self.assertYapfReformats(unformatted_code, expected_formatted_code)

  def testRetainingVerticalWhitespace(self):
    unformatted_code = textwrap.dedent("""\
        def h():
            if (xxxxxxxxxxxx.yyyyyyyy(zzzzzzzzzzzzz[0]) == 'aaaaaaaaaaa' and xxxxxxxxxxxx.yyyyyyyy(zzzzzzzzzzzzz[0].mmmmmmmm[0]) == 'bbbbbbb'):
                pass

        def g():


            if (xxxxxxxxxxxx.yyyyyyyy(zzzzzzzzzzzzz[0]) == 'aaaaaaaaaaa' and xxxxxxxxxxxx.yyyyyyyy(zzzzzzzzzzzzz[0].mmmmmmmm[0]) == 'bbbbbbb'):

                pass
        """)
    expected_formatted_code = textwrap.dedent("""\
        def h():
            if (xxxxxxxxxxxx.yyyyyyyy(zzzzzzzzzzzzz[0]) == 'aaaaaaaaaaa' and
                    xxxxxxxxxxxx.yyyyyyyy(zzzzzzzzzzzzz[0].mmmmmmmm[0]) == 'bbbbbbb'):
                pass

        def g():


            if (xxxxxxxxxxxx.yyyyyyyy(zzzzzzzzzzzzz[0]) == 'aaaaaaaaaaa' and xxxxxxxxxxxx.yyyyyyyy(zzzzzzzzzzzzz[0].mmmmmmmm[0]) == 'bbbbbbb'):

                pass
        """)
    self.assertYapfReformats(
        unformatted_code,
        expected_formatted_code,
        extra_options=['--lines', '1-2'])

    unformatted_code = textwrap.dedent("""\


        if a:     b


        if c:
            to_much      + indent

            same



        #comment

        #   trailing whitespace
        """)
    expected_formatted_code = textwrap.dedent("""\
        if a: b


        if c:
            to_much      + indent

            same



        #comment

        #   trailing whitespace
        """)
    self.assertYapfReformats(
        unformatted_code,
        expected_formatted_code,
        extra_options=['--lines', '3-3', '--lines', '13-13'])

    unformatted_code = textwrap.dedent("""\
        '''
        docstring

        '''

        import blah
        """)

    self.assertYapfReformats(
        unformatted_code, unformatted_code, extra_options=['--lines', '2-2'])

  def testRetainingSemicolonsWhenSpecifyingLines(self):
    unformatted_code = textwrap.dedent("""\
        a = line_to_format
        def f():
            x = y + 42; z = n * 42
            if True: a += 1 ; b += 1 ; c += 1
        """)
    expected_formatted_code = textwrap.dedent("""\
        a = line_to_format


        def f():
            x = y + 42; z = n * 42
            if True: a += 1 ; b += 1 ; c += 1
        """)
    self.assertYapfReformats(
        unformatted_code,
        expected_formatted_code,
        extra_options=['--lines', '1-1'])

  def testDisabledMultilineStrings(self):
    unformatted_code = textwrap.dedent('''\
        foo=42
        def f():
            email_text += """<html>This is a really long docstring that goes over the column limit and is multi-line.<br><br>
        <b>Czar: </b>"""+despot["Nicholas"]+"""<br>
        <b>Minion: </b>"""+serf["Dmitri"]+"""<br>
        <b>Residence: </b>"""+palace["Winter"]+"""<br>
        </body>
        </html>"""
        ''')
    expected_formatted_code = textwrap.dedent('''\
        foo = 42


        def f():
            email_text += """<html>This is a really long docstring that goes over the column limit and is multi-line.<br><br>
        <b>Czar: </b>"""+despot["Nicholas"]+"""<br>
        <b>Minion: </b>"""+serf["Dmitri"]+"""<br>
        <b>Residence: </b>"""+palace["Winter"]+"""<br>
        </body>
        </html>"""
        ''')
    self.assertYapfReformats(
        unformatted_code,
        expected_formatted_code,
        extra_options=['--lines', '1-1'])

  def testDisableWhenSpecifyingLines(self):
    unformatted_code = textwrap.dedent("""\
        # yapf: disable
        A = set([
            'hello',
            'world',
        ])
        # yapf: enable
        B = set([
            'hello',
            'world',
        ])  # yapf: disable
        """)
    expected_formatted_code = textwrap.dedent("""\
        # yapf: disable
        A = set([
            'hello',
            'world',
        ])
        # yapf: enable
        B = set([
            'hello',
            'world',
        ])  # yapf: disable
        """)
    self.assertYapfReformats(
        unformatted_code,
        expected_formatted_code,
        extra_options=['--lines', '1-10'])

  def testDisableFormattingInDataLiteral(self):
    unformatted_code = textwrap.dedent("""\
        def horrible():
          oh_god()
          why_would_you()
          [
             'do',

              'that',
          ]

        def still_horrible():
            oh_god()
            why_would_you()
            [
                'do',

                'that'
            ]
        """)
    expected_formatted_code = textwrap.dedent("""\
        def horrible():
            oh_god()
            why_would_you()
            [
               'do',

                'that',
            ]

        def still_horrible():
            oh_god()
            why_would_you()
            ['do', 'that']
        """)
    self.assertYapfReformats(
        unformatted_code,
        expected_formatted_code,
        extra_options=['--lines', '14-15'])

  def testRetainVerticalFormattingBetweenDisabledAndEnabledLines(self):
    unformatted_code = textwrap.dedent("""\
        class A(object):
            def aaaaaaaaaaaaa(self):
                c = bbbbbbbbb.ccccccccc('challenge', 0, 1, 10)
                self.assertEqual(
                    ('ddddddddddddddddddddddddd',
             'eeeeeeeeeeeeeeeeeeeeeeeee.%s' %
                     c.ffffffffffff),
             gggggggggggg.hhhhhhhhh(c, c.ffffffffffff))
                iiiii = jjjjjjjjjjjjjj.iiiii
        """)
    expected_formatted_code = textwrap.dedent("""\
        class A(object):
            def aaaaaaaaaaaaa(self):
                c = bbbbbbbbb.ccccccccc('challenge', 0, 1, 10)
                self.assertEqual(('ddddddddddddddddddddddddd',
                                  'eeeeeeeeeeeeeeeeeeeeeeeee.%s' % c.ffffffffffff),
                                 gggggggggggg.hhhhhhhhh(c, c.ffffffffffff))
                iiiii = jjjjjjjjjjjjjj.iiiii
        """)
    self.assertYapfReformats(
        unformatted_code,
        expected_formatted_code,
        extra_options=['--lines', '4-7'])

  def testFormatLinesSpecifiedInMiddleOfExpression(self):
    unformatted_code = textwrap.dedent("""\
        class A(object):
            def aaaaaaaaaaaaa(self):
                c = bbbbbbbbb.ccccccccc('challenge', 0, 1, 10)
                self.assertEqual(
                    ('ddddddddddddddddddddddddd',
             'eeeeeeeeeeeeeeeeeeeeeeeee.%s' %
                     c.ffffffffffff),
             gggggggggggg.hhhhhhhhh(c, c.ffffffffffff))
                iiiii = jjjjjjjjjjjjjj.iiiii
        """)
    expected_formatted_code = textwrap.dedent("""\
        class A(object):
            def aaaaaaaaaaaaa(self):
                c = bbbbbbbbb.ccccccccc('challenge', 0, 1, 10)
                self.assertEqual(('ddddddddddddddddddddddddd',
                                  'eeeeeeeeeeeeeeeeeeeeeeeee.%s' % c.ffffffffffff),
                                 gggggggggggg.hhhhhhhhh(c, c.ffffffffffff))
                iiiii = jjjjjjjjjjjjjj.iiiii
        """)
    self.assertYapfReformats(
        unformatted_code,
        expected_formatted_code,
        extra_options=['--lines', '5-6'])

  def testCommentFollowingMultilineString(self):
    unformatted_code = textwrap.dedent("""\
        def foo():
            '''First line.
            Second line.
            '''  # comment
            x = '''hello world'''  # second comment
            return 42  # another comment
        """)
    expected_formatted_code = textwrap.dedent("""\
        def foo():
            '''First line.
            Second line.
            '''  # comment
            x = '''hello world'''  # second comment
            return 42  # another comment
        """)
    self.assertYapfReformats(
        unformatted_code,
        expected_formatted_code,
        extra_options=['--lines', '1-1'])

  def testDedentClosingBracket(self):
    # no line-break on the first argument, not dedenting closing brackets
    unformatted_code = textwrap.dedent("""\
      def overly_long_function_name(first_argument_on_the_same_line,
      second_argument_makes_the_line_too_long):
        pass
    """)
    expected_formatted_code = textwrap.dedent("""\
      def overly_long_function_name(first_argument_on_the_same_line,
                                    second_argument_makes_the_line_too_long):
          pass
    """)
    self.assertYapfReformats(
        unformatted_code,
        expected_formatted_code,
        extra_options=['--style=pep8'])

    # TODO(ambv): currently the following produces the closing bracket on a new
    # line but indented to the opening bracket which is the worst of both
    # worlds. Expected behaviour would be to format as --style=pep8 does in
    # this case.
    # self.assertYapfReformats(unformatted_code, expected_formatted_code,
    #                          extra_options=['--style=facebook'])

    # line-break before the first argument, dedenting closing brackets if set
    unformatted_code = textwrap.dedent("""\
      def overly_long_function_name(
        first_argument_on_the_same_line,
        second_argument_makes_the_line_too_long):
        pass
    """)
    # expected_formatted_pep8_code = textwrap.dedent("""\
    #   def overly_long_function_name(
    #           first_argument_on_the_same_line,
    #           second_argument_makes_the_line_too_long):
    #       pass
    # """)
    expected_formatted_fb_code = textwrap.dedent("""\
      def overly_long_function_name(
          first_argument_on_the_same_line, second_argument_makes_the_line_too_long
      ):
          pass
    """)
    self.assertYapfReformats(
        unformatted_code,
        expected_formatted_fb_code,
        extra_options=['--style=facebook'])
    # TODO(ambv): currently the following produces code that is not PEP8
    # compliant, raising "E125 continuation line with same indent as next
    # logical line" with flake8. Expected behaviour for PEP8 would be to use
    # double-indentation here.
    # self.assertYapfReformats(unformatted_code, expected_formatted_pep8_code,
    #                          extra_options=['--style=pep8'])

  def testCoalesceBrackets(self):
    unformatted_code = textwrap.dedent("""\
       some_long_function_name_foo(
           {
               'first_argument_of_the_thing': id,
               'second_argument_of_the_thing': "some thing"
           }
       )""")
    expected_formatted_code = textwrap.dedent("""\
       some_long_function_name_foo({
           'first_argument_of_the_thing': id,
           'second_argument_of_the_thing': "some thing"
       })
       """)
    with utils.NamedTempFile(dirname=self.test_tmpdir, mode='w') as (f, name):
      f.write(
          textwrap.dedent(u'''\
          [style]
          column_limit=82
          coalesce_brackets = True
          '''))
      f.flush()
      self.assertYapfReformats(
          unformatted_code,
          expected_formatted_code,
          extra_options=['--style={0}'.format(name)])

  def testPseudoParenSpaces(self):
    unformatted_code = textwrap.dedent("""\
        def foo():
          def bar():
            return {msg_id: author for author, msg_id in reader}
        """)
    expected_formatted_code = textwrap.dedent("""\
        def foo():

          def bar():
            return {msg_id: author for author, msg_id in reader}
        """)
    self.assertYapfReformats(
        unformatted_code,
        expected_formatted_code,
        extra_options=['--lines', '1-1', '--style', 'chromium'])

  def testMultilineCommentFormattingDisabled(self):
    unformatted_code = textwrap.dedent("""\
        # This is a comment
        FOO = {
            aaaaaaaa.ZZZ: [
                bbbbbbbbbb.Pop(),
                # Multiline comment.
                # Line two.
                bbbbbbbbbb.Pop(),
            ],
            'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx':
                ('yyyyy', zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz),
            '#': lambda x: x  # do nothing
        }
        """)
    expected_formatted_code = textwrap.dedent("""\
        # This is a comment
        FOO = {
            aaaaaaaa.ZZZ: [
                bbbbbbbbbb.Pop(),
                # Multiline comment.
                # Line two.
                bbbbbbbbbb.Pop(),
            ],
            'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx':
                ('yyyyy', zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz),
            '#': lambda x: x  # do nothing
        }
        """)
    self.assertYapfReformats(
        unformatted_code,
        expected_formatted_code,
        extra_options=['--lines', '1-1', '--style', 'chromium'])

  def testTrailingCommentsWithDisabledFormatting(self):
    unformatted_code = textwrap.dedent("""\
        import os

        SCOPES = [
            'hello world'  # This is a comment.
        ]
        """)
    expected_formatted_code = textwrap.dedent("""\
        import os

        SCOPES = [
            'hello world'  # This is a comment.
        ]
        """)
    self.assertYapfReformats(
        unformatted_code,
        expected_formatted_code,
        extra_options=['--lines', '1-1', '--style', 'chromium'])

  def testUseTabs(self):
    unformatted_code = """\
def foo_function():
 if True:
  pass
"""
    expected_formatted_code = """\
def foo_function():
	if True:
		pass
"""
    style_contents = u"""\
[style]
based_on_style = chromium
USE_TABS = true
INDENT_WIDTH=1
"""
    with utils.TempFileContents(self.test_tmpdir, style_contents) as stylepath:
      self.assertYapfReformats(
          unformatted_code,
          expected_formatted_code,
          extra_options=['--style={0}'.format(stylepath)])

  def testUseTabsWith(self):
    unformatted_code = """\
def f():
  return ['hello', 'world',]
"""
    expected_formatted_code = """\
def f():
	return [
	    'hello',
	    'world',
	]
"""
    style_contents = u"""\
[style]
based_on_style = chromium
USE_TABS = true
INDENT_WIDTH=1
"""
    with utils.TempFileContents(self.test_tmpdir, style_contents) as stylepath:
      self.assertYapfReformats(
          unformatted_code,
          expected_formatted_code,
          extra_options=['--style={0}'.format(stylepath)])

  def testStyleOutputRoundTrip(self):
    unformatted_code = textwrap.dedent("""\
        def foo_function():
          pass
        """)
    expected_formatted_code = textwrap.dedent("""\
        def foo_function():
            pass
        """)

    with utils.NamedTempFile(dirname=self.test_tmpdir) as (stylefile,
                                                           stylepath):
      p = subprocess.Popen(
          YAPF_BINARY + ['--style-help'],
          stdout=stylefile,
          stdin=subprocess.PIPE,
          stderr=subprocess.PIPE)
      _, stderrdata = p.communicate()
      self.assertEqual(stderrdata, b'')
      self.assertYapfReformats(
          unformatted_code,
          expected_formatted_code,
          extra_options=['--style={0}'.format(stylepath)])

  def testSpacingBeforeComments(self):
    unformatted_code = textwrap.dedent("""\
        A = 42


        # A comment
        def x():
            pass
        def _():
            pass
        """)
    expected_formatted_code = textwrap.dedent("""\
        A = 42


        # A comment
        def x():
            pass
        def _():
            pass
        """)
    self.assertYapfReformats(
        unformatted_code,
        expected_formatted_code,
        extra_options=['--lines', '1-2'])

  def testSpacingBeforeCommentsInDicts(self):
    unformatted_code = textwrap.dedent("""\
        A=42

        X = {
            # 'Valid' statuses.
            PASSED:  # Passed
                'PASSED',
            FAILED:  # Failed
                'FAILED',
            TIMED_OUT:  # Timed out.
                'FAILED',
            BORKED:  # Broken.
                'BROKEN'
        }
        """)
    expected_formatted_code = textwrap.dedent("""\
        A = 42

        X = {
            # 'Valid' statuses.
            PASSED:  # Passed
                'PASSED',
            FAILED:  # Failed
                'FAILED',
            TIMED_OUT:  # Timed out.
                'FAILED',
            BORKED:  # Broken.
                'BROKEN'
        }
        """)
    self.assertYapfReformats(
        unformatted_code,
        expected_formatted_code,
        extra_options=['--style', 'chromium', '--lines', '1-1'])

  @unittest.skipUnless(py3compat.PY36, 'Requires Python 3.6')
  def testCP936Encoding(self):
    unformatted_code = 'print("中文")\n'
    expected_formatted_code = 'print("中文")\n'
    self.assertYapfReformats(
        unformatted_code,
        expected_formatted_code,
        env={'PYTHONIOENCODING': 'cp936'})


class BadInputTest(unittest.TestCase):
  """Test yapf's behaviour when passed bad input."""

  def testBadSyntax(self):
    code = '  a = 1\n'
    self.assertRaises(SyntaxError, yapf_api.FormatCode, code)


class DiffIndentTest(unittest.TestCase):

  @staticmethod
  def _OwnStyle():
    my_style = style.CreatePEP8Style()
    my_style['INDENT_WIDTH'] = 3
    my_style['CONTINUATION_INDENT_WIDTH'] = 3
    return my_style

  def _Check(self, unformatted_code, expected_formatted_code):
    formatted_code, _ = yapf_api.FormatCode(
        unformatted_code, style_config=style.SetGlobalStyle(self._OwnStyle()))
    self.assertEqual(expected_formatted_code, formatted_code)

  def testSimple(self):
    unformatted_code = textwrap.dedent("""\
        for i in range(5):
         print('bar')
         """)
    expected_formatted_code = textwrap.dedent("""\
        for i in range(5):
           print('bar')
           """)
    self._Check(unformatted_code, expected_formatted_code)


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

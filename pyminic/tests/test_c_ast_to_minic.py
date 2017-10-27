from __future__ import print_function
import unittest
from pycparser import parse_file
import minic.c_ast_to_minic as ctoc
import minic.minic_ast as mast


class TestConversion1(unittest.TestCase):
    def test_parse_and_convert(self):
        fullc_ast = parse_file('./c_files/minic.c')
        converted = ctoc.transform(fullc_ast)
        self.failUnless(isinstance(converted, mast.FileAST))
        self.assertEqual(len(converted.ext), 2)
        self.failUnless(isinstance(converted.ext[0], mast.FuncDef))

        funcdef_mss = converted.ext[0]
        self.assertEqual(funcdef_mss.decl.name, 'mss')
        mss_body = funcdef_mss.body
        self.assertTrue(isinstance(mss_body, mast.Block))
        self.assertEqual(len(mss_body.block_items), 5)
        self.failUnless(isinstance(mss_body.block_items[0], mast.Decl))
        self.failUnless(isinstance(mss_body.block_items[1], mast.Decl))
        self.failUnless(isinstance(mss_body.block_items[2], mast.Decl))
        self.failUnless(isinstance(mss_body.block_items[3], mast.For))
        forstmt = mss_body.block_items[3]
        print(forstmt.next)
        self.assertTrue(isinstance(forstmt.next, mast.Assignment))
        self.failUnless(isinstance(mss_body.block_items[4], mast.Return))

        funcdef_main =converted.ext[1]
        self.assertEqual(funcdef_main.decl.name, 'main')
        main_body = funcdef_main.body
        self.assertEqual(len(main_body.block_items), 4)
        self.failUnless(isinstance(main_body.block_items[0], mast.Decl))
        self.failUnless(isinstance(main_body.block_items[1], mast.Decl))
        self.failUnless(isinstance(main_body.block_items[2], mast.Assignment))
        self.failUnless(isinstance(main_body.block_items[3], mast.Return))

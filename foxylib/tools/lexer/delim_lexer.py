#!/usr/bin/env python

# import sys,os
# from _functools import reduce
# CORE_DIR = reduce(lambda x,f:f(x), [os.path.dirname,]*4, os.path.realpath(__file__))
# sys.path.extend( [os.path.join(CORE_DIR,x) for x in ["web","lib"]] )
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
# import django
# django.setup()

import re

from future.utils import lfilter, lmap
from ply import lex
# from ply.lex import TOKEN
from itertools import chain
from foxylib.tools.lexer.lexer_tools import (LexerTool, MultipleColonInCommandError as MCICErr)

from foxylib.tools.collections.collections_tool import lchain
from foxylib.tools.string.string_tool import str2strip


class DelimLexer(object):
    tokens = (
       'DQ',
       'SQ',
       'BACKSLASH',
       'DELIM',
       'ANY',
    )

    t_SQ = r"'"
    t_DQ = r'"'
    t_BACKSLASH = r'\\'
    
    @classmethod
    def chariter2r_ANY(cls, l,): return r"[{0}]".format("".join(map(re.escape,l)))
    @classmethod
    def chariter2r_NONE(cls, l,): return r"[^{0}]+".format("".join(map(re.escape,l)))
    @classmethod
    def specialchars(cls): return "".join(["'",'"',"\\",])
    
    def t_DELIM(self,t): return t
    def t_ANY(self,t): return t
    #def t_DELIM_EATER(self, t): return t
        
    # Error handling rule
    def t_error(self,t):
        raise Exception("Illegal character '%s'" % t.value[0])

    # Build the lexer
    def build(self,**kwargs):
        self.lexer = lex.lex(module=self, **kwargs)
    
    @classmethod
    def r_TUPLE2lexer(cls, r_TUPLE):
        m = cls()
        (cls.t_DELIM.regex, cls.t_ANY.regex,) = r_TUPLE
        #if cls.t_DELIM_EATER.regex is None: cls.t_DELIM_EATER.regex = cls.t_ANY.regex 
        m.build()
        lexer = m.lexer
        return lexer
    
    @classmethod
    def lexer_args(cls):
        s_delim_eaters = ","
        s_ANY_EXs = lchain(s_delim_eaters,DelimLexer.specialchars())
        r_TUPLE = (r"\s+",
                   r"(?:(?:[^\s{0}])|(?:{1}))".format("".join(map(re.escape,s_ANY_EXs)),
                                                      r"\s*(?:{0})\s*".format("|".join(map(re.escape, s_delim_eaters))),
                                                      ),
                   )
        lexer = cls.r_TUPLE2lexer(r_TUPLE)
        return lexer
    
    @classmethod
    def str_DELIMs2lexer(cls, str_DELIMs):
        r_TUPLE = (DelimLexer.chariter2r_ANY(str_DELIMs),
                   DelimLexer.chariter2r_NONE(chain(DelimLexer.specialchars(),str_DELIMs)),
                   )
        
        lexer = cls.r_TUPLE2lexer(r_TUPLE)
        return lexer
    
    @classmethod
    def str2s_INSTR_list(cls, s_IN, delim_HEAD=None, delim_INSTR=None):
        if delim_HEAD is None: delim_HEAD=":"
        if delim_INSTR is None: delim_INSTR=";"
        
        s_COLON_list = DelimLexer.lexer2str_DELIM_list(cls.str_DELIMs2lexer(delim_HEAD), LexerTool.DELIM_EXCLUDED, s_IN)
        MCICErr.chk_n_raise(s_COLON_list, s_IN)
        if not s_COLON_list: return s_COLON_list
        
        s_SEMI_list_RAW = DelimLexer.lexer2str_DELIM_list(cls.str_DELIMs2lexer(delim_INSTR), LexerTool.DELIM_EXCLUDED, s_COLON_list[-1],)
        s_SEMI_list = lfilter(bool,map(lambda x:x.strip(),s_SEMI_list_RAW))
        
        if len(s_COLON_list)==1: return s_SEMI_list
        
        l = [" ".join([s_COLON_list[0],s_SEMI])
             for s_SEMI in s_SEMI_list]
        return l
    
    @classmethod
    def str2s_COMMA_list(cls, s_IN):
        l = DelimLexer.lexer2str_DELIM_list(cls.str_DELIMs2lexer(","), LexerTool.DELIM_EXCLUDED, s_IN)
        s_COMMA_list = lmap(str2strip,l)
        return s_COMMA_list
        
    @classmethod
    def lexer2str_DELIM_list(cls, lexer, delim_rule, s_IN, maxsplit=None,):
        lexer.input(s_IN)
        
        tt_list_ESCAPE = ["BACKSLASH"]
        #tt_list_STATE = ["SQ","DQ"]
        tt_list_STATE = ["DQ",]
        tt_list_DELIM = ["DELIM"]
         
        str_DELIM_list = []
        token_list_DELIM = []
        state_INITIAL = "INITIAL"
        l_state = [state_INITIAL,]
        
        while True:
            tok = lexer.token()
            if not tok:  break

            state_CUR = l_state[-1]
            
            stop_split = (maxsplit is not None) and (len(str_DELIM_list) >= maxsplit)
            
            stt = LexerTool.tok2semantic_token_type(tok,
                                              token_list_DELIM,
                                              [tt_list_ESCAPE,tt_list_STATE,tt_list_DELIM],
                                              stop_split,
                                              state_CUR,
                                              state_INITIAL,
                                              )
            
            
            is_append_BEFORE = all([tok.type not in tt_list_STATE,
                                    any([stt not in [LexerTool.STT_DELIM],
                                         delim_rule in [LexerTool.DELIM_AS_SUFFIX,],
                                         ]),
                                    ])
            is_append_BEFORE_and_done = (stt in [LexerTool.STT_ANY])
            
            
            if is_append_BEFORE: token_list_DELIM.append(tok)
            if is_append_BEFORE_and_done: continue
            
            if stt == LexerTool.STT_DELIM:
                create_str_DELIM = True #any([token_list_DELIM,(not str_DELIM_list),])
                if create_str_DELIM:
                    str_DELIM_list.append( LexerTool.token_list_DELIM2str_DELIM(token_list_DELIM) )
                    token_list_DELIM = []
                
                if delim_rule in [LexerTool.DELIM_AS_PREFIX,]:
                    token_list_DELIM.append(tok)
                continue
            
            if stt == LexerTool.STT_START:
                l_state.append(tok.type)
                continue
            
            if stt == LexerTool.STT_END:
                if l_state[-1] != tok.type: raise Exception()
                l_state.pop()
                continue
        
        
        if len(l_state)>1: return None
        if l_state[0] != state_INITIAL: return None
        
        
        if token_list_DELIM:
            str_DELIM_list.append( LexerTool.token_list_DELIM2str_DELIM(token_list_DELIM) )
        
        return str_DELIM_list
    
def main():
    
    s_IN = '"a1{0} a2"{0} b1 b2{0} "c1 c2" c3{0} d1'.format(";")
    l = DelimLexer.lexer2str_DELIM_list(DelimLexer.str_DELIMs2lexer(";"),
                                        LexerTool.DELIM_AS_SUFFIX,
                                        s_IN,
                                        )
    #l = m.str2str_token_list(s)
    
    print(l)

if __name__ == "__main__":
    main()


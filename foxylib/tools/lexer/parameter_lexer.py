import re

from future.utils import lmap, lfilter
from ply import lex

from foxylib.tools.collections.collections_tool import lchain
from foxylib.tools.lexer.lexer_tools import LexerTool
from foxylib.tools.string.string_tool import str2strip


class ParameterLexer:
    # List of token names.   This is always required
    tokens = (
       'ANY',
       #'WHITESPACE',
       'DQ',
       'SQ',
       'BACKSLASH',
       'EQUAL',
       'DELIM_PREFIX',
    )

    l_PREFIX = ["+","-","*","?"]
    t_DQ = r'"'
    t_SQ = r"'"
    t_BACKSLASH = r'\\'
    t_EQUAL    = r'='
    t_DELIM_PREFIX    = r'[{0}]'.format("".join(lmap(re.escape,l_PREFIX)))
    
    l_VAR = lchain(l_PREFIX,["\\","=","'",'"',],)
    t_ANY = r'(?:[^\s{0}]+)|(?:\s+)'.format("".join(lmap(re.escape,l_VAR)))
    #t_WHITESPACE = r'\W+'
    
    # Error handling rule
    def t_error(self,t): raise Exception("Illegal character '%s'" % t.value[0])

    # Build the lexer
    def build(self,**kwargs):
        self.lexer = lex.lex(module=self, **kwargs)
    
    
    DELIM_TYPE_PREFIX = "P"
    DELIM_TYPE_INFIX = "I"
    
    
    @classmethod
    def r_prefix(cls): return r"(?:{0})".format("|".join(lmap(re.escape,cls.l_PREFIX)))
    @classmethod
    def stt_delim2type(cls, tok):
        is_PREFIX = (tok.value in cls.l_PREFIX)
        is_INFIX = (tok.value in ["="])
        if len(lfilter(bool,[is_PREFIX,is_INFIX]))!=1: raise Exception()
        
        if is_PREFIX: return cls.DELIM_TYPE_PREFIX
        if is_INFIX: return cls.DELIM_TYPE_INFIX
        raise Exception() 
            
    @classmethod
    def delim_infix2iStart(cls, token_list_DELIM,tt_list_DELIM,):
        if not token_list_DELIM: return None
        tok_LAST = token_list_DELIM[-1]
        
        if tok_LAST.type != "ANY": return None
        
        if len(token_list_DELIM)<=1: return -1
        
        tok_2PREV = token_list_DELIM[-2]
        if tok_2PREV.type not in tt_list_DELIM: return -1
        
        delim_type = cls.stt_delim2type(tok_2PREV)
        
        if delim_type == cls.DELIM_TYPE_INFIX: return None # Wrong syntax
        if delim_type == cls.DELIM_TYPE_PREFIX: return -2
        raise Exception()
    
    @classmethod
    def is_delim_infix_valid(cls, token_list_DELIM):
        if not token_list_DELIM: return False
        tok_LAST = token_list_DELIM[-1]
        
        if tok_LAST.type != "ANY": return False
        return True
        
    @classmethod
    def lexer2str_DELIM_list(cls, lexer, s_IN, maxsplit=None,):
        # delim_rule = LexerTool.DELIM_AS_PREFIX
        
        lexer.input(s_IN)
        
        tt_list_ESCAPE = ["BACKSLASH"]
        tt_list_STATE = ["SQ","DQ"]
        tt_list_DELIM = ["DELIM_PREFIX","EQUAL",]
        
        str_DELIM_list = []
        token_list_DELIM = []
        state_INITIAL = "INITIAL"
        l_state = [state_INITIAL,]
        
        while True:
            tok = lexer.token()
            if not tok:  break

            #print(tok, tok.type, file=sys.stderr)
            state_CUR = l_state[-1]
            
            stop_split = (maxsplit is not None) and (len(str_DELIM_list) >= maxsplit)
            
            stt = LexerTool.tok2semantic_token_type(tok,
                                              token_list_DELIM,
                                              [tt_list_ESCAPE,tt_list_STATE,tt_list_DELIM,],
                                              stop_split,
                                              state_CUR,
                                              state_INITIAL,
                                              )
            
            
            is_append_BEFORE = stt not in [LexerTool.STT_DELIM]
            is_append_BEFORE_and_done = (stt in [LexerTool.STT_ANY])
            
            if is_append_BEFORE: token_list_DELIM.append(tok)
            if is_append_BEFORE_and_done: continue
            
            if stt == LexerTool.STT_DELIM:
                delim_type = cls.stt_delim2type(tok)
                
                
                if delim_type == cls.DELIM_TYPE_INFIX:
                    iSTART_INFIX = cls.delim_infix2iStart(token_list_DELIM, tt_list_DELIM,)
                    if iSTART_INFIX is None:
                        #raise Exception()
                        return None # Syntactically wrong
                    
                    if iSTART_INFIX<-1:
                        if len(token_list_DELIM)!=2: raise Exception()
                    else:
                        token_list_PREV = token_list_DELIM[:iSTART_INFIX]
                        str_DELIM_list.append( LexerTool.token_list_DELIM2str_DELIM(token_list_PREV) )
                        token_list_DELIM = token_list_DELIM[iSTART_INFIX:]
                        
                    #print(tok, token_list_DELIM, str_DELIM_list, iSTART_INFIX, file=sys.stderr)
                
                elif delim_type == cls.DELIM_TYPE_PREFIX:
                    token_list_PREV = token_list_DELIM
                    str_DELIM_list.append( LexerTool.token_list_DELIM2str_DELIM(token_list_PREV) )
                    token_list_DELIM = []
                else: raise Exception()
                
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
    
    
    
    
    @classmethod
    def str2l_token(cls, s, maxsplit=None, include_tokens=None,):
        if include_tokens is None: include_tokens = True
        
        m = cls()
        m.build()
        
        tok_groups = (["ANY","SINGLEQUOTE","DOUBLEQUOTE"],
                      ["DELIM"],
                      )
        l = LexerTool.str2str_token_list(m.lexer, s, tok_groups, maxsplit=maxsplit, include_tokens=include_tokens,)
        return l
    
    @classmethod
    def create_lexer(cls):
        m = cls()
        m.build()
        lexer = m.lexer
        return lexer
    
    @classmethod
    def str2args_kwargs_pair(cls, s_IN, maxsplit=None,):
        str_PARAM_list = cls.lexer2str_DELIM_list(cls.create_lexer(),
                                                  s_IN,
                                                  maxsplit=maxsplit,
                                                  )
        
        if not str_PARAM_list: return (None, str_PARAM_list)
        
        return (str2strip(str_PARAM_list[0]),
                lmap(str2strip,str_PARAM_list[1:]),
                )
        
    @classmethod
    def str2args_kwargs_pair_NEW(cls, s_IN, split_ARG_str,):
        str_PARAM_list = cls.lexer2str_DELIM_list(cls.create_lexer(),
                                                  s_IN,
                                                  )
        
        if not str_PARAM_list: return (None, str_PARAM_list)
        
        return (str2strip(str_PARAM_list[0]),
                lmap(str2strip,str_PARAM_list[1:]),
                )

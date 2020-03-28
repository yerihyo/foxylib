import re


class LexerTool:
    DELIM_AS_PREFIX = "P"
    DELIM_AS_SUFFIX = "S"
    DELIM_EXCLUDED = "X"
    
    @classmethod
    def is_token_escaped(cls, token_list_DELIM, tt_list_ESCAPE):
        if not token_list_DELIM: return False
        count_ESCAPE = next((i for i,tok_PREV in enumerate(reversed(token_list_DELIM)) if tok_PREV.type not in tt_list_ESCAPE),
                            len(token_list_DELIM),
                            )
        
        return count_ESCAPE%2!=0
    
    @classmethod
    def tok2is_STATE_START(cls, tok, token_list_DELIM, tt_list_ES, state_CUR, state_INITIAL):
        [tt_list_ESCAPE, tt_list_STATE] = tt_list_ES
        
        if tok.type not in tt_list_STATE: return False
        if state_CUR != state_INITIAL: return False
        
        is_escaped = cls.is_token_escaped(token_list_DELIM, tt_list_ESCAPE)
        return (not is_escaped)
        
    @classmethod
    def tok2is_STATE_END(cls, tok, token_list_DELIM, tt_list_ES, state_CUR,):
        [tt_list_ESCAPE, tt_list_STATE] = tt_list_ES
        
        if tok.type not in tt_list_STATE: return False
        if state_CUR != tok.type: return False
        
        is_escaped = cls.is_token_escaped(token_list_DELIM, tt_list_ESCAPE)
        return (not is_escaped)
    
    @classmethod
    def tok2is_DELIM(cls, tok, token_list_DELIM, tt_list_ED, stop_split, state_CUR, state_INITIAL):
        [tt_list_ESCAPE,tt_list_DELIM] = tt_list_ED 
        
        if tok.type not in tt_list_DELIM: return False
        
        #raise Exception(tok, stop_split, state_CUR, state_INITIAL)
    
        if stop_split: return False
        if state_CUR != state_INITIAL: return False
        
        # not sure whether DELIM should be escape-able
        is_escaped = cls.is_token_escaped(token_list_DELIM, tt_list_ESCAPE)
        
        return (not is_escaped)
    
    # Semantic 
    STT_DELIM = SEMANTIC_TOKEN_TYPE_DELIM = "D"
    STT_START = SEMANTIC_TOKEN_TYPE_STATE_START = "S"
    STT_END = SEMANTIC_TOKEN_TYPE_STATE_END = "E"
    STT_ANY = SEMANTIC_TOKEN_TYPE_STATE_ANY = "A"
    
    @classmethod
    def tok2semantic_token_type(cls, tok, token_list_DELIM, tt_list_ESD, stop_split, state_CUR, state_INITIAL,):
        def lfilter(*args, **kwargs): return list(filter(*args,**kwargs))
        [tt_list_ESCAPE,tt_list_STATE,tt_list_DELIM] = tt_list_ESD 
        tt_list_ES = [tt_list_ESCAPE, tt_list_STATE]
        tt_list_ED = [tt_list_ESCAPE,tt_list_DELIM,]

        is_STATE_START = cls.tok2is_STATE_START(tok, token_list_DELIM, tt_list_ES, state_CUR, state_INITIAL,)
        is_STATE_END = cls.tok2is_STATE_END(tok, token_list_DELIM, tt_list_ES, state_CUR)
        is_DELIM = cls.tok2is_DELIM(tok, token_list_DELIM, tt_list_ED, stop_split, state_CUR, state_INITIAL,)
        
        if len(lfilter(bool, [is_DELIM,is_STATE_START,is_STATE_END,]))>1:
            raise Exception()
        
        if is_DELIM: return cls.STT_DELIM
        if is_STATE_START: return cls.STT_START
        if is_STATE_END: return cls.STT_END
        
        # ALL THE OTHERS
        return cls.STT_ANY
    
    @classmethod
    def token_list_DELIM2str_DELIM(cls, token_list_DELIM):
        return "".join([x.value for x in token_list_DELIM])
    
    
    @classmethod
    def str2str_token_list(cls, lexer, data, tok_type_ll, maxsplit=None, include_tokens=False, ):
        (tt_list_APPEND,
         tt_list_DELIM,
         ) = tok_type_ll
        
        lexer.input(data)
        
        l = []
        l_tmp = []
        while True:
            tok = lexer.token()
            if not tok:  break

            if tok.type in tt_list_APPEND:
                l_tmp.append(tok)
                continue
            
            if tok.type in tt_list_DELIM:
                stop_split = (maxsplit is not None) and (len(l) >= maxsplit)
                if stop_split:
                    l_tmp.append(tok)
                    continue
                
                if l_tmp:
                    l.append("".join([x.value for x in l_tmp]))
                    l_tmp = []
                
                if include_tokens:
                    l_tmp.append(tok)
        
        if l_tmp:
            l.append("".join([x.value for x in l_tmp]))
            
        #raise Exception()
    
        return l
    
    @classmethod
    def str_token_list2args_kwargs_pair(cls, l_token):
        if not l_token: return (None, l_token)
        
        m_first_token_has_prefix = re.match(r"\s*[+\-*/]", l_token[0])
        if not m_first_token_has_prefix: return (l_token[0],l_token[1:])
        raise Exception()
        #else: return (None, l_token)


class MultipleColonInCommandError(Exception):
    @classmethod
    def check_and_raise(cls, s_COLON_list, s_IN):
        colon_count = len(s_COLON_list)-1
        if colon_count<=1: return
        data = {"colon_count":colon_count,
                "s_IN":s_IN,}
        raise cls(data)

    chk_n_raise = check_and_raise
# MCICErr = MultipleColonInCommandError

    

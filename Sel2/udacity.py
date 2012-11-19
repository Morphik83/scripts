def remove_html_markup(s):
    tag = False
    quote = False
    out = ""
    for c in s:
        if quote and not tag:
            raise ValueError
        
        if c == "<" and not quote:    #Start of markup
            tag = True
        elif c == ">" and not quote:
            tag = False
       
        #=======================================================================
        # elif c == '"' or c == "'" and tag:
        #    quote = not quote
        # OR has lower precedence than AND, so code would be interpreted as:
        # elif c == '"' or (c == "'" and tag)
        # So, if c=='"' -> TRUE. OR returns first TRUE, so next condition(AND) is not being checked
        # and the 'quote=not quote' is executed (" is stripped in that way)
        # On the other hand, it c=="'", then second condition is executed, but 'tag' is FALSE, so 
        # 'quote=not quote' is NOT executed, and that is why "'" is stripped from string.
        # FIRST SOLUTION: elif (c == '"' or c == "'") and tag
        #
        # SECOND SOLUTION:
        # possible states of this program: ^quoteAND^tag ->occurs > -> ^quoteANDtag -> quoteANDtag -> ^quoteANDtag -> ^quoteAND^tag
        # we do not want to have: quoteAND^tag (so quotes outside of the tags) -> this code should never be reached
        # IF (quotesAND^tag) raise error
        #          ==
        # IF NOT !(quotesAND^tag) raise error
        #          ==
        # IF NOT (tagOR^quotes) raise error
        #          ==
        # assert tag or not quotes -> this statement put at the very beginning to avoid erroneous behavior 
        # or put: if quote and not tag:
        #            raise ValueError
        # this is the same as assert!
        #=======================================================================
        
        elif c == '"' or c == "'" and tag:  #quote can be true only when tag is true! 
            quote = not quote
        elif not tag:
            out = out + c
    return out

#===============================================================================
# assert condition is the same as:
# if __debug__:
#    if not condition: raise AssertionError
#===============================================================================

def kelivinToFahrenheit(temperature):
    assert(temperature>=0), "Colder than absolute zero!"
    return ((temperature-273)*1.8)+32

def temp_converter(var):
    try:
        return int(var)
    except ValueError, e:
        print "The argument does not contain numbers\n", e
        


if __name__ == '__main__':
    s="'foo'"
    #s="'foo'"
    print remove_html_markup(s)
    
    #print temp_converter('xyz')
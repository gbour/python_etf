# -*- coding: utf8 -*-

import re, os

def serialize(val, **kwargs):
    # "<class 'erl_terms.objects.Proplist'>" -> proplist
    typ = str(type(val)).split("'")[1].split('.')[-1].lower()

    try:
        return eval("_"+typ)(val, **kwargs)
    except NameError, e:
        raise BaseException("unsupported {0} type".format(type(val)))


###


def _int(val, out, **kwargs):
    out.write(str(val))

def _float(val, out, **kwargs):
    out.write(str(val))

def _bool(val, out, **kwargs):
    out.write(str(val).lower())

def _str(val, out, **kwargs):
    out.writelines(['"', val, '"'])

def _atom(atom, out, **kwargs):
    if re.match("^[a-z][0-9a-zA-Z]*$", atom):
        out.writelines(atom)
    else:
        out.writelines(["'", atom, "'"])

def _list(lst, out, cr, sp, csp, depth, **kwargs):
    if len(lst) == 0:
        out.write('[]')
    else:
        kwargs.update({'cr': cr, 'sp': sp, 'csp': csp, 'depth': depth+1})
        # forcing uniline when number of list elements < 11 (even if pretty mode)
        if len(lst) < 6:
            sp = ''; cr = ''; csp = ' '

        out.writelines(['[', cr])
        for v in lst[:-1]:
            out.write(sp*(depth+1))
            serialize(v, out=out, **kwargs)
            out.writelines([',', csp, cr])

        out.write(sp*(depth+1))
        serialize(lst[-1], out=out, **kwargs)
        out.writelines([cr, sp*depth, ']'])

def _tuple(tupl, out, cr, sp, csp, depth, **kwargs):
    if len(tupl) == 0:
        out.write('{}')
    else:
        kwargs.update({'cr': cr, 'sp': sp, 'csp': csp, 'depth': depth+1})

        # forcing uniline when number of list elements < 11 (even if pretty mode)
        if len(tupl) < 6:
            sp = ''; cr = ''; csp = ' '

        out.writelines(['{', cr])
        for v in tupl[:-1]:
            out.write(sp*(depth+1))
            serialize(v, out=out, **kwargs)
            out.writelines([',', csp, cr])

        out.write(sp*(depth+1))
        serialize(tupl[-1], out=out, **kwargs)
        out.writelines([cr, sp*depth, '}'])

def _proplist(dct, out, cr, sp, csp, depth, **kwargs):
    if len(dct) == 0:
        out.write('[]')
    else:
        kwargs.update({'cr': cr, 'sp': sp, 'csp': csp, 'depth': depth+1})

        # forcing uniline when number of list elements < 11 (even if pretty mode)
        #if len(dct) < 11:
        #    sp = ''; cr = ''; csp = ' '

        out.writelines(['[', cr])
        for k in sorted(dct.keys()):
            out.writelines([sp*(depth+1), '{'])
            serialize(k, out=out, **kwargs)
            out.write(', ')
            serialize(dct[k], out=out, **kwargs)
            out.writelines(['},', csp, cr])


        out.seek(-len(csp+cr)-1, os.SEEK_END); out.truncate()
        out.writelines([cr, sp*depth, ']'])

def _dict(dct, out, cr, sp, csp, depth, **kwargs):
    if len(dct) == 0:
        out.write('#{}')
    else:
        kwargs.update({'cr': cr, 'sp': sp, 'csp': csp, 'depth': depth+1})

        # forcing uniline when number of list elements < 11 (even if pretty mode)
        if len(dct) < 6:
            sp = ''; cr = ''; csp = ' '

        out.writelines(['#{', cr])
        for k in sorted(dct.keys()):
            out.write(sp*(depth+1))
            serialize(k, out=out, **kwargs)
            out.write(' => ')
            serialize(dct[k], out=out, **kwargs)
            out.writelines([',', csp, cr])


        out.seek(-len(csp+cr)-1, os.SEEK_END); out.truncate()
        out.writelines([cr, sp*depth, '}'])


#!/usr/bin/env python3

"""
code developed by [github.com/nessimk] as part of a solution to quickly cobble together yaml files, markdown and templating to produce a single pdf.

If you're deperate enough to want to use it, be my guest, it's licensed under the MIT license.

Copyright 2019 [github.com/nessimk]

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import yaml
import sys
import re
import logging
import numbers
import pdb
import os

"""
    replace all \n- with \n<indent spaces>-
"""
def reformatList(l, indent):
    return re.sub("\n-", "\n{}-".format(" " * indent), l)

"""
    replace all \n\n with \n<indent spaces>\n
"""
def reformatMultiParagraph2(l, indent):
    m = re.sub("\n-", "\n{}-".format(" " * indent), l)
    l = re.sub("\n\*", "\n{}*".format(" " * indent), m)
    #pdb.set_trace()
    m = re.sub(r"\n\n(?!\s)([\w].*)", r"\n\n{}\1".format(" " * indent), l, flags=re.UNICODE)
    return m

"""
    replace all \n\n with \n<indent spaces>\n
"""
def reformatMultiParagraph(l, indent):
    return re.sub("\n\n", "\n\n{}".format(" " * indent), l)

"""
    naively render python objects originally loaded from the yaml to markdown (aka, I can't believe there isn't already an easily reusable solution that does this)
    indent is the number of spaces we need to indent the result with
    
    There are a number of problems here: 
    The text loses its original indentation once its loaded into a python object (mostly a plain old string).
    To keep downstream elements of our pipeline happy (e.g. hugo build system) we need to recover some elements of it.
    Currently that means trying to guess yaml lists and multi paragraph strings and adjusting their level of indentation to match
    the insertion point in the template.

    FIXME: That is brittle and horribly hackish. There must be a correct way of doing this and we should change this before it becomes too encrusted in the code.

"""
def pyObj2md(o, indent):
    md = ""
    #pdb.set_trace()

    if type(o) is str:
        o = reformatMultiParagraph2(o, indent)
        if o.startswith("-"):
            logging.debug("Looks like i'm handling a list. Trying to adjust its indentation level\n")
            return reformatList(o, indent)

        """
        elif "\n\n" in o:
            logging.debug("Looks like i'm handling a multi-paragraph. Trying to adjust its indentation level\n")
            return reformatMultiParagraph(o, indent)
        """
        return o

    elif type(o) is int:
        return str(o)

    elif type(o) is list:
        for elem in o:
            md += format("{}- {}\n".format(" "*indent, elem))
        return md[indent:]
    else:
        raise Exception("Don't know how to render objects of type %s in markdown (object is %s)\n" % (type(o), o))

"""
    handle templates like: {{item.sub}} 
    if item is a list of dicts, return a list of values for all 'sub' key
    if item is a dict, just return key sub.
"""
def handle_subitem(ns, key):
    logging.debug("key %s uses dot notation\n" % key)
    (item, sub) = key.split('.')
    value = None
    
    try:
        whatType = type(yamlData[ns][item])
        logging.debug("%s has type %s: %s\n" % (item, whatType, yamlData[ns][item]))

        if whatType is list:
            """
            handle the Text element in Values in AnswerSets
            """
            value = [level[sub] for level in yamlData[ns][item] if sub in level]

        elif whatType is dict:
            """
            not tested. we don't currently have a use case for this. should remove it.
            TODO: test and rewrite as dict comprehension
            """
            logging.debug("will return all %s keys in dict %s\n" % (sub, item))
            value = [] 
            for (level, contents) in yamlData[ns][item].items():
                if sub in contents:
                    value.append(contents[sub])

        elif whatType==str or isinstance(yamlData[ns][item], numbers.Number):
            # anything other than a dict. 
            # does it make sense to use dot notation to access plain lists?
            logging.debug("assuming %s is a simple dict\n" % yamlData[ns])
            value = yamlData[ns][item][sub]

    except KeyError as e:
        # not sure what to do with this complex thing. give up.
        logging.error("Don't know how to parse sub-item %s in namespace %s. Sorry. The error was: \n" % (key, ns, e))
        raise(e)

    return value

def doit(m):
    logging.debug("0: %s\n1: %s\n2: %s\n" % (m.group(0), m.group(1), m.group(2)))

    ns = m.group(1)
    try:
        ns = ns[:-1]
    except TypeError: # ns is None
        ns = no_ns
    try:
        key = m.group(2)
        """
        we need to support sub-item (e.g. values.text)
        this gets complicated when values is a list of dicts (e.g. for values in AnswerSet)
        in that case, return a list of 
        """
        if '.' in key:
            val = handle_subitem(ns, key)
        else:
            val = yamlData[ns][key]

        logging.debug("%s in %s -> %s\n" % (key, ns, val))

    except Exception as err:
        logging.error("EE: failed to find key '%s' in namespace '%s': %s\n" % (key, ns, err))
        sys.exit(1)

    return pyObj2md(val, m.start(0))

"""
    shortens the filenames dividing by slashes
    (i.e. D-Security-Architecture => D-SA)
"""
def get_short_filename(original_string):
    sections = original_string.split('-')

    if len(sections) == 1:
        return original_string

    new_name = sections[0] + '-' + ''.join(part[0] for part in sections[1:])
    return new_name
   
def get_original_eng_practice_name_from_filename(filename):
    # Get the base name of the file (without the directory path and extension)
    basename = os.path.splitext(os.path.basename(filename))[0]
    
    # Split the filename by the first hyphen
    parts = basename.split('-', 1)
    
    # If there was a hyphen, return the part after it, converted to lowercase
    if len(parts) > 1:
        result = parts[1].lower()
        return result
    else:
        return filename

if __name__ == '__main__':
    if len(sys.argv) != 3 and len(sys.argv) != 4:
        print("Usage: %s <yaml.namespace> <template.markdown>" % sys.argv[0])
        sys.exit(1)

    logging.basicConfig(level = logging.INFO)
    arg_ns = sys.argv[1]
    arg_tmpl = sys.argv[2]
    language = sys.argv[3] if len(sys.argv) > 3 else None
    no_ns='NO_NS'

    yamlData = {}
    namespaces = {}

    for line in open(arg_ns, 'r').readlines():
        line = line.strip()

        if line.startswith('#') or line=='':
            logging.debug("skipping %s\n" % line)
            continue

        try:
            (ns, file) = line.split(':')
            namespaces[ns.strip()] = file.strip()
            logging.debug("main namespace '%s' from '%s'\n" % (ns.strip(), namespaces[ns.strip()]))

        except ValueError:
            namespaces[no_ns] = line.strip()
            logging.debug("main defaulting to namespace '%s' from '%s'\n" % (no_ns, namespaces[no_ns]))
            continue 

        except Exception as err:
            logging.error("EE: failed to parse yaml file %s: %s" % (arg_ns, err))
            sys.exit(1)

    # load each file in the yamlDict into its own namespace
    try:
        for ns,file in namespaces.items():
            yamlData[ns] = yaml.load(open(file, 'r').read(), Loader=yaml.SafeLoader)
            logging.debug("DD: %s (%s) -> %s" % (file, ns, yamlData[ns]))
            basename = os.path.basename(file)
            filename_without_extension = os.path.splitext(basename)[0]
            yamlData[ns]["filename"] = filename_without_extension
            yamlData[ns]["lowercaseFilename"] = filename_without_extension.lower()
            '''
            TODO
            Previously the urls for the security practices and business functions were derived from the name. That worked until we had translations in other languages
            because now strategy-and-metrics is going to be different in different languages. That way we will have multiple urls for each language. 
            I changed the logic to use the filenames which are always in English. However, the security practice filenames are different from the practice names. 
            Example - Requirements-driven Testing is in filename D-Requirements-Testing. Strategy and Metrics is in filename Strategy-Metrics, etc.
            Using the practice filename as url is going to change and break existing links (url will be requirements-testing instead of requirements-driven-testing).
            One of my suggestions is to change the filenames to be correct and derive the URL from there (see function get_original_eng_practice_name_from_filename). 
            Other possibility is using some config file from the website repository that will tell us which practice/function from what URL should be served
            or hardcoding the urls here. Until we made a decision I am going to use the filenames as URL and hardcode those URLs of practices that have difference between the filename and practice name.
            '''
            practiceUrl = get_original_eng_practice_name_from_filename(file)
            if ns == 'practice' or ns.startswith('practice_'):
                practiceId = yamlData[ns]['id']
                if practiceId == "32b3bdd85d3a4d53827960004f9d1c7e":
                    practiceUrl = "strategy-and-metrics"
                if practiceId == "483a0a1b78264cafbc470ce72d557332":
                    practiceUrl = "education-and-guidance"
                if practiceId == "66fb99798fe946e4979a2de98e9d6f8b":
                    practiceUrl = "requirements-driven-testing"
                if practiceId == "be9e7ddb98b84abe8b9e185b979ccf60":
                    practiceUrl = "policy-and-compliance"
            yamlData[ns]["originalPracticeEngName"] = practiceUrl
            yamlData[ns]["shortFilename"] = get_short_filename(filename_without_extension)
            yamlData[ns]["langPrefix"] = '' if language is None else f'/{language}'

    except Exception as err:
        logging.error("EE: failed to parse yaml file %s: %s" % (file, err))

    # read the template file. We do it line by line to know the offset of the regex matches from start of line to correct yaml indentatio. see pyObj2md()
    # it's quite brittle though and should really be rewritten to something more presentable.
    try:
        lines = open(arg_tmpl, 'r').readlines()

    except Exception as err:
        logging.error("EE: failed to load template %s: %s" % (arg_tmpl, err))
        sys.exit(1)

    logging.debug("DD: using template:\n%s\n" % arg_tmpl)

    """
        this is the regex we use to match our templates. We currently understand:
        {{namespace:item}}
        {{namespace:item.subitem}}
    """
    pat = re.compile('{{([\w_-]+:)?(.+?)}}')

    for l in lines:
        print(re.sub(pat, doit, l.rstrip()))

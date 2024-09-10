#!/usr/bin/env python3

"""
code developed by [github.com/nessimk] as part of a solution to quickly cobble together yaml files, markdown and templating to produce a single pdf.

If you're deperate enough to want to use it, be my guest, it's licensed under the MIT license.

Copyright 2019 [github.com/nessimk]

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import sys
import os
import logging
import glob
import yaml
import pdb
import argparse

class Sammpdf:
    def __init__(self, model):
        self.model = model
        # FIXME: this has grown useless. consider replacing with a pageOrder per section (e.g. intor, overview of functions, function details, activities, outro)
        # that way each function can build the list as it needs it and main can orchestrate.
        self.pageOrder = []


    """
    For consistency, we output a template and namespace files although we could output the full final result (yaml/markdown)
    This at the cost of requiring further post processing (for example, we need to fix up the casing of practice_X_url and replace spaces with hyphens.

    outputs:
        - 1 namespace file for each business function
    """
    def writeWebBusinessFunctions(self, namespaceBase):

        for function in self.model.getBusinessFunctions(ordered=True):
            functionName = function.getOriginalEngFileNameNoExt()
            _namespace = open("{}{}.ns".format(namespaceBase, functionName) , 'w')
            logging.debug("writing ns %s\n" % _namespace.name)

            _namespace.write("function:%s\n" % function.getYamlFile())
            for practice in self.model.getPracticesBy(function=function, ordered=True):
                _namespace.write("practice_%d: %s\n" % (practice.getOrder(), practice.getYamlFile()))
            _namespace.close()


    """
        output: 1 file containing 1 activity title per line
    """
    def writeActivities(self, *, output):
        trace = False
        logging.debug("Writing Activities to {}\n".format(output))
        with open(output, 'w') as _out:
            for function in self.model.getBusinessFunctions():
                for practice in self.model.getPracticesBy(function=function):
                    for maturity in self.model.getMaturityLevels():
                        for stream in self.model.getStreamsBy(practice=practice):
                            practiceLevel = self.model.getPracticeLevelBy(practice=practice, maturityLevel=maturity, trace=trace)
                            for activity in self.model.getActivitiesBy(stream=stream, practiceLevel=practiceLevel, trace=trace):
                                _out.write("{}\n".format(activity.getTitle()))

    """
    write:
      - 1 namespace file per practice for each business functions
    """
    def writeWebPractices(self, *, namespaceBase):
        trace = False

        for function in self.model.getBusinessFunctions(ordered=True):
            functionName = function.getOriginalEngFileNameNoExt()
            for practice in self.model.getPracticesBy(function=function):
                _namespace = open("{}{}-{}.ns".format(namespaceBase, functionName, practice.getShortName()), 'w')
                logging.debug("writing ns {}\n".format(_namespace.name))

                _namespace.write("function: %s\n" % function.getYamlFile())
                _namespace.write("practice: %s\n" % practice.getYamlFile())

                for stream in self.model.getStreamsBy(practice=practice):
                    _namespace.write("stream-%s: %s\n" % (stream.getLetter().lower(), stream.getYamlFile()))

                    for maturity in self.model.getMaturityLevels():
                        practiceLevel = self.model.getPracticeLevelBy(practice=practice, maturityLevel=maturity, trace=trace)

                        if stream.getLetter().lower() == 'a':
                            # Hack: Only write the practiceLevel once to the namespace
                            _namespace.write("practiceLevel-{}: {}\n".format(maturity.getNumber(), practiceLevel.getYamlFile()))

                        for activity in self.model.getActivitiesBy(stream=stream, practiceLevel=practiceLevel, trace=trace):
                            _namespace.write("stream-%s-maturity-%d-activity: %s\n" % (stream.getLetter().lower(), maturity.getNumber(), activity.getYamlFile()))
                _namespace.close()

    """
    write:
      - 1 namespace file per activity stream per practice per each business functions
    """
    def writeWebActivityStreams(self, *, namespaceBase):
        trace = False

        for function in self.model.getBusinessFunctions(ordered=True):
            functionName = function.getOriginalEngFileNameNoExt()
            for practice in self.model.getPracticesBy(function=function):
                for stream in self.model.getStreamsBy(practice=practice):

                    _namespace = open("{}{}-{}-{}.ns".format(namespaceBase, functionName, practice.getShortName(), stream.getLetter()), 'w')
                    logging.debug("writing ns {}\n".format(_namespace.name))

                    _namespace.write("function: {}\n".format(function.getYamlFile()))
                    _namespace.write("practice: {}\n".format(practice.getYamlFile()))
                    _namespace.write("stream: {}\n".format(stream.getYamlFile()))

                    for maturity in self.model.getMaturityLevels():
                        maturityNum=maturity.getNumber()
                        _namespace.write("maturity-{}: {}\n".format(maturityNum, maturity.getYamlFile()))

                        practiceLevel = self.model.getPracticeLevelBy(practice=practice, maturityLevel=maturity, trace=trace)

                        # should only be 1. Any sense in keeping this a list?
                        for activity in self.model.getActivitiesBy(stream=stream, practiceLevel=practiceLevel, trace=trace):
                            _namespace.write("activity-{}: {}\n".format(maturityNum, activity.getYamlFile()))

                            question = self.model.getQuestionBy(activity=activity, trace=trace)
                            _namespace.write("question-{}: {}\n".format(maturityNum, question.getYamlFile()))

                            answerset = self.model.getAnswerSetBy(question=question, trace=trace)
                            _namespace.write("answerSet-{}: {}\n".format(maturityNum, answerset.getYamlFile()))

                    _namespace.close()


    """
        output: 1 namespace file per business function. used for the separator pages
    """
    def writeFunctionSeparators(self, *, namespaceBase):
        trace = False
        for function in self.model.getBusinessFunctions():
            with open("{}{}.ns".format(namespaceBase, function.getName()), 'w') as _out:
                logging.debug("Writing function name to {}\n".format(_out.name))
                _out.write("function:{}\n".format(function.getYamlFile()))

    """
    create the template file for the page describing the business functions and its corresponding namespace file.
    # TODO: consider rewriting using f-strings or some other improved string formatting
    """
    def writeBusinessFunctionDetail(self, *, namespaceBase):

        for function in self.model.getBusinessFunctions(ordered=True):

            _namespace = open("%s-%s.ns" % (namespaceBase, function.getName()) , 'w')

            # TODO: find a cleaner way of passing a filename template in. we could define some printf style formatters
            logging.debug("Creating namespace:%s\n" % (_namespace.name))

            # FIXME: quick hack, really need to cleaup handling of templates.
            # use the order of functions called in main to order the pages in the pdf.
            self.pageOrder.append(os.path.basename(_namespace.name))

            _namespace.write("function:{}\n".format(function.getYamlFile()))

            for practice in self.model.getPracticesBy(function=function):
                practiceNamespace = "practice-{}".format(practice.getOrder())
                _namespace.write("{}:{}\n".format(practiceNamespace, practice.getYamlFile()))

                for stream in self.model.getStreamsBy(practice=practice):
                    streamNamespace = "stream-{}-p{}".format(stream.getLetter(), practice.getOrder())
                    _namespace.write("%s:%s\n" % (streamNamespace, stream.getYamlFile()))

            _namespace.close()

    def writeBusinessFunctionsOverview(self, *, namespace):
        _namespace = open(namespace, 'w')

        # use the order of functions called in main to order the pages in the pdf.
        self.pageOrder.append(os.path.basename(_namespace.name))

        for function in self.model.getBusinessFunctions(ordered=True):
            fnNamespace = "function-{}".format(function.getOrder())
            _namespace.write("%s:%s\n" % (fnNamespace, function.getYamlFile()))

            for practice in self.model.getPracticesBy(function=function):
                practiceNamespace="{}-practice-{}".format(fnNamespace, practice.getOrder())
                _namespace.write("%s:%s\n" % (practiceNamespace, practice.getYamlFile()))

        _namespace.close()

    """
        Iterate over the model and print the necessary namespace statements used by any template files to generate the markdown.
    """
    def writeNamespaces(self, outputDir):
        # create a namespace file per activity per maturity level.
        setTrace = {}
        """
        setTrace['maturityLevel'] = 1
        setTrace['businessFunction'] = 'Verification'
        setTrace['practice.shortName'] = 'AA'
        """
        trace = False

        for maturity in self.model.getMaturityLevels(ordered=True):
            number = maturity.getNumber()

            for function in self.model.getBusinessFunctions(ordered=True):
                name = function.getName()

                for practice in self.model.getPracticesBy(function=function):
                    longDesc = practice.getLongDescription()

                    # horrible debugging hack. needs must..
                    try:
                        if practice.getShortName()==setTrace['practice.shortName'] and number==setTrace['maturityLevel']:
                            trace = True
                            pdb.set_trace()
                        else:
                            trace = False
                    except KeyError:
                        # no keys set for SetTrace{}
                        trace = False

                    fname = "%s/%s-%s-%d.ns" % (outputDir, name, practice.getShortName(), number)
                    ns = open(fname, 'w')

                    logging.debug("creating namespace %s-%s-%d.ns\n" % (name, practice.getShortName(), number))
                    ns.write("function: %s\n" % function.getYamlFile())
                    ns.write("practice: %s\n" % practice.getYamlFile())

                    practiceLevel = self.model.getPracticeLevelBy(practice=practice, maturityLevel=maturity, trace=trace)
                    ns.write("practice-level: %s\n" % practiceLevel.getYamlFile())

                    for stream in self.model.getStreamsBy(practice=practice, trace=trace):
                        ns.write("stream-%s: %s\n" % (stream.getLetter().lower(), stream.getYamlFile()))

                        for activity in self.model.getActivitiesBy(stream=stream, practiceLevel=practiceLevel, trace=trace):
                            longDesc = activity.getLongDescription()
                            ns.write("activity-%s: %s\n" % (stream.getLetter().lower(), activity.getYamlFile()))

                            question = self.model.getQuestionBy(activity=activity, trace=trace)
                            ns.write("question-%s: %s\n" % (stream.getLetter().lower(), question.getYamlFile()))

                            answerset = self.model.getAnswerSetBy(question=question, trace=trace)
                            ns.write("answerset-%s: %s\n" % (stream.getLetter().lower(), answerset.getYamlFile()))

                            # TODO: We still need to work out how this will be handled in the template. See https://github.com/OWASP/samm/issues/236
                            externalReferences = self.model.getExternalReferencesBy(activity=activity, trace=trace)
                            i=0
                            for er in externalReferences:
                                ns.write("externalref-%d: %s" % (i, er.getYamlFile()))
                                i=i+1

                    ns.write("maturity: %s\n" % maturity.getYamlFile())
                    ns.close()

    """
    generate a file containing the namespace files in the order in which
    they will be used in the pdf.
    This allows us to script the conversion of each file to pdf.
    """
    def writeBookOrder(self, orderFileName):
        orderedFiles = open(orderFileName, 'w')

        for page in self.pageOrder:
            orderedFiles.write("%s\n" % page)

        for function in self.model.getBusinessFunctions(ordered=True):
            name = function.getName()

            for practice in self.model.getPracticesBy(function=function):
                for maturity in self.model.getMaturityLevels(ordered=True):
                    number = maturity.getNumber()
                    fname = "%s-%s-%d.ns" % (name, practice.getShortName(), number)

                    orderedFiles.write("%s\n" % fname)
        orderedFiles.close()

class Model:
    def __init__(self):
        # do we need a dict or is a list enough?
        self.objs = {}

        # initialize a list for each type of object
        # NOTE: this is more a shortcut than an encapsulation thing since
        # this class knows about the internals and subclasses of the ModelObject

        for c in ModelObject.__subclasses__():
            logging.debug("creating self.objs[%s]\n" % c.__name__)
            self.objs[c.__name__] = []

    def getQuestionBy(self, *, activity, trace=False):
        if trace:
            pdb.set_trace()

        res = list(filter(lambda q: q.data['activity']==activity.data['id'], self.objs['Question']))

        if len(res) > 1:
            logging.warning("Found %d Questions when 1 was expected\n" % len(res))
        return res[0]


    def getAnswerSetBy(self, *, question, trace=False):
        if trace:
            pdb.set_trace()

        res = list(filter(lambda a: a.data['id']==question.data['answerSet'], self.objs['AnswerSet']))
        if len(res) > 1:
            logging.warning("Found %d Answer Sets when 1 was expected\n" % len(res))
        return res[0]

    def getStreamsBy(self, *, practice, trace=False):
       if trace:
           pdb.set_trace()

       _practice=practice.data['id']
       res = list(filter(lambda p: p.data['practice']==_practice, self.objs['Stream']))
       return sorted(res, key=lambda s: s.data['order'])

    """
    # CHECKME: completely untested, since we've abandoned this functionality for the current release.
    # return ExternalReference objects whose id matches one of the elements in an Activity's externalReferences list.
    # this needs to be worked out further, especially as the templating will have to be adapted first.
    """
    def getExternalReferencesBy(self, *, activity, trace=False):
        if trace:
            pdb.set_trace()

        # return an empty list to avoid impacting anything.
        return []
        res = list(filter(lambda er: er.data['id'] in activity.data['externalReference'], self.objs['externalReference']))
        return res


    def getActivitiesBy(self, *, stream, practiceLevel, trace=False):
        if trace:
            pdb.set_trace()

        _stream = stream.data['id']
        _practiceLevel = practiceLevel.data['id']


        res = list(filter(lambda a: a.data['stream']==_stream and a.data['level']==_practiceLevel, self.objs['Activity']))
        if len(res) == 0:
            msg = "Did not find any activities for stream {} in level {}. ".format(_stream, _practiceLevel)
            msg += "Make sure practiceLevel and stream guids are correct"
            logging.warning(msg)
        return res

    def getPracticeLevelBy(self, *, practice, maturityLevel, trace=False):
       if trace:
           pdb.set_trace()

       _practice = practice.data['id']
       _maturityLevel = maturityLevel.data['id']

       res = list(filter(lambda p: p.data['practice']==_practice and p.data['maturityLevel']==_maturityLevel, self.objs['PracticeLevel']))
       if len(res) > 1:
           logging.warning("Oups: Matched more than 1 PracticeLevel by practice=%s and maturityLevel=%s\n" % (str(practice), str(maturityLevel)))

       return res[0]


    def getPracticesBy(self, *, function, ordered=True, trace=False):
        if trace:
            pdb.set_trace()

        functionId=function.data['id']
        res = list(filter(lambda p: p.data['function']==functionId, self.objs['Practice']))
        return sorted(res, key=lambda p: p.data['order'])

    def getMaturityLevels(self, *, ordered=True):
        return sorted(self.objs['MaturityLevel'], key=lambda m: m.data['number'])

    def getBusinessFunctions(self, *, ordered=True):
        return sorted(self.objs['BusinessFunction'], key=lambda b: b.data['order'])

    def _addObj(self, data, filename):
        (obj, objClassName) = Model.classifyObj(data, filename)

        if obj is None:
            logging.error("oups, couldn't classify %s\n" % filename)
            sys.exit(1)

        obj.setFilename(filename)
        self.objs[objClassName].append(obj)
        logging.debug("classified %s as %s\n" % (filename, objClassName))


    @staticmethod
    def classifyObj(data, filename):
        matches = 0
        for modelObj in ModelObject.__subclasses__():
            #logging.debug("\t querying %s\n" % modelObj.__name__)

            # invoke the classe's staticmethod itsme(data)
            ok = modelObj.__dict__['itsme'].__func__(data)
            if ok:
                matches = matches + 1
                objType = modelObj
                logging.debug("\t %s will handle %s (%d matches)" % (modelObj.__name__, filename, matches))

        if matches > 1:
            logging.error("%s was matched by more than 1 object!\n" % filename)
            sys.exit(1)

        elif matches == 0:
            logging.error("%s was not matched by any object!\n" % filename)
            sys.exit(1)

        # the object was matched by 1 classifier, use it somehow.
        return (objType(data), objType.__name__)

class ModelObject:
    """
        data is a dict of values (most likely loaded from a yaml template)
    """
    def __init__(self, data, filename=None):
        self.data = data
        self.filename = filename

    def setFilename(self, filename):
        self.filename = filename

    @staticmethod
    def itsme(obj):
        return False

    def getData(self):
        return self.data

    def getYamlFile(self):
        return self.filename
    
    def getOriginalEngFileNameNoExt(self):
         basename = os.path.basename(self.filename)
         return os.path.splitext(basename)[0]

class BusinessFunction(ModelObject):
    @staticmethod
    def itsme(obj):
        if 'logo' in obj:
            return True
        return False

    def getName(self):
        return self.data['name']

    def getOrder(self):
        return self.data['order']

    def getDescription(self):
        return self.data['description']

class Practice(ModelObject):
    """
        FIXME: rewrite to just return the 'type' key and get rid of all specialized implementations once we add that to the yaml files
    """
    @staticmethod
    def itsme(obj):
        if 'function' in obj:
            return True
        return False

    def getLongDescription(self):
        return self.data['longDescription']

    def getshortDescription(self):
        return self.data['shortDescription']

    def getShortName(self):
        return self.data['shortName']

    def getOrder(self):
        return self.data['order']

    def getName(self):
        return self.data['name']

class MaturityLevel(ModelObject):
    @staticmethod
    def itsme(obj):
        try:
            return obj['type'] == 'MaturityLevel'
        except KeyError:
            return False

    def getNumber(self):
        return self.data['number']

class PracticeLevel(ModelObject):
    @staticmethod
    def itsme(obj):
        if 'maturityLevel' in obj:
            return True
        return False

class Stream(ModelObject):
    @staticmethod
    def itsme(obj):
        if 'letter' in obj:
            return True
        return False

    def getLetter(self):
        return self.data['letter']

class Activity(ModelObject):
    @staticmethod
    def itsme(obj):
        if 'benefit' in obj:
            return True
        return False

    def getLongDescription(self):
        return self.data['longDescription']

    def getTitle(self):
        return self.data['title']

class Question(ModelObject):
    @staticmethod
    def itsme(obj):
        if 'answerSet' in obj:
            return True
        return False

class AnswerSet(ModelObject):
    @staticmethod
    def itsme(obj):
        if 'values' in obj:
            return True
        return False

class ExternalReference(ModelObject):
    @staticmethod
    def itsme(obj):
        try:
            return obj['type'] == 'ExternalReference'
        except KeyError:
            return False


def loadYaml(directory):
    model = Model()

    templates = glob.glob(directory + '/**/*.yml', recursive=True)

    for t in templates:
        logging.debug(f'Loaded file {t}')
        model._addObj(yaml.load(open(t, 'r').read(), Loader=yaml.SafeLoader), t)

    return model

def handleArgs():
    parser = argparse.ArgumentParser(description="Parse SAMM2 model files and write templates for various output formats")
    parser.add_argument("--target", "-t", choices=["web", "pdf", "misc", "all"], required=True, help="For which target to generate the namespaces for")

    parser.add_argument("--output", "-o", required=True, type=str, help="Directory to write the namespace files to")
    parser.add_argument("--model", "-y", required=True, type=str, help="The Yaml model files directory")
    parser.add_argument("--loglevel", "-l", choices=["ERROR", "WARNING", "INFO", "DEBUG"], default="INFO", type=str, required=False, help="The log level to use")

    args = parser.parse_args()
    return args


def main():
    try:
        args = handleArgs()
    except Exception as e:
        logging.error("handleArgs had an error: %s" % e)
        sys.exit(0)

    logging.basicConfig(level = args.loglevel)
    directory = args.model

    logging.debug(f'Loading files in {directory}')

    model = loadYaml(directory)
    for (objtype, objs) in model.objs.items():
        logging.debug("loaded %d objects of type %s\n" % (len(objs), objtype))

    sammpdf = Sammpdf(model)

    if args.target in ["misc"]:
        sammpdf.writeActivities(output="{}/all-activities.txt".format(args.output))

    if args.target in ["pdf", "all"]:
        # currently the writeBusiness* methods assume they're called in the right order for the purposes of recording their template files
        # in the sammpdf.orderPages[] list. Need a cleaner approach to this in the long run.
        sammpdf.writeBusinessFunctionsOverview(namespace="{}/namespaces/businessFunctionsOverview.ns".format(args.output))
        sammpdf.writeBusinessFunctionDetail(namespaceBase="{}/namespaces/businessFunction".format(args.output))

        logging.debug("main: running writeNamespaces()\n")
        sammpdf.writeNamespaces("{}/namespaces".format(args.output))

        sammpdf.writeFunctionSeparators(namespaceBase="{}/namespaces/businessFunctionSeparator-".format(args.output))

        logging.debug("main: running writeBookOrder()\n")
        sammpdf.writeBookOrder("{}/ns.order".format(args.output))

    if args.target in ["web", "all"]:
        logging.debug("main: running writeWebBusinessFunctions()\n")
        sammpdf.writeWebBusinessFunctions(namespaceBase="{}/namespaces/{}".format(args.output, "function-"))

        logging.debug("main: running writeWebPractices()\n")
        sammpdf.writeWebPractices(namespaceBase="{}/namespaces/{}".format(args.output, "practice-"))

        logging.debug("main: running writeWebActivityStreams()\n")
        sammpdf.writeWebActivityStreams(namespaceBase="{}/namespaces/{}".format(args.output, "activity-"))


if __name__ == '__main__':
    main()

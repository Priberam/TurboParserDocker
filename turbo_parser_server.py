import logging
from turboparser import PyCppToPyTurboSink, PyCTurboTextAnalysis, PyLoadOptions, PyAnalyseOptions

logger = logging.getLogger('TurboParserServer')

class TurboParserServer():
    def __init__(self, language='en', data_path='/opt/TurboTextAnalysis/Data/', annotators=''):
        # similar to CoreNLP
        # https://stanfordnlp.github.io/CoreNLP/cmdline.html
        # TODO: tokenize and ssplit is not implemented yet.
        self.annotators = [a.strip() for a in annotators.split(',')]
        self.turbotextanalysis = PyCTurboTextAnalysis()

        # TurboParser original config file uses 'en', 'es', 'pt'
        language = 'en' if language == 'english' else language
        language = 'es' if language == 'spanish' else language
        language = 'pt' if language == 'portuguese' else language

        load_options = PyLoadOptions()
        load_options.load_tagger = True if 'pos' in annotators else False
        load_options.load_morphological_tagger = True if 'morph' in annotators else False
        load_options.load_entity_recognizer = True if 'ner' in annotators else False
        load_options.load_parser = True if 'parse' in annotators else False
        load_options.load_semantic_parser = True if 'sem' in annotators else False
        load_options.load_coreference_resolver = True if 'coref' in annotators else False
        retval = self.turbotextanalysis.load_language(language, data_path, load_options)
        if retval != 0:
            logger.error("ERROR in PyCTurboTextAnalysis load_language")
            logger.error("Error loading the model. Probably the models folder is empty.")
            exit()

    def parse(self, text, language, annotators=None):
        language = 'en' if language == 'english' else language
        language = 'es' if language == 'spanish' else language
        language = 'pt' if language == 'portuguese' else language

        if annotators is None or annotators == '':
            annotators = self.annotators
        else:
            annotators = [a.strip() for a in annotators.split(',')]

        # Process the text with Turbo
        sink = PyCppToPyTurboSink(True)
        options = PyAnalyseOptions()
        options.use_tagger = True if 'pos' in annotators else False
        options.use_parser = True if 'parse' in annotators else False
        options.use_morphological_tagger = True if 'morph' in annotators else False
        options.use_entity_recognizer = True if 'ner' in annotators else False
        options.use_semantic_parser = True if 'sem' in annotators else False
        options.use_coreference_resolver = True if 'coref' in annotators else False

        retval = self.turbotextanalysis.analyse(language, text, sink, options)
        if retval != 0:
            logger.error("ERROR in PyCTurboTextAnalysis analyse")
            logger.error("Return value: ", retval)
            exit()

        tokens_info = sink.get_tokens_info()

        conll_header = ['start_offset', 'end_offset', 'id', 'word']
        if 'lemma' in annotators:
            conll_header.append('lemma')

        if 'pos' in annotators:
            conll_header.append('pos')

        if 'ner' in annotators:
            conll_header.append('ner')

        if 'parse' in annotators:
            conll_header.append('head')
            conll_header.append('relation')

        if 'coref' in annotators:
            conll_header.append('coref')

        if 'sem' in annotators:
            conll_header.append('pred')
            conll_header.append('args')

        grids = []

        grid = []
        for x in tokens_info:
            start_offset = int(x['start_pos'])
            end_offset = start_offset + int(x['len'])
            word = x['word']
            token_id = int(x['features']['sentence_token_id'])

            conll_data = [start_offset, end_offset, token_id, word]

            if 'lemma' in annotators:
                conll_data.append(x['features']['lemma'])

            if 'pos' in annotators:
                conll_data.append(x['features']['pos_tag'])

            if 'ner' in annotators:
                conll_data.append(x['features']['entity_tag'])

            if 'parse' in annotators:
                conll_data.append(x['features']['dependency_head'])
                conll_data.append(x['features']['dependency_relation'])

            if 'coref' in annotators:
                conll_data.append(x['features']['coref_info'])

            if 'sem' in annotators:
                pred = x['features']['semantic_predicate']
                args = x['features']['semantic_arguments_list'].split('|')
                conll_data.append(pred)
                conll_data.append('\t'.join(args))

            token = {label: data for label, data in zip(conll_header, conll_data)}
            if token_id == 1 and len(grid) > 0:
                grids.append(grid)
                grid = []
            grid.append(token)

        if len(grid) > 0:
            grids.append(grid)

        conll_txt = []
        for grid in grids:
            str_grid = '\n'.join(['\t'.join([str(token[field]) for field in conll_header]) for token in grid])
            conll_txt.append(str_grid)

        return '\n\n'.join(conll_txt) + '\n'
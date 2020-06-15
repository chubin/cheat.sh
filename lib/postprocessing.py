import re
import fmt.comments

def postprocess(answer, keyword, options, request_options=None):
    answer = _answer_add_comments(answer, request_options=request_options)
    answer = _answer_filter_by_keyword(answer, keyword, options, request_options=request_options)
    return answer

def _answer_add_comments(answer, request_options=None):

    if answer['format'] != 'text+code':
        return answer

    topic = answer['topic']
    if "filetype" in answer:
        filetype = answer["filetype"]
    else:
        filetype = 'bash'
        if '/' in topic:
            filetype = topic.split('/', 1)[0]
            if filetype.startswith('q:'):
                filetype = filetype[2:]

    answer['answer'] = fmt.comments.beautify(
        answer['answer'], filetype, request_options)
    answer['format'] = 'code'
    answer['filetype'] = filetype
    return answer

def _answer_filter_by_keyword(answer, keyword, options, request_options=None):
    answer['answer'] = _filter_by_keyword(answer['answer'], keyword, options)
    return answer

def _filter_by_keyword(answer, keyword, options):

    def _join_paragraphs(paragraphs):
        answer = "\n".join(paragraphs)
        return answer

    def _split_paragraphs(text):
        answer = []
        paragraph = ""
        for line in text.splitlines():
            if line == "":
                answer.append(paragraph)
                paragraph = ""
            else:
                paragraph += line+"\n"
        answer.append(paragraph)
        return answer

    def _paragraph_contains(paragraph, keyword, insensitive=False, word_boundaries=True):
        """
        Check if `paragraph` contains `keyword`.
        Several keywords can be joined together using ~
        For example: ~ssh~passphrase
        """
        answer = True

        if '~' in keyword:
            keywords = keyword.split('~')
        else:
            keywords = [keyword]

        for kwrd in keywords:
            regex = re.escape(kwrd)
            if not word_boundaries:
                regex = r"\b%s\b" % kwrd

            if insensitive:
                answer = answer and bool(re.search(regex, paragraph, re.IGNORECASE))
            else:
                answer = answer and bool(re.search(regex, paragraph))

        return answer


    if not keyword:
        return answer

    search_options = {
        'insensitive': 'i' in options,
        'word_boundaries': 'b' in options
    }

    paragraphs = [p for p in _split_paragraphs(answer)
                  if _paragraph_contains(p, keyword, **search_options)]
    if not paragraphs:
        return ""

    return _join_paragraphs(paragraphs)

# Extends Sublime Text autocompletion to find matches in all open
# files. By default, Sublime only considers words from the current file.

import sublime_plugin
import sublime
import re
import time
from os.path import basename

MAX_FIX_TIME_SECS_PER_VIEW = 0.01


class toluaAutocomplete(sublime_plugin.EventListener):

    def on_query_completions(self, view, prefix, locations):
        words = []
        view_words =  view.extract_completions(prefix.upper(), locations[0]) + view.extract_completions(prefix.lower(), locations[0])
        view_words = fix_truncation(view, view_words)
        words += [(w, view) for w in view_words]

        words = without_duplicates(words)
        matches = []
        for w, v in words:
            trigger = w
            contents = w.replace('$', '\\$')
            if v.id != view.id and v.file_name():
                trigger += '\t(%s)' % basename(v.file_name())
            matches.append((trigger, contents))
        return matches

def without_duplicates(words):
    result = []
    used_words = []
    for w, v in words:
        if w not in used_words:
            used_words.append(w)
            result.append((w, v))
    return result


# Ugly workaround for truncation bug in Sublime when using view.extract_completions()
# in some types of files.
def fix_truncation(view, words):
    fixed_words = []
    start_time = time.time()

    for i, w in enumerate(words):
        #The word is truncated if and only if it cannot be found with a word boundary before and after

        # this fails to match strings with trailing non-alpha chars, like
        # 'foo?' or 'bar!', which are common for instance in Ruby.
        match = view.find(r'\b' + re.escape(w) + r'\b', 0)
        truncated = is_empty_match(match)
        if truncated:
            #Truncation is always by a single character, so we extend the word by one word character before a word boundary
            extended_words = []
            view.find_all(r'\b' + re.escape(w) + r'\w\b', 0, "$0", extended_words)
            if len(extended_words) > 0:
                fixed_words += extended_words
            else:
                # to compensate for the missing match problem mentioned above, just
                # use the old word if we didn't find any extended matches
                fixed_words.append(w)
        else:
            #Pass through non-truncated words
            fixed_words.append(w)

        # if too much time is spent in here, bail out,
        # and don't bother fixing the remaining words
        if time.time() - start_time > MAX_FIX_TIME_SECS_PER_VIEW:
            return fixed_words + words[i+1:]

    return fixed_words


if sublime.version() >= '3000':
    def is_empty_match(match):
        return match.empty()
else:
    def is_empty_match(match):
        return match is None
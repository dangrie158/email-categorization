#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Usage: %s output_dir corpus_name

Extracts and normalizes all texts that are saved by the rss feed-crawler.
The resulting file is a usable corpus for training with word2vec
"""

from pymongo import MongoClient
from normalizr import Normalizr
import codecs
import re
import sys

normalizr = Normalizr(language='de')

normalizations = [
    'remove_extra_whitespaces',
    'replace_hyphens',
    'remove_accent_marks',
    'replace_symbols',
    ('replace_punctuation', {'replacement': ' '})
]

category_extractors = {
    u'Spiegel': re.compile(r"http://www\.spiegel\.de/(\w+)/"),
    u'Tagesschau': re.compile(r"http://www\.tagesschau\.de/(\w+)/"),
    u'N24': re.compile(r"http://(?:www|feeds)\.n24\.de(?:/~r)?/n24/([a-cA-Ce-xE-X_]+)/(\w*)"),
    u'NTV': re.compile(r"http://www\.n-tv\.de/(\w*)/"),
    u'Zeit': re.compile(r"http://www\.zeit\.de/(?:(politik)/(\w*)|(\w*))/"),
    u'Welt': re.compile(r"https://www\.welt\.de/(?:(politik)/((?!article)\w*)|(\w*))/"),
    u'FAZ': re.compile(r"http://www\.faz\.net/aktuell/(\w*)/"),
    u'TAZ': None,
    u'Focus': re.compile(r"http://www\.focus\.de/(\w*)/"),
    u'Huffington Post': None,
    u'Deutsche Stimme': None,
    u'Junge Freiheit': re.compile(r"https://jungefreiheit\.de/(\w*)/"),
    u'Junge Welt': None,
    u'Süddeutsche': re.compile(r"http://www\.sueddeutsche\.de/(\w*)/"),
    u'Handelsblatt': re.compile(r"http://www\.handelsblatt\.com/(?:my/)?(\w*)/(?:(\w+)/|\w*-)"),
    u'WirtschaftsWoche': re.compile(r"http://www\.wiwo\.de/(\w*)/"),
    u'Netzpolitik': None,
    u'Telepolis': re.compile(r"https://www\.heise\.de/tp/(\w*)/"),
    u'Golem': 'IT',
    u'RT': None,
    u'Stern': None,
    u'RP Online': re.compile(r"http://www\.rp-online\.de/(\w*)/"),
    u'Der Postillion': None,
    u'Titanic': None,
    u'Vice': None,
    u'Volksstimme': re.compile(r"http://www\.volksstimme\.de/deutschland-welt/(\w+)/"),
    u'Unsere Zeit': re.compile(r"http://www\.unsere-zeit\.de/de/\d+/(\w+)/"),
    u'Cicero': None
}

# This list is manually curated and maps the extracted freeform categories
# to fewer predefined categories. This list probably needs regular maintenance

category_mapping = {
    'Politik': ['politik_konjunktur', 'politischesBuch', 'politik_', 'Nachrichten_Politik', 'politik_deutschland', 'politik', 'innenpolitik', 'video_politik'],
    'Ausland': ['politik_ausland', 'ausland', 'internationale_politik', 'politik_international'],
    'Aktuell': ['newsticker', 'thema', 'eilmeldung', 'termine', 'pressemitteilung', 'news'],
    'Technologie': ['video_technik', 'Wissen_Mensch', 'spiegelwissen', 'technik_gadgets', 'netzwelt', 'wissenschaft', 'Nachrichten_Netzwelt', 'technik_medizin', 'Wissen_Technik', 'IT', 'Wissen_Job', 'Nachrichten_Auto', 'technologie', 'auto', 'digitales', 'technik', 'Nachrichten_Wissenschaft', 'digital', 'technik_zukunftdergesundheit'],
    'Kultur': ['kultur', 'Wissen_Kultur', 'Wissen_History', 'theorie_geschichte', 'Wissen_d', 'wissen'],
    'Wirtschaft': ['video_unternehmen', 'unternehmen_mittelstand', 'wirtschaft_soziales', 'wirtschaft', 'unternehmen', 'unternehmen_management', 'karriere', 'unternehmen_dienstleister', 'unternehmen_industrie', 'Nachrichten_Wirtschaft'],
    'Finanzen': ['finanzen_immobilien', 'finanzen_anlagestrategie', 'finanzen', 'finanzen_vorsorge', 'Wissen_Finanzen', 'wirtschaft_boerse_', 'finanzen_maerkte', 'immobilien', 'video_finanzen'],
    'Sport': ['Sport_tennis', 'Sport_Fussball', 'Sport_mehr', 'Sport_d', 'Sport_us', 'Sport_formel1', 'sport'],
    'Sonstiges': ['dev', 'spiegel', '2017', '21', 'allgemein', 'schlusslicht', '25', 'videos', 'incoming', 'fernsehen', 'Nachrichten_n24', 'campus', 'studium', 'feature', 'magazin', 'panorama', 'positionen', 'Nachrichten_Panorama', 'einestages', 'imBild', 'vorabmeldungen', 'feuilleton', 'debatte', 'features', 'vermischtes', 'aktion', 'panorama', 'hintergrund', 'mobilitaet', 'freitext', 'video_panorama', '2016'],
    'Ignore': ['newsletter', 'my', 'icon', 'videoblog', 'anzeigen', 'fotos', 'Teletext', 'images', 'quiztool', 'ardimport', 'leserbriefe', 'kolumnen_oliver', 'sptv', 'focustv', '22', 'kommentar', '32', '28', 'multimedia', 'video', 'kolumnen_Prof', 'fotostrecke'],
    'Lokal': ['kommunalpolitik', 'nrw', 'hamburg', 'deutschland', 'inland', 'regionales', 'regional'],
    'Lifestyle': ['shopping', 'stil', 'entdecken', 'lebenundlernen', 'reisen', 'Nachrichten_Verbraucher', 'familie', 'reise', 'leben', 'ratgeber', 'erfolg', 'Wissen_Gesundheit', 'Wissen_Reise', 'leute', 'gesundheit', 'spiele', 'gesellschaft']
}

def tryGetCategoryHardcoded(source):
    if 'sportschau' in source:
        return 'sport'
    else:
        return ''

def getFreeformCategory(entry):
    site = entry['site']
    source = entry['source']
    matcher = category_extractors[site]
    if matcher is None:
        return

    try:
        result = matcher.match(source)
    except AttributeError:
        return matcher
    else:
        if result != None:
            #if there are subcategories, join them with an underscore
            return '_'.join([x for x in result.groups() if x != None])
        else:
            return tryGetCategoryHardcoded(source)

def mapFreeformCategory(freeformCategory):
    for mapping, mapped_categories in category_mapping.items():
        if freeformCategory in mapped_categories:
            return mapping

def normalize(text):
    norm_text = re.sub(r'"|“|„|“', ' ', text)
    norm_text = normalizr.normalize(norm_text, normalizations)
    return norm_text.lower()

if __name__ == '__main__':

    if len(sys.argv) < 3:
        print(__doc__ % sys.argv[0].split("/")[-1])
        sys.exit(1)

    output_dir = sys.argv[1]
    corpus_name = sys.argv[2]

    print('connecting to db...')
    client = MongoClient('mongodb://localhost:27017/')
    db = client.articles

    all_articles = db.articles.find()

    saved_messages = 0
    print('found {} articles in db'.format(all_articles.count()))
    print('saving to disk')
    categories = {category: [] for category in category_mapping}

    # this list contains all freefor categories that could not be mapped to a predefined
    # category using the mapping in category_mapping
    unmapped_categories = set()

    for article in all_articles:

        freeformCategory, text = getFreeformCategory(article), normalize(article['text'])

        #normalize the text
        norm_text = normalize(text)

        category = mapFreeformCategory(freeformCategory)
        if category is None:
            unmapped_categories.add(freeformCategory)
        else:
            categories[category].append(norm_text)

        #print the current article count for each category
        count_stats = {category: len(items) for (category, items) in categories.items()}
        sys.stdout.write("\r {} / {} : {}".format(saved_messages, all_articles.count(), count_stats))
        saved_messages += 1

    print('\n')
    print('\n')

    print('saving corpora')
    for category_name, category in categories.items():
        file_name = output_dir + corpus_name + category_name + '.txt'
        print('saving {} corpus as {}'.format(category_name, file_name))
        category_file = codecs.open(file_name, 'w', 'utf-8')
        for text in category:
            category_file.write(text + '\n')

        category_file.close()


    #remove all None and empty string values from the list
    unmapped_categories = list(filter(None, unmapped_categories))
    if len(unmapped_categories) > 0:
        print('freeform categories that could not be mapped: {}'.format(unmapped_categories))
        print('consider adding them to the mapping')

    #print('corpus saved to file {}'.format(out_file_path))
    print('done.')
    print('')

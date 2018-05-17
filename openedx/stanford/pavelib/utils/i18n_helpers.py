"""
Tools for stanford i18n tasks
"""

from datetime import datetime
import copy
import fnmatch
import logging
import os

import django
from django.conf import settings
from i18n.execute import execute
import polib

LOG = logging.getLogger(__name__)


def clean_pofile(filename):
    LOG.info("Cleaning %s", filename)
    pofile = polib.pofile(filename)
    fix_header(pofile)
    fix_metadata(pofile)
    pofile.save()


def get_theme_dir():
    """
    Fetch the absolute path to the default theme directory
    """
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "openedx.stanford.lms.envs.aws")
    os.environ.setdefault("SERVICE_VARIANT", 'lms')
    django.setup()
    from openedx.core.djangoapps.theming.helpers import get_theme_base_dir
    return get_theme_base_dir(settings.DEFAULT_SITE_THEME)


def segment_pofile_lazy(filename, segments):
    """
    Segment a .po file using patterns in `segments`.

    The .po file at `filename` is read, and the occurrence locations of its
    messages are examined.  `segments` is a list of single key-value pairs:
    the keys are segment .po filenames, the values are lists of patterns::

        [
            {'django-studio.po': [
                'cms/*',
                'some-other-studio-place/*',
            ]},
            {'django-weird.po': [
                '*/weird_*.*',
            ]},
        ]

    If ANY of a message's occurrences match the patterns for a segment, then that
    message is written to the new segmented .po file (the first segment with
    matching patterns).

    Any message that matches no segments is written back to
    the original file.

    Arguments:
        filename (path.path): a path object referring to the original .po file.
        segments (list of dicts): specification of the segments to create.

    Returns:
        a set of path objects, all the segment files written.

    """
    source_po = polib.pofile(filename)
    LOG.info('Reading %s entries from %s', len(source_po), filename)

    # A new pofile just like the source, but with no messages. We'll put
    # anything not segmented into this file.
    remaining_po = copy.deepcopy(source_po)
    remaining_po[:] = []

    # Turn the segments list into two structures: segment_patterns is a
    # list of (pattern, segmentfile) pairs.  segment_po_files is a dict mapping
    # segment file names to pofile objects of their contents.
    segment_po_files = {filename.name: remaining_po}
    segment_patterns = []
    for segment in segments:
        segmentfile, patterns = segment.items()[0]
        segment_po_files[segmentfile] = copy.deepcopy(remaining_po)
        segment_patterns.extend((pat, segmentfile) for pat in patterns)

    # Examine each message in the source file. If any of its occurrences match
    # a pattern for a segment, it goes in the first such segment.  Otherwise, it
    # goes in remaining.
    for msg in source_po:
        segment_match = False
        for pat, segment_file in segment_patterns:
            for occ_file, _ in msg.occurrences:
                if fnmatch.fnmatch(occ_file, pat):
                    segment_po_files[segment_file].append(msg)
                    segment_match = True
                    break
            if segment_match:
                break

        if not segment_match:
            remaining_po.append(msg)

    # Write out the results.
    files_written = set()
    for segment_file, pofile in segment_po_files.items():
        out_file = filename.dirname() / segment_file
        if not pofile:
            LOG.error('No messages to write to %s, did you run segment twice?', out_file)
        else:
            LOG.info('Writing %s entries to %s', len(pofile), out_file)
            pofile.save(out_file)
            files_written.add(out_file)

    return files_written


def fix_header(pofile):
    """
    Replace default headers with Stanford headers
    """
    pofile.metadata_is_fuzzy = []
    header = pofile.header
    fixes = (
        ('SOME DESCRIPTIVE TITLE', 'Stanford OpenEdX translation file'),
        ('Translations template for PROJECT.', 'Stanford OpenEdX translation file'),
        ('YEAR', str(datetime.utcnow().year)),
        ('ORGANIZATION', 'Stanford University'),
        ("THE PACKAGE'S COPYRIGHT HOLDER", 'Stanford University'),
        (
            'This file is distributed under the same license as the PROJECT project.',
            'This file is distributed under the GNU AFFERO GENERAL PUBLIC LICENSE.'
        ),
        (
            'This file is distributed under the same license as the PACKAGE package.',
            'This file is distributed under the GNU AFFERO GENERAL PUBLIC LICENSE.'
        ),
        ('FIRST AUTHOR <EMAIL@ADDRESS>', 'Stanford OpenEdX Team'),
    )
    for src, dest in fixes:
        header = header.replace(src, dest)
    pofile.header = header


def fix_metadata(pofile):
    """
    Replace default metadata with Stanford metadata
    """
    fixes = {
        'PO-Revision-Date': datetime.utcnow(),
        'Report-Msgid-Bugs-To': '',
        'Project-Id-Version': 'stanford-openedx',
        'Language': 'en',
        'Last-Translator': '',
        'Language-Team': 'English',
    }
    pofile.metadata.update(fixes)


def merge_existing_translations(existing, target, lang):
    """
    Merge translations from existing file to target file for locale lang and
    push up to Transifex
    """
    from openedx.stanford.pavelib.i18n import CONFIG
    target_filename = "stanford_" + target + '.po'

    # Fetch common messages first
    msgcomm_template = 'msgcomm {existing_file} {target_source} -o {output}'
    target_source = CONFIG.source_messages_dir / target_filename
    common_file = CONFIG.get_messages_dir(lang) / 'common.po'
    msgcomm_cmd = msgcomm_template.format(
        existing_file=CONFIG.get_messages_dir(lang) / existing,
        target_source=target_source,
        output=common_file,
    )
    execute(msgcomm_cmd)

    msgmerge_template = 'msgmerge --no-fuzzy-matching {common_file} {target_source} -o {output}'
    msgmerge_cmd = msgmerge_template.format(
        common_file=common_file,
        target_source=target_source,
        output=CONFIG.get_messages_dir(lang) / target_filename,
    )
    execute(msgmerge_cmd)

    push_cmd = 'tx push -t -l {lang} -r stanford-openedx.{resource}'.format(lang=lang, resource=target)
    execute(push_cmd)

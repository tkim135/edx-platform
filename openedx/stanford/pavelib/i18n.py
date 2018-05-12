"""
Stanford internationalization tasks
"""

from __future__ import absolute_import, print_function

import logging
import os
import shutil
import subprocess as sp
import sys

from i18n.config import Configuration
from i18n.execute import execute
from i18n import segment
from path import Path
from paver.easy import task, cmdopts, needs, sh
import polib
from pavelib.utils.cmd import django_cmd
from .utils.i18n_helpers import fix_header, fix_metadata, get_theme_dir, segment_pofile_lazy

BASE_DIR = Path('.').abspath()
CONFIG = Configuration(filename=BASE_DIR / 'conf/locale/stanford_config.yaml')
LOG = logging.getLogger(__name__)

logging.basicConfig(stream=sys.stdout, level=logging.INFO)


@task
@needs(
    'pavelib.prereqs.install_prereqs',
)
def stanfordi18n_extract_platform():

    files_to_clean = set()

    babel_cmd_template = (
        'pybabel extract --mapping={config} '
        '--add-comments="Translators:" --keyword="interpolate" '
        '. --output={output}'
    )
    babel_mako_cfg = CONFIG.locale_dir / 'stanford_mako.cfg'
    mako_file = CONFIG.source_messages_dir / 'stanford_mako.po'
    babel_mako_cmd = babel_cmd_template.format(
        config=babel_mako_cfg,
        output=mako_file,
    )
    execute(babel_mako_cmd)
    files_to_clean.add(mako_file)

    babel_underscore_cfg = CONFIG.locale_dir / 'stanford_underscore.cfg'
    underscore_file = CONFIG.source_messages_dir / 'stanford_underscore.po'
    babel_underscore_cmd = babel_cmd_template.format(
        config=babel_underscore_cfg,
        output=underscore_file,
    )
    execute(babel_underscore_cmd)
    files_to_clean.add(underscore_file)

    # Rename django.po and djangojs.po to avoid being overwritten
    os.rename(CONFIG.source_messages_dir / 'django.po', CONFIG.source_messages_dir / 'django-saved.po')
    os.rename(CONFIG.source_messages_dir / 'djangojs.po', CONFIG.source_messages_dir / 'djangojs-saved.po')

    makemessages = 'django-admin.py makemessages -l en'
    ignores = ' '.join('--ignore="{}/*"'.format(d) for d in CONFIG.ignore_dirs)
    if ignores:
        makemessages += ' ' + ignores
    execute(makemessages)

    django_file = CONFIG.source_messages_dir / 'stanford_django.po'
    os.rename(CONFIG.source_messages_dir / 'django.po', django_file)
    files_to_clean.add(django_file)

    make_djangojs_cmd = makemessages + ' -d djangojs'
    execute(make_djangojs_cmd)

    djangojs_file = CONFIG.source_messages_dir / 'stanford_djangojs.po'
    os.rename(CONFIG.source_messages_dir / 'djangojs.po', djangojs_file)
    files_to_clean.add(djangojs_file)

    for filename in files_to_clean:
        LOG.info('Cleaning %s', filename)
        pofile = polib.pofile(filename)
        fix_header(pofile)
        fix_metadata(pofile)
        pofile.save()

    os.rename(CONFIG.source_messages_dir / 'django-saved.po', CONFIG.source_messages_dir / 'django.po')
    os.rename(CONFIG.source_messages_dir / 'djangojs-saved.po', CONFIG.source_messages_dir / 'djangojs.po')


@task
@needs(
    'pavelib.prereqs.install_prereqs',
)
def stanfordi18n_extract_theme(options):
    """
    Extract strings that need translation.
    """
    files_to_clean = set()
    theme_dir = get_theme_dir()
    babel_mako_cfg = theme_dir / 'conf/locale/babel_mako.cfg'
    template_dir = 'lagunita/lms/templates/'
    theme_file = CONFIG.source_messages_dir / 'theme.po'
    babel_cmd_template = (
        'pybabel extract --mapping={config} '
        '--add-comments="Translators:" --keyword="interpolate" '
        '--output={output} {template_dir}'
    )
    babel_mako_cmd = babel_cmd_template.format(
        config=babel_mako_cfg,
        output='../../edx-platform' / theme_file,
        template_dir=template_dir,
    )
    execute(babel_mako_cmd, working_directory=theme_dir)
    files_to_clean.add(theme_file)

    # Monkeypatch upstream function
    segment.segment_pofile = segment_pofile_lazy

    # Segment out tos strings into separate files
    segmented_tos = segment.segment_pofiles(CONFIG, CONFIG.source_locale)
    files_to_clean.update(segmented_tos)

    for filename in files_to_clean:
        LOG.info('Cleaning %s', filename)
        pofile = polib.pofile(filename)
        fix_header(pofile)
        fix_metadata(pofile)
        pofile.save()

    print('Done extracting theme')


@task
@needs('pavelib.i18n.i18n_validate_transifex_config')
def stanfordi18n_transifex_push():
    """
    Push source strings to Transifex for translation
    """
    execute('tx push -s -r stanford-openedx.theme')
    execute('tx push -s -r stanford-openedx.tos')
    execute('tx push -s -r stanford-openedx.privacy')
    execute('tx push -s -r stanford-openedx.honor')
    execute('tx push -s -r stanford-openedx.copyright')
    execute('tx push -s -r stanford-openedx.mako')
    execute('tx push -s -r stanford-openedx.django')
    execute('tx push -s -r stanford-openedx.djangojs')
    execute('tx push -s -r stanford-openedx.underscore')
    print('Pushed source files to Transifex')

    # merge in existing platform translations
    for lang in CONFIG.translated_locales:
        if not CONFIG.get_messages_dir(lang).exists():
            # Language not yet available in code, fetch from upstream Transifex
            print('Fetch upstream translations for ' + lang)
            break
        common_platform_template = 'msgcomm {platform_file} {new_source} -o {output}'
        mako_file = CONFIG.source_messages_dir / 'stanford_mako.po'
        common_mako = CONFIG.get_messages_dir(lang) / 'common_mako.po'
        common_mako_cmd = common_platform_template.format(
            platform_file=CONFIG.get_messages_dir(lang) / 'django.po',
            new_source=mako_file,
            output=common_mako,
        )
        execute(common_mako_cmd)

        msgmerge_template = 'msgmerge --no-fuzzy-matching {common_platform} {new_source} -o {output}'
        msgmerge_cmd = msgmerge_template.format(
            common_platform=common_mako,
            new_source=mako_file,
            output=CONFIG.get_messages_dir(lang) / 'stanford_mako.po'
        )
        execute(msgmerge_cmd)

        push_cmd = 'tx push -t -l {lang} -r stanford-openedx.mako'.format(lang=lang)
        execute(push_cmd)

        django_file = CONFIG.source_messages_dir / 'stanford_django.po'
        common_django = CONFIG.get_messages_dir(lang) / 'common_django.po'
        common_django_cmd = common_platform_template.format(
            platform_file=CONFIG.get_messages_dir(lang) / 'django.po',
            new_source=django_file,
            output=common_django,
        )
        execute(common_django_cmd)

        msgmerge_cmd = msgmerge_template.format(
            common_platform=common_django,
            new_source=django_file,
            output=CONFIG.get_messages_dir(lang) / 'stanford_django.po'
        )
        execute(msgmerge_cmd)

        push_django = 'tx push -t -l {lang} -r stanford-openedx.django'.format(lang=lang)
        execute(push_django)

        djangojs_file = CONFIG.source_messages_dir / 'stanford_djangojs.po'
        common_djangojs = CONFIG.get_messages_dir(lang) / 'common_djangojs.po'
        common_djangojs_cmd = common_platform_template.format(
            platform_file=CONFIG.get_messages_dir(lang) / 'djangojs.po',
            new_source=djangojs_file,
            output=common_djangojs,
        )
        execute(common_djangojs_cmd)

        msgmerge_cmd = msgmerge_template.format(
            common_platform=common_djangojs,
            new_source=djangojs_file,
            output=CONFIG.get_messages_dir(lang) / 'stanford_djangojs.po'
        )
        execute(msgmerge_cmd)

        push_djangojs = 'tx push -t -l {lang} -r stanford-openedx.djangojs'.format(lang=lang)
        execute(push_djangojs)

        underscore_file = CONFIG.source_messages_dir / 'stanford_underscore.po'
        common_underscore = CONFIG.get_messages_dir(lang) / 'common_underscore.po'
        common_underscore_cmd = common_platform_template.format(
            platform_file=CONFIG.get_messages_dir(lang) / 'djangojs.po',
            new_source=underscore_file,
            output=common_underscore,
        )
        execute(common_underscore_cmd)

        msgmerge_cmd = msgmerge_template.format(
            common_platform=common_underscore,
            new_source=underscore_file,
            output=CONFIG.get_messages_dir(lang) / 'stanford_underscore.po'
        )
        execute(msgmerge_cmd)

        push_underscore = 'tx push -t -l {lang} -r stanford-openedx.underscore'.format(lang=lang)
        execute(push_underscore)


@task
@needs(
    'stanfordi18n_extract_theme',
    'stanfordi18n_extract_platform',
    'stanfordi18n_transifex_push',
)
def stanfordi18n_robot_push():
    """
    Extract source strings and push to Transifex
    """
    print('Pushed updated source strings to Transifex')


@task
def stanfordi18n_robot_pull():
    """
    Pull translations from Transifex, generate po and mo files
    """
    langs = CONFIG.translated_locales
    for lang in langs:
        pull_cmd = 'tx pull -l {lang} -r "stanford-openedx.*"'.format(lang=lang)
        execute(pull_cmd)
        fix_privacy_cmd = 'sed -i "/python-format/d" conf/locale/{lang}/LC_MESSAGES/privacy.po'.format(lang=lang)
        sh(fix_privacy_cmd)
    print('Pulled all files')

    # generate merged theme django.po
    sh('i18n_tool generate -c conf/locale/stanford_config.yaml -v 1')

    theme_dir = get_theme_dir()
    for lang in langs:
        theme_messages_dir = theme_dir / 'conf/locale/{lang}/LC_MESSAGES'.format(lang=lang)
        theme_messages_dir.makedirs_p()
        shutil.move(CONFIG.get_messages_dir(lang) / 'theme.po', theme_messages_dir / 'django.po')
        shutil.move(CONFIG.get_messages_dir(lang) / 'theme.mo', theme_messages_dir / 'django.mo')
        # Generate static i18n JS files.
        sh(django_cmd('lms', 'devstack', 'compilejsi18n', '-l', lang))

    sh('git add conf/locale')
    sh('git add lms/static/js/i18n')
    sp.check_call('git add conf/locale', cwd=theme_dir, shell=True)
    print('Check updated translations files in platform and theme before committing')

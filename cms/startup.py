"""
Module with code executed during Studio startup
"""

from django.conf import settings

# Force settings to run so that the python path is modified

settings.INSTALLED_APPS  # pylint: disable=pointless-statement

from openedx.core.lib.django_startup import add_mimetypes
from openedx.core.lib.django_startup import autostartup
import django
from openedx.core.djangoapps.monkey_patch import (
    third_party_auth,
    django_db_models_options
)
from openedx.core.lib.xblock_utils import xblock_local_resource_url

import xmodule.x_module
import cms.lib.xblock.runtime

from startup_configurations.validate_config import validate_cms_config
from openedx.core.djangoapps.theming.core import enable_theming
from openedx.core.djangoapps.theming.helpers import is_comprehensive_theming_enabled


def run():
    """
    Executed during django startup
    """
    third_party_auth.patch()
    django_db_models_options.patch()

    # Comprehensive theming needs to be set up before django startup,
    # because modifying django template paths after startup has no effect.
    if is_comprehensive_theming_enabled():
        enable_theming()

    django.setup()

    autostartup()

    add_mimetypes()

    # In order to allow descriptors to use a handler url, we need to
    # monkey-patch the x_module library.
    # TODO: Remove this code when Runtimes are no longer created by modulestores
    # https://openedx.atlassian.net/wiki/display/PLAT/Convert+from+Storage-centric+runtimes+to+Application-centric+runtimes
    xmodule.x_module.descriptor_global_handler_url = cms.lib.xblock.runtime.handler_url
    xmodule.x_module.descriptor_global_local_resource_url = xblock_local_resource_url

    # validate configurations on startup
    validate_cms_config(settings)

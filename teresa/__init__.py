import gettext
import sys
import locale


_usr_share_locale = sys.prefix + '/share/locale'

_locale_dirs = gettext.find('teresa', _usr_share_locale)


_locale_lang = gettext.translation("teresa",
                                   _usr_share_locale if _locale_dirs else 'teresa/locale',
                                   languages=[locale.getlocale()[0] or 'en_US'],
                                   fallback=True)

_locale_lang.install(True)

translate = _locale_lang.gettext

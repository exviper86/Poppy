# language_handler.py

import subprocess
import ctypes
user32 = ctypes.windll.user32

class LanguageHandler():
    def get_layout_id(self):
        def get_window_class(hwnd):
            try:
                buf = ctypes.create_unicode_buffer(256)
                user32.GetClassNameW(hwnd, buf, 256)
                return buf.value
            except:
                return "<error>"
        
        hwnd = user32.GetForegroundWindow()
        if hwnd == 0:
            return self._get_layout_alt()
        
        window_class = get_window_class(hwnd)
        #print(window_class)
        if window_class in self._exception_windows:
            return self._get_layout_alt()
        
        thread_id = user32.GetWindowThreadProcessId(hwnd, None)
        layout_id = user32.GetKeyboardLayout(thread_id)

        return layout_id & 0xFFFF
    
    def get_name(self, lang_id):
        return self._lang_names.get(lang_id, "Unknown")
    
    def get_code(self, lang_id):
        return self._lang_native_codes.get(lang_id, "--")
    
    def _get_layout_alt(self):
        try:
            cmd = [
                "powershell", "-Command",
                """Add-Type -AssemblyName System.Windows.Forms; 
                [System.Windows.Forms.InputLanguage]::CurrentInputLanguage.Culture.LCID"""
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=0.5, creationflags=subprocess.CREATE_NO_WINDOW)
            if result.returncode == 0:
                return int(result.stdout.strip())
            return None
        except Exception as e:
            print(f"[LanguageHandler] Ошибка при получении раскладки: {e}")
            return None
    
    _exception_windows = ["Notepad", "ApplicationFrameWindow", "XamlExplorerHostIslandWindow"]

    _lang_names = {
        # Европейские языки
        0x0409: 'English',
        0x0809: 'English (UK)',
        0x0419: 'Русский',
        0x0407: 'Deutsch',
        0x040C: 'Français',
        0x040A: 'Español',
        0x0410: 'Italiano',
        0x0816: 'Português',
        0x0416: 'Português (PT)',
        0x0413: 'Nederlands',
        0x0415: 'Polski',
        0x041D: 'Svenska',
        0x0406: 'Dansk',
        0x0414: 'Norsk',
        0x040B: 'Suomi',
        0x0405: 'Čeština',
        0x041B: 'Slovenčina',
        0x040E: 'Magyar',
        0x0418: 'Română',
        0x0402: 'Български',
        0x0408: 'Ελληνικά',
        0x0422: 'Українська',
        0x041F: 'Türkçe',
        0x041A: 'Hrvatski',
        0x0C1A: 'Srpski',
        0x081A: 'Српски',
        0x0424: 'Slovenščina',
        0x0425: 'Eesti',
        0x0426: 'Latviešu',
        0x0427: 'Lietuvių',

        # Азиатские языки
        0x0804: '中文',
        0x0404: '中文 (繁體)',
        0x0411: '日本語',
        0x0412: '한국어',
        0x041E: 'ไทย',
        0x042A: 'Tiếng Việt',
        0x0421: 'Bahasa Indonesia',
        0x043E: 'Bahasa Melayu',
        0x0439: 'हिन्दी',
        0x0445: 'বাংলা',
        0x0449: 'தமிழ்',
        0x044A: 'తెలుగు',
        0x044E: 'मराठी',
        0x0420: 'اردو',
        0x0429: 'فارسی',
        0x0401: 'العربية',
        0x040D: 'עברית',

        # Другие
        0x0403: 'Català',
        0x0456: 'Galego',
        0x042D: 'Euskara',
        0x040F: 'Íslenska',
        0x083C: 'Gaeilge',
        0x0452: 'Cymraeg',
        0x043A: 'Malti',
        0x0441: 'Kiswahili',
        0x0436: 'Afrikaans',
        0x045E: 'አማርኛ',
        0x0437: 'ქართული',
        0x042B: 'Հայերեն',
        0x042C: 'Azərbaycanca',
        0x043F: 'Қазақ тілі',
        0x0443: 'Oʻzbekcha',
        0x0450: 'Монгол',
        0x0461: 'नेपाली',
        0x045B: 'සිංහල',
        0x0453: 'ភាសាខ្មែរ',
        0x0454: 'ລາວ',
        0x0455: 'မြန်မာ',
    }

    _lang_codes = {
        # Европейские языки
        0x0409: 'EN',  # English (US)
        0x0809: 'EN',  # English (UK)
        0x0419: 'RU',  # Русский
        0x0407: 'DE',  # Deutsch
        0x040C: 'FR',  # Français
        0x040A: 'ES',  # Español
        0x0410: 'IT',  # Italiano
        0x0816: 'PT',  # Português (BR)
        0x0416: 'PT',  # Português (PT)
        0x0413: 'NL',  # Nederlands
        0x0415: 'PL',  # Polski
        0x041D: 'SV',  # Svenska
        0x0406: 'DA',  # Dansk
        0x0414: 'NO',  # Norsk (обычно 'nb', но 'no' допустимо)
        0x040B: 'FI',  # Suomi
        0x0405: 'CS',  # Čeština
        0x041B: 'SK',  # Slovenčina
        0x040E: 'HU',  # Magyar
        0x0418: 'RO',  # Română
        0x0402: 'BG',  # Български
        0x0408: 'EL',  # Ελληνικά
        0x0422: 'UK',  # Українська
        0x041F: 'TR',  # Türkçe
        0x041A: 'HR',  # Hrvatski
        0x0C1A: 'SR',  # Srpski (Latin)
        0x081A: 'SR',  # Српски (Cyrillic) — ISO код один
        0x0424: 'SL',  # Slovenščina
        0x0425: 'ET',  # Eesti
        0x0426: 'LV',  # Latviešu
        0x0427: 'LT',  # Lietuvių

        # Азиатские языки
        0x0804: 'ZH',  # 中文 (упрощённый)
        0x0404: 'ZH',  # 中文 (традиционный)
        0x0411: 'JA',  # 日本語
        0x0412: 'KO',  # 한국어
        0x041E: 'TH',  # ไทย
        0x042A: 'VI',  # Tiếng Việt
        0x0421: 'ID',  # Bahasa Indonesia
        0x043E: 'MS',  # Bahasa Melayu
        0x0439: 'HI',  # हिन्दी
        0x0445: 'BN',  # বাংলা
        0x0449: 'TA',  # தமிழ்
        0x044A: 'TE',  # తెలుగు
        0x044E: 'MR',  # मराठी
        0x0420: 'UR',  # اردو
        0x0429: 'FA',  # فارسی
        0x0401: 'AR',  # العربية
        0x040D: 'HE',  # עברית

        # Другие
        0x0403: 'CA',  # Català
        0x0456: 'GL',  # Galego
        0x042D: 'EU',  # Euskara
        0x040F: 'IS',  # Íslenska
        0x083C: 'GA',  # Gaeilge
        0x0452: 'CY',  # Cymraeg
        0x043A: 'MT',  # Malti
        0x0441: 'SW',  # Kiswahili
        0x0436: 'AF',  # Afrikaans
        0x045E: 'AM',  # አማርኛ
        0x0437: 'KA',  # ქართული
        0x042B: 'HY',  # Հայերեն
        0x042C: 'AZ',  # Azərbaycanca
        0x043F: 'KK',  # Қазақ тілі
        0x0443: 'UZ',  # Oʻzbekcha
        0x0450: 'MN',  # Монгол
        0x0461: 'NE',  # नेपाली
        0x045B: 'SI',  # සිංහල
        0x0453: 'KM',  # ភាសាខ្មែរ
        0x0454: 'LO',  # ລາວ
        0x0455: 'MY',  # မြန်မာ
    }

    _lang_native_codes = {
        # Европейские языки (латиница — ISO 639-2/T)
        0x0409: 'ENG',      # English (US)
        0x0809: 'ENG',      # English (UK)
        0x0407: 'DEU',      # Deutsch
        0x040C: 'FRA',      # Français
        0x040A: 'SPA',      # Español ← исправлено
        0x0410: 'ITA',      # Italiano
        0x0816: 'POR',      # Português (BR)
        0x0416: 'POR',      # Português (PT) ← унифицировано
        0x0413: 'NLD',      # Nederlands ← современный ISO (вместо NED)
        0x0415: 'POL',      # Polski
        0x041D: 'SWE',      # Svenska
        0x0406: 'DAN',      # Dansk
        0x0414: 'NOR',      # Norsk
        0x040B: 'FIN',      # Suomi
        0x0405: 'CES',      # Čeština
        0x041B: 'SLK',      # Slovenčina
        0x040E: 'HUN',      # Magyar
        0x0418: 'RON',      # Română
        0x0402: 'BUL',      # Български
        0x0408: 'ELL',      # Ελληνικά
        0x041F: 'TUR',      # Türkçe
        0x041A: 'HRV',      # Hrvatski
        0x0424: 'SLV',      # Slovenščina
        0x0425: 'EST',      # Eesti
        0x0426: 'LAV',      # Latviešu
        0x0427: 'LIT',      # Lietuvių
        0x0403: 'CAT',      # Català
        0x0456: 'GAL',      # Galego (допустимо; ISO: glg, но GAL — устоявшееся)
        0x042D: 'EUS',      # Euskara
        0x040F: 'ISL',      # Íslenska
        0x083C: 'GLE',      # Gaeilge ← исправлено (вместо GAE)
        0x0452: 'CYM',      # Cymraeg
        0x043A: 'MLT',      # Malti
        0x0436: 'AFR',      # Afrikaans
        0x0441: 'SWA',      # Kiswahili

        # Европейские языки (кириллица — родное сокращение для UI)
        0x0419: 'РУС',      # Русский
        0x0422: 'УКР',      # Українська
        0x0C1A: 'SRP',      # Srpski (lat)
        0x081A: 'СРП',      # Српски (cyr)

        # Азиатские и другие языки (родное письмо — для узнаваемости)
        0x0804: '中文',      # Упрощённый китайский
        0x0404: '繁體',      # Традиционный китайский
        0x0411: '日本語',    # Японский
        0x0412: '한국어',    # Корейский
        0x041E: 'ไทย',      # Тайский
        0x042A: 'VIỆT',     # Tiếng Việt
        0x0421: 'IND',      # Bahasa Indonesia
        0x043E: 'MSA',      # Bahasa Melayu
        0x0439: 'हिं',      # हिन्दी
        0x0445: 'বাং',      # বাংলা
        0x0449: 'தமி',     # தமிழ்
        0x044A: 'తెలు',    # తెలుగు
        0x044E: 'मरा',     # मराठी
        0x0420: 'اردو',     # Урду
        0x0429: 'فارس',    # فارسی
        0x0401: 'عرب',     # العربية
        0x040D: 'עברית',    # Иврит

        # Другие языки (родное письмо или устоявшееся сокращение)
        0x045E: 'አማ',      # አማርኛ
        0x0437: 'ქარ',      # ქართული
        0x042B: 'ՀԱՅ',      # Հայերեն
        0x042C: 'АЗӘ',      # Azərbaycanca
        0x043F: 'ҚАЗ',      # Қазақ тілі
        0x0443: 'ЎЗБ',      # Oʻzbekcha (кириллическая форма для узнаваемости)
        0x0450: 'МОН',      # Монгол
        0x0461: 'नेपा',     # नेपाली
        0x045B: 'සිං',      # සිංහල
        0x0453: 'ខ្មែ',     # ភាសាខ្មែរ
        0x0454: 'ລາວ',     # ລາວ
        0x0455: 'မြန်',     # မြန်မာ
    }
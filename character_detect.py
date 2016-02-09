
# 平仮名
hiragana = \
    'ぁあぃいぅうぇえぉおかがきぎく'\
    'ぐけげこごさざしじすずせぜそぞた'\
    'だちぢっつづてでとどなにぬねのは'\
    'ばぱひびぴふぶぷへべぺほぼぽまみ'\
    'むめもゃやゅゆょよらりるれろゎわ'\
    'ゐゑをんゔゕゖ゙゚゛゜ゝゞゟ'

# 片仮名
katakana = \
    '゠ァアィイゥウェエォオカガキギク'\
    'グケゲコゴサザシジスズセゼソゾタ'\
    'ダチヂッツヅテデトドナニヌネノハ'\
    'バパヒビピフブプヘベペホボポマミ'\
    'ムメモャヤュユョヨラリルレロヮワ'\
    'ヰヱヲンヴヵヶヷヸヹヺ・ーヽヾヿ'\


katakana_ext = 'ㇰㇱㇲㇳㇴㇵㇶㇷㇸㇹㇺㇻㇼㇽㇾㇿ'

japanese_chars = hiragana + katakana + katakana_ext

korean_chars = \
    'ㅏㅑㅓㅕㅗㅛㅜㅠㅡㅣㅐㅔㅒㅖㅘㅙㅚㅢㅝㅞㅟ'\
    'ㄱ가갸거겨고교구규그기개게걔계과괘괴긔궈궤귀'\
    'ㄴ나냐너녀노뇨누뉴느니내네냬녜놔놰뇌늬눠눼뉘'\
    'ㄷ다댜더뎌도됴두듀드디대데댸뎨돠돼되듸둬뒈뒤'\
    'ㄹ라랴러려로료루류르리래레럐례롸뢔뢰릐뤄뤠뤼'\
    'ㅁ마먀머며모묘무뮤므미매메먜몌뫄뫠뫼믜뭐뭬뮈'\
    'ㅂ바뱌버벼보뵤부뷰브비배베뱨볘봐봬뵈븨붜붸뷔'\
    'ㅅ사샤서셔소쇼수슈스시새세섀셰솨쇄쇠싀숴쉐쉬'\
    'ㅇ아야어여오요우유으이애에얘예와왜외의워웨위'\
    'ㅈ자쟈저져조죠주쥬즈지재제쟤졔좌좨죄즤줘줴쥐'\
    'ㅊ차챠처쳐초쵸추츄츠치채체챼쳬촤쵀최츼춰췌취'\
    'ㅋ카캬커켜코쿄쿠큐크키캐케컈켸콰쾌쾨킈쿼퀘퀴'\
    'ㅌ타탸터텨토툐투튜트티태테턔톄톼퇘퇴틔퉈퉤튀'\
    'ㅍ파퍄퍼펴포표푸퓨프피패페퍠폐퐈퐤푀픠풔풰퓌'\
    'ㅎ하햐허혀호효후휴흐히해헤햬혜화홰회희훠훼휘'\
    'ㄲ까꺄꺼껴꼬꾜꾸뀨끄끼깨께꺠꼐꽈꽤꾀끠꿔꿰뀌'\
    'ㄸ따땨떠뗘또뚀뚜뜌뜨띠때떼떄뗴똬뙈뙤띄뚸뛔뛰'\
    'ㅃ빠뺘뻐뼈뽀뾰뿌쀼쁘삐빼뻬뺴뼤뽜뽸뾔쁴뿨쀄쀠'\
    'ㅆ싸쌰써쎠쏘쑈쑤쓔쓰씨쌔쎄썌쎼쏴쐐쐬씌쒀쒜쒸'\
    'ㅉ짜쨔쩌쪄쪼쬬쭈쮸쯔찌째쩨쨰쪠쫘쫴쬐쯰쭤쮀쮜'


def chars_detect(text):
    j = 0
    k = 0
    unknown = 0
    for char in text:
        if char in japanese_chars:
            j += 1
        elif char in korean_chars:
            k += 1
        else:
            unknown += 1

    if j >= k > 0:
        return 'ja'
    elif k >= j > 0:
        return 'ko'
    else:
        return None


def has_ja_char(text):
    return len(set(text) & set(japanese_chars))


def has_ko_char(text):
    return len(set(text) & set(korean_chars))


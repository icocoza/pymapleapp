UNIT_NUMBER = {
    'WP000': 0, # 배터리
    'WP001': 1, # 온도
    'WP002': 2, # 습도
    'WP003': 3, # 기압
    'WP004': 4, # 풍향
    'WP005': 5, # 풍속
    'WP006': 6, # 강우량
    'WP007': 7, # PM10
    'WP008': 8, # PM2.5
    'WP009': 9, # CO
    'WP010': 10, # NO2
    'WP011': 11, # SO2
    'WP012': 12, # O3
    'WP013': 13, # 토양온도
    'WP014': 14, # 토양습도
    'WP015': 15, # 토양E/C
    'WP016': 16, # 진동(평균)
    'WP017': 17, # 진동(min)
    'WP018': 18, # 진동(max)
    'WP019': 19, # 진동(표준편차)
    'WP020': 20, # 전류(R)
    'WP021': 21, # 전류(S)
    'WP022': 22, # 전류(T)
    'WP023': 23, # PM1.0
    'WP024': 24, # 수위
    'WP025': 25, # 배터리 잔량
    'WP026': 26, # 암모니아
    'WP027': 27, # 폼알데하이드
    'WP028': 28, # CO2
    'WP031': 29, # VOC(유기화합물)
    'WP030': 30, # CO2
    'WP031': 31, #	VOC
    'WP032': 32, #	Leq
    'WP033': 33, #	Lmax
    'WP034': 34, #	L10
    'WP035': 35, #	총먼지
    'WP036': 36, #	유량
    'WP037': 37, #	Frequency X
    'WP038': 38, #	Frequency Y
    'WP039': 39, #	Frequency Z
    'WP040': 40, #	Velocity RMS X
    'WP041': 41, #	Velocity RMS Y
    'WP042': 42, #	Velocity RMS Z
    'WP043': 43, #	Acceleration RMS X
    'WP044': 44, #	Acceleration RMS Y
    'WP045': 45, #	Acceleration RMS Z
    'WP046': 46, #	Acceleration Peak X
    'WP047': 47, #	Acceleration Peak Y
    'WP048': 48, #	Acceleration Peak Z
    'WP049': 49, #	Displacement X
    'WP050': 50, #	Displacement Y
    'WP051': 51, #	Displacement Z
    'WP052': 52, #	Crest Factor X
    'WP053': 53, #	Crest Factor Y
    'WP054': 54, #	Crest Factor Z
    'WP055': 55, #	Duty Cycle
    'WP056': 56, #	g-force X
    'WP057': 57, #	g-force Y
    'WP058': 58, #	g-force Z
    'WP059': 59, #	Pitch
    'WP060': 60, #	Roll
    'WP061': 61, #	Motion

    'WX190': 190, # 조도
    'WX191': 191, # 자력 X
    'WX192': 192, # 자력 Y
    'WX193': 193, # 자력 Z
}

def getUnitNumber(unit):
    if unit in UNIT_NUMBER:
        return UNIT_NUMBER[unit]
    return unit
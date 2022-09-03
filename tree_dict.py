tree_dict = {
    'Allowed':[
        'FieldUniform',
        'Generals',
        'Other',
        'PolarUniform',
        'Sv',
        'SvUniform',
        'Vdv',
        'VdvUniform',
        'Vks',
        'VksUniform',
        'Vmf',
        'VmfUniform',
        'Atributes'
        ],
    'NotAllowed':[
        'FieldUniform',
        'Generals',
        'Other',
        'PolarUniform',
        'Sv',
        'SvUniform',
        'Vdv',
        'VdvUniform',
        'Vks',
        'VksUniform',
        'Vmf',
        'VmfUniform',
        ], 
    'Vehicles':[
        'Aviation',
        'Engine',
        'Navy',
        ],
    'Civil':[
        ],
    'Delete':[

        ],
}
translate_dict = {
    'Allowed':'Не нарушение 76ФЗ',
    'Civil':'Гражданский',
    'NotAllowed':'Нарушение 76ФЗ',
    'Vehicles':'Военная техника',
    'FieldUniform':'Полевая форма',
    'Generals':'Генерал',
    'Other':'Другое',
    'PolarUniform':'Полярная форма',
    'Sv':'СВ',
    'SvUniform':'Форма СВ',
    'Vdv':'ВДВ',
    'VdvUniform':'Форма ВДВ',
    'Vks':'ВКС',
    'VksUniform':'Форма ВКС',
    'Vmf':'ВМФ',
    'VmfUniform':'Форма ВМФ',
    'Delete':'Удалить',
    'Aviation':'Авиационная техника',
    'Engine':'Сухопутная техника',
    'Navy':'Морская техника',
    'Atributes':'Военная атрибутика',
}
def get_translate(eng):
    return translate_dict[eng]
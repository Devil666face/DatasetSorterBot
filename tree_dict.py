tree_dict = {
    'Allowed':[
        'FieldUniform',
        'Generals',
        'Other',
        'PolarUniform',
        'SvOffice',
        'SvUniform',
        'VdvOffice',
        'VdvUniform',
        'VksOffice',
        'VksUniform',
        'VmfOffice',
        'VmfUniform',
        'Atributes'
        ],
    'NotAllowed':[
        'FieldUniform',
        'Generals',
        'Other',
        'PolarUniform',
        'SvOffice',
        'SvUniform',
        'VdvOffice',
        'VdvUniform',
        'VksOffice',
        'VksUniform',
        'VmfOffice',
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
    'SvOffice':'Офисная СВ',
    'SvUniform':'Парадная СВ',
    'VdvOffice':'Офисная ВДВ',
    'VdvUniform':'Парадная ВДВ',
    'VksOffice':'Офисная ВКС',
    'VksUniform':'Парадная ВКС',
    'VmfOffice':'Офисная ВМФ',
    'VmfUniform':'Парадная ВМФ',
    'Delete':'Удалить',
    'Aviation':'Авиационная техника',
    'Engine':'Сухопутная техника',
    'Navy':'Морская техника',
    'Atributes':'Военная атрибутика',
}
def get_translate(eng):
    return translate_dict[eng]
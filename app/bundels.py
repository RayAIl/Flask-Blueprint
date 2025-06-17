import os

from flask_assets import Bundle, Environment
from .functions import recursive_filt_iter


def get_bundle(route, tpl, ext, paths, type=False):
    """
    Функция возвращает нужный Bundle (css/js) для регистрации в главном файле приложения. 
    
        Содержит пути до локальных исходников css/js файлов, сгрупированных друг с другом
            по использованию в шаблонах html.
    ######################################################################################

    route - название роута
    tpl - название шаблона html из каталога "templates"
    ext - расширение "css/js"
    paths (массив) - все пути к исходникам 
    
        type (опциональный) - используется только для js.
            (
            [INFO]: Если нужен главный файл "main.js", параметр не указывать!
                    Если нужен скрипт длительной загрузки "defer.js", передать булево значение True.
            )
    ######################################################################################
    """
    if route and tpl and ext:
        return {
            'instance': Bundle(*paths, output=get_path(route, tpl, ext, type), filters=get_filter(ext)),
            'name': get_filename(route, tpl, ext, type),
            'dir': os.getcwd()
        }

def register_bundle(assets, bundle):
    assets.register(bundle['name'], bundle['instance'])
    return f"[INFO]: Bundle {bundle['name']} успешно зарегистрирован!"

def register_bundles(assets, bundles):
    for x in recursive_filt_iter(bundles):
        for bundles in x:
            register_bundle(assets, bundles)

def get_filename(route, tpl, ext, type):
    if type:
        return f"{route} {tpl} {ext}"
    else:
        return f"{route} {tpl} {ext}"

def get_path(route, tpl, ext, type):
    if type:
        return f"/{route}/{tpl}/{ext}"
    else:
        return f"/{route}/{tpl}/{ext}"

def get_filter(ext):
    if ext.upper() == 'CSS':
        return 'cssmin' 
    elif ext.upper() == 'JS':
        return 'jsmin'   
    else:
        return None

bundles = {
    "post": {
        "all": {
            "CSS": [
                get_bundle('post', 'all', 'CSS', ['CSS/blocks/table.css', 'CSS/libs/bootstrap.min.css'])
            ],
            
            "js": [
                get_bundle('post', 'all', 'JS', ['js/app.js'])
                
                ],
        },

        "create": {},
        "update": {},
    },
    "user": {
        "login": {},
        "register": {},
    },
}
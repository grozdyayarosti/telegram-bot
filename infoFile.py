# Объект, который будет хранить в себе информацию о записи пользователя
info = {
    "name": "",
    "style": "",
    "phone": ""
}

# Функция которая читает файл и возвращает подробную информацию о стиле под соответствующим ключом, который передали в параметр
def getInfoStyle(style):
    a = {}
    # Смысловые абзацы разделены символом * в файле stylesInfo.txt
    with open("stylesInfo.txt", "r", encoding="utf8") as file:
        content = file.read().split("*")
        a['VOGUE'] = content[0]
        a['K-POP'] = content[1]
        a['HIP-HOP'] = content[2]
        a['JAZZ-FUNK'] = content[3]
        a['HIGH-HEELS'] = content[4]
    return a[style]
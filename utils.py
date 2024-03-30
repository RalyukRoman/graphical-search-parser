def redact_parse(dict_parse: list[dict]) -> list:
    list_parse_redact: list = []
    for i in dict_parse:
        for k in ['link', 'title', 'description']:
            if k == 'title':
                list_parse_redact.append(str(i[k]) + ' ---> ' + str(i['name']))
            elif k == 'link':
                list_parse_redact.append(str(i[k]) + '\n')
            else:
                list_parse_redact.append(str(i[k]))
        list_parse_redact.append('\n-----------------------\n')
    return list_parse_redact
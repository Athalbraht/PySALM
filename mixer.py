def auto_register(comm, tab, typedef, bool_tab : list = [], bool_tab2=[]):
    describ = []
    bools = []
    bools2 = []
    multi = []
    register = []
    if isinstance(tab, dict):
        pass
    if isinstance(tab, list):
        for i, question in enumerate(tab):
            register.append(comm.register('static', 'desc', '\\newpage'))
            if question in bool_tab:
                bools.append(question)
            elif question in bool_tab2:
                bools2.append(question)
            elif question in typedef["m"]:
                register.append(
                    comm.register('gen', 'expandtable', question, alias=question, mode='reload'),
                )
            elif question in typedef["q"]:
                describ.append(question)

            else:
                register.append(
                    comm.register('gen', 'counttable', question, alias=question, mode='reload'),
                )
        if describ:
            register = [
                comm.register('static', 'desc', '\\newpage'),
                comm.register('gen', 'desctable', describ, alias=describ[0] + 'DESC', mode='reload')
            ] + register
        if bools:
            register = [

                comm.register('static', 'desc', '\\newpage'),
                comm.register('gen', 'counttable', bools, alias=bools[0], mode='reload')] + register
        if bools2:
            register = [
                comm.register('static', 'desc', '\\newpage'),
                comm.register('gen', 'counttable', bools2, alias=bools[0], mode='reload')] + register
        return register


def register_characteristic(df, cols):
    pass

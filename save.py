from io import open

def load_save(filename):
    save0 = open('saves/save0.txt', 'r')
    save1 = open('saves/save1.txt', 'r')
    save2 = open('saves/save2.txt', 'r')
    save3 = open('saves/save3.txt', 'r')
    save4 = open('saves/save4.txt', 'r')
    if filename == 'save0.txt':
        return save0.readline(0), save0.readline(1), save0.readline(2), save0.readline(3), save0.readline(4)
    elif filename == 'save1.txt':
        return save1.readline(0), save1.readline(1), save1.readline(2), save1.readline(3), save1.readline(4)
    elif filename == 'save2.txt':
        return save2.readline(0), save2.readline(1), save2.readline(2), save2.readline(3), save2.readline(4)
    elif filename == 'save3.txt':
        return save3.readline(0), save3.readline(1), save3.readline(2), save3.readline(3), save3.readline(4)
    elif filename == 'save4.txt':
        return save4.readline(0), save4.readline(1), save4.readline(2), save4.readline(3), save4.readline(4)
def write_save(filename, line1, line2, line3, line4, line5):
    save0 = open('saves/save0.txt', 'w')
    save1 = open('saves/save1.txt', 'w')
    save2 = open('saves/save2.txt', 'w')
    save3 = open('saves/save3.txt', 'w')
    save4 = open('saves/save4.txt', 'w')
    if filename == 'save0.txt':
        save0.writelines([line1, line2, line3, line4, line5])
    if filename == 'save1.txt':
        save1.writelines([line1, line2, line3, line4, line5])
    if filename == 'save2.txt':
        save2.writelines([line1, line2, line3, line4, line5])
    if filename == 'save3.txt':
        save3.writelines([line1, line2, line3, line4, line5])
    if filename == 'save4.txt':
        save4.writelines([line1, line2, line3, line4, line5])    
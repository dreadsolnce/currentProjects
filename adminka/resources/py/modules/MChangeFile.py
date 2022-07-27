#!/usr/bin/python3
import os
import subprocess

fileTemp = "/tmp/file.tmp"  # Временный файл


# Запуск терминальной команды с выводом: кода выхода, выходных данных, описания ошибки
def runProcess(command=None):
    if command:
        process = subprocess.Popen(command,
                                   shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        return process.returncode, stdout.decode("utf-8"), stderr.decode("utf-8")
    else:
        print("Ошибка параметра при запросе функции!")


# Копирование обрабатываемого файла во временную папку, для его обработки
def copyFileToTmp(file=None):
    # Копируем файл во временную папку, во избежание возникновения ошибки Permission Denied
    command = "sudo cp {} {} ; sudo chmod 644 {}".format(file, fileTemp, fileTemp)
    return_code, stdout, stderr = runProcess(command)
    return return_code, stdout, stderr


# Класс обработки файлов
class FileProcess(object):
    def __init__(self, file=None):
        super().__init__()
        self.file = file  # Обрабатываемый файл

    # Функция, определяющая заканчивается ли файл пустой строкой:
    # 0 - не пустая, 1 - пустая, 2 - пустая (символ перевода от последней строки)
    def __emptyLine(self):
        try:
            with open(self.file, "r") as f:
                last_line = f.readlines()[-1]
                if len(last_line) > 1 and last_line[-1].encode("utf-8") == b'\n':
                    return 2
                if len(last_line) == 1 and last_line[-1].encode("utf-8") == b'\n':
                    return 1
                if len(last_line) > 1 and last_line[-1].encode("utf-8") != b'\n':
                    return 0
        except (PermissionError, FileNotFoundError) as e:
            print("Ошибка в функции emptyLine: " + str(e))

    # Функция поиска строки в файле: 0 - найдена, 1 - отсутствует
    def findString(self, template):
        try:
            with open(self.file, 'r') as f:
                for line in f:
                    if " ".join(line.split()) == " ".join(template.split()):
                        print("Файл {} содержит искомую строку!".format(self.file))
                        return 0
            print("В файле {} не найдена строка!".format(self.file))
            return 1
        except (PermissionError, FileNotFoundError) as e:
            print("Ошибка в функции findString: " + str(e))

    # Функция создания копии файла с именем *.PNOSKO.bak: True - успех выполнения функции, False - ошибка выполнения функции
    def createPNOSKOBakFile(self):
        file_bak = self.file + ".PNOSKO.bak"
        if os.path.isfile(self.file):
            if not os.path.isfile(file_bak):
                command = "sudo cp -R {} {}.PNOSKO.bak".format(self.file, self.file)
                out_data = runProcess(command)
                if out_data[0] == 0:
                    print("Копия файла {} успешно создана!".format(self.file))
                    return True
                else:
                    print("Ошибка при создании копии файла: {}".format(out_data[2]))
                    return False
            elif os.path.isfile(file_bak):
                print("Копия файла {} уже создана".format(self.file))
                return True
        else:
            print("Ошибка в функции createPNOSKOBakFile: файл {} не найден!".format(self.file))
            return False

    # Функция добавления строки в конец файла
    def addStringEndFile(self, addstr=None):
        copyFileToTmp(self.file)
        count = 0
        count_clear_line = 0
        try:
            with open(fileTemp, "w") as ft:
                f = open(self.file, "r")
                while True:
                    line = f.readline()
                    if len(line) > 0:
                        if len(line) > 1:
                            for j in range(count_clear_line):
                                ft.writelines("\n")
                            ft.writelines(line)
                            count = 0
                            count_clear_line = 0
                        elif len(line) == 1 and count == 0:
                            ft.writelines(line)
                            count = 1
                        else:
                            count_clear_line += 1
                    if not line:
                        break
                f.close()

            state = self.__emptyLine()
            with open(fileTemp, "a") as f:
                if state == 0:
                    txt = "\n\n" + addstr + "\n"
                elif state == 1:
                    txt = addstr + "\n"
                elif state == 2:
                    txt = "\n" + addstr + "\n"
                f.writelines(txt)

            command = "sudo mv -f {} {}".format(fileTemp, self.file)
            out_data = runProcess(command)
            return out_data[0]

        except (PermissionError, FileNotFoundError) as e:
            print("Ошибка в функции emptyLine: " + str(e))


if __name__ == '__main__':
    fp = FileProcess("/etc/sudoers")


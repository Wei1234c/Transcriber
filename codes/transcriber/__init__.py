from datetime import datetime



class Script:
    TIME_FORMAT = '%H:%M:%S.%f'


    def __init__(self, idx, t_start, t_end, text):
        self.idx = idx
        self.t_start = t_start
        self.t_end = t_end
        self.text = text


    @property
    def boundle(self):
        return [self.idx, self.t_start, self.t_end, self.text]


    def __str__(self):
        return str(self.boundle)


    @property
    def start_time(self):
        return datetime.strptime(self.t_start, self.TIME_FORMAT)


    @property
    def end_time(self):
        return datetime.strptime(self.t_end, self.TIME_FORMAT)


    def merge(self, script):
        return Script(self.idx,
                      self.t_start,
                      script.t_end,
                      self.text + ' ' + script.text)



class SRT:

    def __init__(self, file_path = None):
        self.scripts = []

        if file_path is not None:
            self.load(file_path)


    def sort(self):
        self.scripts = sorted(self.scripts, key = lambda script: script[1])


    def reindex(self):
        self.sort()

        for i in range(len(self.scripts)):
            self.scripts[i][0] = i + 1


    def get_script(self, idx, pop = False) -> Script:
        for i in range(len(self.scripts)):
            fields = self.scripts[i]

            if fields[0] == idx:
                script = Script(*fields)

                if pop:
                    self.scripts.pop(i)

                return script


    def set_script(self, script):
        for i in range(len(self.scripts)):
            if self.scripts[i][0] == script.idx:
                self.scripts[i] = script.boundle


    def set_text(self, idx, text):
        script = self.get_script(idx)
        script.text = text
        self.set_script(script)
        return script


    def merge(self, *indice):
        indice = sorted(indice)
        idx_0 = indice[0]

        for idx in indice[1:]:
            self.merge_two_scripts(idx_0, idx)

        return self.get_script(idx_0)


    def merge_two_scripts(self, idx_0, idx_1):
        idx_0, idx_1 = sorted((idx_0, idx_1))

        script_0 = self.get_script(idx_0)
        script_1 = self.get_script(idx_1, pop = True)
        assert script_0.start_time < script_1.start_time

        script = script_0.merge(script_1)
        self.set_script(script)

        return script


    @property
    def text(self):
        return '\n'.join(fields[3] for fields in self.scripts)


    def dumps(self):
        self.reindex()
        lines = [f'{script[0]}\n{script[1]} --> {script[2]}\n{script[3]}\n' for script in self.scripts]

        return '\n'.join(lines)


    def dump(self, file_name, encoding = 'utf-8'):
        lines = self.dumps()

        with open(file_name, 'wt', encoding = encoding) as f:
            f.writelines(lines)

        return lines


    def loads(self, str_scripts, line_sep = '\n'):
        str_scripts = str_scripts.strip()
        str_scripts = str_scripts.replace(',', '.').replace(line_sep, ',').replace('-->', ',').replace(',,', line_sep)
        lines = str_scripts.split(line_sep)

        for line in lines:
            fields = line.split(',')
            self.scripts.append([int(fields[0]),
                                 fields[1].strip(),
                                 fields[2].strip(),
                                 fields[3].strip()])
        return self


    def load(self, file_path, encoding = 'utf-8'):
        with open(file_path, 'rt', encoding = encoding) as f:
            lines = f.readlines()

        return self.loads(''.join(lines))

from enum import Enum


class NoteSign(Enum):
    """Ноты"""
    C = 1
    D = 2
    E = 3
    F = 4
    G = 5
    A = 6
    H = 7


class MusicalMood(Enum):
    """Лады"""
    minor = 1
    major = 2

"""Класс нотной тетради"""
class MelodyNote:
    """Инициализация нотной тетради"""
    def __init__(self, songs=None):
        if songs is None:
            songs = []
        self.songs = songs
        self.status = False

    def __lshift__(self, other):
        """Перегрузка <<"""
        if not self.status:
            raise Exception('The note is closed')
        self.songs.append(Song(other))
        return self

    def show_songs(self):
        """Вывод названий песен"""
        for i in self.songs:
            print(i.title)

    def __getitem__(self, i):
        """Взять элемент по индексу obj[i]"""
        if not self.status:
            raise Exception('The note is closed')
        return self.songs[i]

    def __iter__(self):
        self.status = True
        """Передача управления на итерацию по песне"""
        yield from iter(self.songs)
        self.status = False

    def __enter__(self):
        """Перегрузка enter метода менеджера контекста"""
        self.status = True
        return self

    def __exit__(self, exception_type, exception_val, trace):
        """Перегрузка exit метода  менеджера контекста"""
        self.status = False

"""Класс песни"""
class Song:
    """Инициализация песни"""
    def __init__(self, title, notes: list = None):
        if notes is None:
            notes = []
        self.notes = notes
        self.title = title

    def __lshift__(self, other: str):
        """Перегрузка <<"""
        self.notes.append(Note(NoteSign[other]))
        return self

    def play_song(self):
        """Проигрывание песни"""
        print('Start playing a song!')
        for i in self.notes:
            i.show_note()
        print()
        print('The song is not playing anymore.')

    def change_mood(self, mood: MusicalMood, start: int = 0, end: int = -1):
        """Смена настроя нот в диапазоне от start до end"""
        if end == -1:
            end = len(self.notes)

        for i in range(start, end):
            self.notes[i].change_note_mood(mood)

    def __getitem__(self, i):
        """Взять элемент по индексу obj[i]"""
        return self.notes[i]

    def __iter__(self):
        """Возвращаеим итератор

        for note in song:

            print(note) #Выводятся ноты из песни

            """
        return iter(self.notes)

    @property
    def mood_count(self):
        """Cчетчик мажорных нот"""
        return len(list(filter(lambda x: x.mood == 'major', self.notes)))

    def __lt__(self, other):
        """ Перегрузка < """
        return len(self.notes) < len(other.notes) or \
               (self.mood_count < other.mood_count and len(self.notes) == len(other.notes))

    def __gt__(self, other):
        """ Перегрузка > """
        return len(self.notes) > len(other.notes) or \
               (self.mood_count > other.mood_count and len(self.notes) == len(other.notes))

    def __eq__(self, other):
        """ Перегрузка == """
        return self.mood_count == other.mood_count and len(self.notes) == len(other.notes)

"""Класс ноты"""
class Note:
    """Инициализация ноты"""
    def __init__(self, sign, mood=MusicalMood.major):
        self.__sign = sign
        self.mood = mood

    @property
    def sign(self):
        """Защита перезаписи знака ноты"""
        return self.__sign

    def show_note(self):
        """Вывести ноту"""
        if self.mood == MusicalMood.major:
            print(self.sign.name, end=' ')
        else:
            print(self.sign.name.lower(), end=' ')

    def change_note_mood(self, mood: MusicalMood):
        """Меняем настрой ноты"""
        self.mood = mood

    def __gt__(self, other):
        """ Перегрузка > """
        return self.sign.value > other.sign.value or \
               (self.mood.value > other.mood.value and self.sign == other.sign)

    def __lt__(self, other):
        """ Перегрузка < """
        return self.sign.value < other.sign.value or \
               (self.mood.value < other.mood.value and self.sign == other.sign)

    def __eq__(self, other):
        """ Перегрузка == """
        return self.mood.value == other.mood.value and self.sign == other.sign


note1 = Note(NoteSign.C, MusicalMood.major)
note2 = Note(NoteSign.D, MusicalMood.major)
note3 = Note(NoteSign.E, MusicalMood.minor)
note4 = Note(NoteSign.F, MusicalMood.minor)
note5 = Note(NoteSign.G, MusicalMood.major)
note6 = Note(NoteSign.A, MusicalMood.minor)
note7 = Note(NoteSign.H, MusicalMood.major)

song1 = Song("FirstSong", [note2, note1, note6, note5, note5, note3, note4, note5, note1, note7, note5, note4, note1, note2, note1, note2, note2, note1, note6, note5, note6, note5, note5, note3])
song2 = Song("SecondSong", [note1, note1, note4, note7, note4, note5, note1, note2, note1, note4, note3, note2, note1, note4, note5, note6, note5, note1, note2, note1, note1, note2, note1, note4, note3, note2])
song3 = Song("TrirdSong", [note3, note6, note4, note2, note7, note1, note7, note5, note5, note4, note6, note7, note6, note5, note7, note4, note6, note7, note3, note6, note4, note2, note7])

my_melody_note = MelodyNote([song1, song2, song3])

with my_melody_note as note:
    note[1].play_song()

    print(my_melody_note[2][1].sign.name)
    my_melody_note.show_songs()

    my_melody_note << 'Song4'
    my_melody_note.show_songs()

    my_melody_note.songs[2].play_song()
    my_melody_note.songs[2].change_mood(MusicalMood.minor)
    my_melody_note.songs[2].play_song()

    print(note6 < note1)
    print(song1 > song2)
    my_melody_note[2] << 'C'
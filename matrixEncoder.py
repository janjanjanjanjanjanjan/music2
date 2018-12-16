"""takes pieces of music, deconstructs it into notes and creates a corresponding matrix"""
import glob
import pickle
import numpy
from music21 import converter, instrument, note, chord
#all played unique notes
uniqueNotes = []
#counters for number of appearances of uniquenotes
notesCount =[]
#all notes in order of appearance
notes = []
#the position keeper for the note in the
map={}

"""checks wether the note has already been seen, adds it into seen ones if its new"""
def appNotes(musicNote):
    isNew = True
    string = str(musicNote)
    for a, sign in enumerate(uniqueNotes):
        if sign == string:
            isNew = False
            notesCount[a]+=1
            break
    if(isNew):
        uniqueNotes.append(string)
        notesCount.append(1)

"""goes through every midi file in folder and fills a list of unique notes and a list of all the notes played in the file
also counts how many times a certain note is played"""
def parser():
    notes_to_parse = parse_files()
    for element in notes_to_parse: #takes every note and asks if its been seen already
            if isinstance(element, note.Note):
                notes.append(str(element.pitch))
                #print(str(element.pitch))
                appNotes(element.pitch)
            elif isinstance(element, chord.Chord):
                notes.append('.'.join(str(n) for n in element.normalOrder))

    print("length of notes:", len(notes))
    print("length of uniqueNotes:", len(uniqueNotes))
    counter = 0
    #printout because we can
    for c, obj in enumerate(uniqueNotes):
        print(uniqueNotes[c], "amount: ", notesCount[c])
        counter += notesCount[c]
    print("Sum:       ", counter)

"""creates a key-value pair, where the key is the String representation of the note and the value the index in the inputvector"""
def vector_builder():
    for increment, unique in enumerate(uniqueNotes):
        map[str(unique)] = increment
    print(map)

"""takes a note and returns its index"""
def getIndex(note):
    return map[str(note)]

"""takes a note and one-hot encodes it"""
def convert_note_into_vector(note):
    vector = []
    index = getIndex(note)
    for i in range(len(uniqueNotes)-1):
        if(index ==i):
            vector.append(1)
        else:
            vector.append(0)
    return vector


def encode_songs():
    vectorList = []
    notes_in_songs = parse_files()
    for element in notes_in_songs:
        vectorList.append(convert_note_into_vector(element))
    pickle.dump(vectorList,"matrix.txt")

def parse_files():
    notes_to_parse = None
    for file in glob.glob("source/*.mid"):
        midi = converter.parse(file)

        print("Parsing %s" % file)

        notes_to_parse = None
        try:  # file has instrument parts
            s2 = instrument.partitionByInstrument(midi)
            notes_to_parse = s2.parts[0].recurse()
            print(len(s2.parts))
            print("partitioned by instrument")
        except:  # file has notes in a flat structure
            notes_to_parse = midi.flat.notes
            print("flat notes")

    return []
    #return notes_to_parse

if __name__ == '__main__':
    #preparations
    parser()
   # vector_builder()
    #taking the midi tracks and encoding it
  #  encode_songs()


from flask import Flask, jsonify, session
from flask_restful import reqparse, abort, Api, Resource
from config import *


class Note:
    ID = -1

    def __init__(self, _id, title, content):
        self._id = _id
        self.title = title
        self.content = content

    def get_id(self):
        return self._id

    def get_title(self):
        if self.title:
            return self.title
        return self.content[:min(N, len(self.content))]

    def get_content(self):
        return self.content

    def contains(self, string):
        return string in self.get_title() or string in self.get_content()

    def to_json(self):
        return {
            'id': self.get_id(),
            'title': self.get_title(),
            'content': self.get_content()
        }

    @staticmethod
    def generate_id():
        Note.ID += 1
        return Note.ID


notes = {}


class NotesListApi(Resource):
    post_parser = reqparse.RequestParser()
    post_parser.add_argument('title', type=str, required=False)
    post_parser.add_argument('content', type=str, required=True)

    get_parser = reqparse.RequestParser()
    get_parser.add_argument('query', type=str, required=False)

    def get(self):
        args = NotesListApi.get_parser.parse_args()
        if not args or not args.get('query', None):
            return jsonify([notes[_id].to_json() for _id in notes])

        string = args['query']
        return jsonify([notes[_id].to_json() for _id in notes if notes[_id].contains(string)])

    def post(self):
        args = NotesListApi.post_parser.parse_args()
        note = Note(Note.generate_id(), args['title'], args['content'])
        notes[note.get_id()] = note
        return jsonify(note.to_json())


class NoteApi(Resource):
    put_parser = reqparse.RequestParser()
    put_parser.add_argument('title', type=str)
    put_parser.add_argument('content', type=str)

    def get(self, note_id):
        note = abort_if_note_not_found(note_id)

        return jsonify(note.to_json())

    def put(self, note_id):
        note = abort_if_note_not_found(note_id)
        args = NoteApi.put_parser.parse_args()
        if 'title' in args:
            note.title = args['title']
        if 'content' in args:
            note.content = args['content']

        return jsonify(note.to_json())

    def delete(self, note_id):
        abort_if_note_not_found(note_id)
        notes.pop(note_id)

        return jsonify({'message': f'Note {note_id} deleted'})


def abort_if_note_not_found(note_id):
    if note_id in notes:
        return notes[note_id]
    abort(404, message=f'Note {note_id} not found')


app = Flask(__name__)
app.config['SECRET_KEY'] = FLASK_SECRET_KEY

api = Api(app, catch_all_404s=True)
api.add_resource(NotesListApi, '/notes')
api.add_resource(NoteApi, '/note/<int:note_id>')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)

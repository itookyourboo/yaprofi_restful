from requests import get, post, delete, put

base_url = 'http://localhost:8000/{}'


def add_note(title, content):
    print(post(base_url.format('notes'), json={
        'title': title,
        'content': content
    }).json())


def put_note(note_id, title, content):
    print(put(base_url.format(f'note/{note_id}'), json={
        'title': title,
        'content': content
    }).json())


def delete_note(note_id):
    print(delete(base_url.format(f'note/{note_id}')).json())


def fill_notes():
    for i in range(5):
        add_note(f'Title{i}', f'Content{i}')


def get_notes(query=None):
    if query is None:
        print(get(base_url.format('notes')).json())
    else:
        print(get(base_url.format(f'notes?query={query}')).json())


# fill_notes()
# put_note(0, 'new Content', 'new Contenedksadks')
# delete_note(1)
# get_notes()
# get_notes('new')
# delete_note(10)

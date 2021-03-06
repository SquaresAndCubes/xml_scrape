from lxml import objectify, etree
import mysql.connector
from datetime import datetime
import random
import string

#key generator for database PK's

def show_keygen(size=7, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

def song_keygen(size=8, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

#config for DB connection

config = {
  'user': '',
  'password': '',
  'host': '0.0.0.0',
  'database': 'sts9',
  'raise_on_warnings': True
}

#database connection objects

mysql_client = mysql.connector.connect(**config)

sts9_db = mysql_client.cursor()

xml_data = objectify.parse('songs.xml')

root = xml_data.getroot()

## Database insert templates

shows_data = (

    "INSERT INTO shows "
    " (show_key, show_date, show_venue, show_city, show_state, show_country) "
    "VALUES (%s, %s, %s, %s, %s, %s)"
)

songs_data = (

    "INSERT INTO songs "
    " (song_key, show_key, song_name, song_set, song_track, song_encore, song_segue, song_notes, song_cover, song_with_guest) "
    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
)

#mail for look scrapes XML

for setlist in root.iterchildren(tag='setlist'):
    show_key = show_keygen()
    show_date = setlist.attrib['eventDate']
    show_venue = setlist.venue.attrib['name']
    show_city = setlist.venue.city.attrib['name']
    show_state = setlist.venue.city.attrib['stateCode']
    show_country = setlist.venue.city.country.attrib['code']
    song_track = 0
    for set in setlist.sets.iterchildren(tag='set'):

        for song in set.iterchildren(tag='song'):
            song_key = song_keygen()
            song_name = song.get('name')
            song_set = set.get('name')
            song_track = song_track + 1
            song_encore = set.get('encore')
            song_segue = None
            song_notes = None
            song_cover = None
            song_with_guest = None

            for detail in song.iterchildren(tag='info'):

                if detail.text == '>':
                    song_segue = detail.text
                else:
                    song_notes = detail.text

            for detaila in song.iterchildren(tag='cover'):
                song_cover = detaila.get('name')


            for detailb in song.iterchildren(tag='with'):
                song_with_guest = detailb.get('name')



            song_data = song_key, show_key, song_name, song_set, song_track, song_encore, song_segue, song_notes, song_cover, song_with_guest
            sts9_db.execute(songs_data, song_data)

            print(song_name, 'set: ' + str(song_set), 'track#: ' + str(song_track), 'encore: ' + str(song_encore), 'segue: ' + str(song_segue), 'notes: ' + str(song_notes), 'cover: ' +str(song_cover))


    show = show_key, datetime.strptime(show_date, '%d-%m-%Y').strftime('%Y-%m-%d'), show_venue, show_city, show_state, show_country

    print(show)

    sts9_db.execute(shows_data, show)


mysql_client.commit()
sts9_db.close()
mysql_client.close()







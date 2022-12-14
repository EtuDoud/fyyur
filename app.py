#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from crypt import methods
import json
import sys
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from models import Artist, Venue, Show, db




#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db.init_app(app)
migrate = Migrate(app, db)


# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

# class Venue(db.Model):
#     __tablename__ = 'Venue'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String)
#     city = db.Column(db.String(120))
#     state = db.Column(db.String(120))
#     address = db.Column(db.String(120))
#     phone = db.Column(db.String(120))
#     image_link = db.Column(db.String(500))
#     facebook_link = db.Column(db.String(120))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# class Artist(db.Model):
#     __tablename__ = 'Artist'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String())
#     city = db.Column(db.String(120))
#     state = db.Column(db.String(120))
#     phone = db.Column(db.String(120))
#     genres = db.Column(db.String(120))
#     image_link = db.Column(db.String(500))
#     facebook_link = db.Column(db.String(120))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
  # data=[{
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "venues": [{
  #     "id": 1,
  #     "name": "The Musical Hop",
  #     "num_upcoming_shows": 0,
  #   }, {
  #     "id": 3,
  #     "name": "Park Square Live Music & Coffee",
  #     "num_upcoming_shows": 1,
  #   }]
  # }, {
  #   "city": "New York",
  #   "state": "NY",
  #   "venues": [{
  #     "id": 2,
  #     "name": "The Dueling Pianos Bar",
  #     "num_upcoming_shows": 0,
  #   }]
  # }]

  resultats = Venue.query.all()
  data = {}
  datas = []
  venues = []

  for result in resultats:
    upcoming_shows  = db.session.query(Show).join(Venue).filter(Show.venue_id == result.id)\
    .filter(Show.start_time>datetime.now()).all()

    id = result.id
    name = result.name
    city = result.city
    state = result.state

    ville = (city, state)
    if ville not in data:
      data[ville] = { 'city' : city, 'state ': state, 'venues': []}
    data[ville]['venues'].append(
      {
        "id": id,
        "name": name,
        "num_upcoming_shows": len(upcoming_shows)
          }
        )

    datas = [data[k] for k in data.keys()]
  return render_template('pages/venues.html', areas = datas )

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  # response={
  #   "count": 1,
  #   "data": [
  #     {
  #     "id": 2,
  #     "name": "The Dueling Pianos Bar",
  #     "num_upcoming_shows": 0,
  #   }
  #   ]
  # }


  #je recupere depuis la db tous les venues en fonction de mon terme de recherche.
  search_term = request.form.get('search_term', '') # je viens de copier 
  
  results = Venue.query.filter(Venue.name.ilike(f'% {search_term}%')).all()

  # upcoming_shows  = db.session.query(Show).join(Venue).filter(Show.venue_id == results.id)\
  #  .filter(Show.start_time>datetime.datetime.now()).all()
  
  response = {
   "count": len(results),
   "data": results
   }
  return render_template(
    'pages/search_venues.html', 
    results=response, 
    search_term=request.form.get('search_term', '')
  )

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id

  venues = Venue.query.filter( Venue.id == venue_id )


  if venues == None:
    return not_found_error(404)

  data = {
    'id': venues.id,
     'name': venues.name,
     'genres': venues.genres,
     'address': venues.address,
     'city': venues.city,
     'state': venues.state,
     'phone': venues.phone,
     'website_link': venues.website_link,
     'facebook_link': venues.facebook_link,
     'seeking_talent': venues.seeking_talent,
     'seeking_description': venues.seeking_description,
     'image_link': venues.image_link,
      'past_shows': [],
      'upcoming_shows' : [],
      'past_shows_count' : 0,
      'upcoming_shows_count' : 0,

     }


  shows = Show.query.filter(Show.venue_id==venue_id).all()
  for show in shows:
      if show.start_time >= datetime.datetime.now():
          data['upcoming_shows_count'] += 1
          data['upcoming_shows'].append({
              'artist_id': show.artist.id,
              'artist_name': show.artist.name,
              'artist_image_link': show.artist.image_link,
              'start_time': format_datetime(str(show.start_time))
          })
      else:
          data['past_shows_count'] += 1
          data['past_shows'].append({
              'artist_id': show.artist.id,
              'artist_name': show.artist.name,
              'artist_image_link': show.artist.image_link,
              'start_time': format_datetime(str(show.start_time))
          })


  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():

  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  form = VenueForm(request.form)
  error = False

  try:
    venue = Venue(
      name=form.name.data,
      city=form.city.data,
      state=form.state.data,
      address=form.address.data,
      phone=form.phone.data,
      genres=form.genres.data,
      image_link=form.image_link.data,
      facebook_link=form.facebook_link.data,
      website_link=form.website_link.data,
      seeking_description=form.seeking_description.data,
      seeking_talent=form.seeking_talent.data,
    )
    db.session.add(venue)
    db.session.commit()
  
  except:
    db.session.rollback()
    error = True
    print(sys.exc_info())
  finally:
    db.session.close()
    if error :
      flash('An error occurred. Venue ' + venue.name + ' could not be listed.')
    else:
      flash('Venue ' + request.form['name'] + ' was successfully listed!')

  return render_template('pages/home.html', form = form)


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  venues = Venue.query.get(venue_id)
  name = venues.name
  error = False
  try:
    Venue.query.filter_by(id=venue_id).delete()
    db.session.commit()
  except:
    db.session.rollback()
    error = True
    print(sys.exc_info())
  finally:
    db.session.close()
    if error:
      flash('An error occurred.')
    else:
      flash('An error occurred. Venue ' + name + ' could not be listed.')


  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  # data=[{
  #   "id": 4,
  #   "name": "Guns N Petals",
  # }, {
  #   "id": 5,
  #   "name": "Matt Quevedo",
  # }, {
  #   "id": 6,
  #   "name": "The Wild Sax Band",
  # }]

  data = db.session.query(Artist.id, Artist.name)

  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  # response={
  #   "count": 1,
  #   "data": [{
  #     "id": 4,
  #     "name": "Guns N Petals",
  #     "num_upcoming_shows": 0,
  #   }]
  # }

  search_term=request.form.get('search_term', '')
  results = Artist.query.filter(Artist.name.ilike(f'% {search_term}%')).all()
  # upcoming_shows  = db.session.query(Show).join(Artist).filter(Show.artist_id == results.id)\
  #   .filter(Show.start_time>datetime.datetime.now()).all()

  response = {
    "count": len(results),
    "data": results # ??? [ je n'ai pas compris cette partie la ... parcequ'on a besoin de id, name et upcomming show ]
  }

#   response["data"].append(
#     {
#       "id": results.id,
#       "name": results.name,
#       "num_upcoming_shows": len(upcoming_shows)
# ,    }
#   )


  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
  artists = Artist.query.filter( Artist.id == artist_id )


  if artists == None:
    return not_found_error(404)

  data = {
    'id': artists.id,
     'name': artists.name,
     'genres': artists.genres,
     'address': artists.address,
     'city': artists.city,
     'state': artists.state,
     'phone': artists.phone,
     'website_link': artists.website_link,
     'facebook_link': artists.facebook_link,
     'seeking_talent': artists.seeking_talent,
     'seeking_description': artists.seeking_description,
     'image_link': artists.image_link,
      'past_shows': [],
      'upcoming_shows' : [],
      'past_shows_count' : 0,
      'upcoming_shows_count' : 0,

     }


  shows = Show.query.filter(Show.artist_id==artist_id).all()
  for show in shows:
      if show.start_time >= datetime.datetime.now():
          data['upcoming_shows_count'] += 1
          data['upcoming_shows'].append({
              'artist_id': show.artist.id,
              'artist_name': show.artist.name,
              'artist_image_link': show.artist.image_link,
              'start_time': format_datetime(str(show.start_time))
          })
      else:
          data['past_shows_count'] += 1
          data['past_shows'].append({
              'artist_id': show.artist.id,
              'artist_name': show.artist.name,
              'artist_image_link': show.artist.image_link,
              'start_time': format_datetime(str(show.start_time))
          })

  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist = Artist.query.get(artist_id)
  if artist is None:
    flash(f"Artist does not exist")
    return redirect(url_for('index'))

  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  form = ArtistForm(request.form)
  error = False
  try:
    artist = Artist.query.filter_by(id=artist_id)
    artist.name=form.name.data,
    artist.city=form.city.data,
    artist.state=form.state.data,
    artist.phone=form.phone.data,
    artist.genres=form.genres.data,
    artist.image_link=form.image_link.data,
    artist.facebook_link=form.facebook_link.data,
    artist.website_link=form.website_link.data,
    artist.seeking_description=form.seeking_description.data,
    artist.seeking_venue=form.seeking_venue.data,
    db.session.commit()
  except:
    db.session.rollback()
    error = True
    print(sys.exc_info())
  finally:
    db.session.close()
    if error:
      flash('An error occurred. Venue ' + artist.name + ' could not be listed.')
    else:
      flash('well done ' + artist.name + 'succes') 

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venue.query.get(venue_id)
  if venue is None:
    flash(f"Venue does not exist")
    return redirect(url_for('index'))

  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  
  form = VenueForm(request.form)
  error = False
  try:
    venue = Venue.query.filter_by(id=venue_id)
    venue.name=form.name.data,
    venue.city=form.city.data,
    venue.state=form.state.data,
    venue.address=form.address.data,
    venue.phone=form.phone.data,
    venue.genres=form.genres.data,
    venue.image_link=form.image_link.data,
    venue.facebook_link=form.facebook_link.data,
    venue.website_link=form.website_link.data,
    venue.seeking_description=form.seeking_description.data,
    venue.seeking_talent=form.seeking_talent.data,
    db.session.commit()
  except:
    db.session.rollback()
    error = True
    print(sys.exc_info())
  finally:
    db.session.close()
    if error:
      flash('An error occurred. Venue ' + venue.name + ' could not be listed.')
    else:
      flash('well done ' + venue.name + 'succes') # ???

  return redirect(url_for('show_artist', venue_id=venue_id))
  
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  form = ArtistForm(request.form)
  error = False

  try:
    artist = Artist(
      name=form.name.data,
      city=form.city.data,
      state=form.state.data,
      phone=form.phone.data,
      genres=form.genres.data,
      image_link=form.image_link.data,
      facebook_link=form.facebook_link.data,
      website_link=form.website_link.data,
      seeking_description=form.seeking_description.data,
      seeking_venue=form.seeking_venue.data,
    )
    db.session.add(artist)
    db.session.commit()
  
  except:
    db.session.rollback()
    error = True
    print(sys.exc_info())
  finally:
    db.session.close()
    if error :
      flash('An error occurred. Venue ')
    else:
      flash('Artist ' + request.form['name'] + ' was successfully listed!')
  return render_template('pages/home.html', form = form)

#  Shows
#  ----------------------------------------------------------------

@app.route('/shows', methods=['GET'])
def shows():

    shows = Show.query.all()
    data = []
    for show in shows:
        data.append({
            'venue_id': show.venue.id,
            'venue_name': show.venue.name,
            'artist_id': show.artist.id,
            'artist_name': show.artist.name,
            'artist_image_link': show.artist.image_link,
            'start_time': format_datetime(str(show.start_time))
        })
    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create', methods=['GET'])
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    form = ShowForm()
    error = False
    try:
      show = Show(
        artist_id = form.artist_id.data,
        venue_id = form.venue_id.data,
        start_time = form.start_time.data
      )

      db.session.add(show)
      db.session.commit()       
    except:
        db.session.rollback()
        error = True
        print(sys.exc_info())
    finally:
        db.session.close()
        if error:
            flash('An error occurred. Show could not be listed.')
        else:
            flash('Show was successfully listed!')

    return redirect(url_for('index'))

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500



if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''

from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
import requests
from django.conf import settings
from django.db.models import Q
from .models import Movie, Watched, Comment
from .forms import UserUpdateForm, ProfileUpdateForm
from random import randint
import urllib3


def home(request):
  return render(request, 'home.html')

# teste de modificações na home
def teste(request):
  genre = request.GET.get('genre')
  context = {'genre': genre}
  print(genre)
  return render(request, 'teste.html', context)



def login_user(request):
    if request.method == "POST":
        user = authenticate(username=request.POST["username"],
                            password=request.POST["password"])
        if user != None:
            login(request, user)
            return redirect("home")

        else:
            return render(request, "login.html")

    if request.user.is_authenticated:
        return redirect("home")

    return render(request, "login.html")


def registrar_user(request):
    if request.method == "POST":
        user = User.objects.create_user(request.POST["username"],
                                        request.POST["email"],
                                        request.POST["password"])
        user.groups.add(Group.objects.get(name="stdUser"))
        user.save()
        login(request, user)
        return redirect("home")
    return render(request, 'registre-se.html')


def logout_user(request):
    if request.method == "POST":
        if "Sim" in request.POST:
            logout(request)
            return redirect("home")
        else:
            return redirect("home")
    return render(request, "logout.html")



def search(request):
  
  if request.method == "POST":
    movie_title = request.POST.get("search")
  elif request.method == "GET":
    movie_title = request.GET.get("title")
      
    # OMDB
  omdb_api_key = settings.OMDB_API_KEY
  omdb_url = f"http://www.omdbapi.com/?apikey={omdb_api_key}&t={movie_title}"
  omdb_response = requests.get(omdb_url)
  movie_data = omdb_response.json()

  if movie_data.get('Response') == 'False':
    context = {
      'movie_data': {}
    }
    return render(request, 'search.html', context)
  else:
    add_to_database(movie_data)
    
  comments = Comment.objects.filter(movie=Movie.objects.filter(title = movie_title).first()).all()
  
  watched = Watched.objects.filter(user=request.user, movie__title=movie_title).first()
  if watched:
      rating = watched.rating
  else:
    rating = None

  # TMDB
  tmdb_api_key = settings.TMDB_API_KEY
  tmdb_search_url = f"https://api.themoviedb.org/3/search/movie"
  tmdb_params = {
      'api_key': tmdb_api_key,
      'query': movie_title
  }

  tmdb_response = requests.get(tmdb_search_url, params=tmdb_params)
  tmdb_movie_data = tmdb_response.json()

  tmdb_watch_providers_data = None
  first_three_providers = None
  if tmdb_movie_data.get('results'):
      tmdb_movie_id = tmdb_movie_data['results'][0]['id']
      tmdb_watch_providers_url = f"https://api.themoviedb.org/3/movie/{tmdb_movie_id}/watch/providers"
      tmdb_providers_params = {
          'api_key': tmdb_api_key
      }
      tmdb_providers_response = requests.get(tmdb_watch_providers_url, params=tmdb_providers_params)
      tmdb_watch_providers_data = tmdb_providers_response.json()

      providers = tmdb_watch_providers_data.get('results', {}).get('BR', {}).get('flatrate', [])
      first_three_providers = providers[:3] if providers else []
  context = {'movie_data': movie_data, 'first_three_providers': first_three_providers, 'comments': comments, 'watched' : watched, 'rating' : rating}
  return render(request, 'search.html', context)
  
    # comments = Comment.objects.filter(movie=Movie.objects.filter(title = movie_title).first()).all()
    # # OMDB
    # omdb_api_key = settings.OMDB_API_KEY
    # omdb_url = f"http://www.omdbapi.com/?apikey={omdb_api_key}&t={movie_title}"
    # omdb_response = requests.get(omdb_url)
    # movie_data = omdb_response.json()

    # if movie_data.get('Response') == 'False':
    #   context = {
    #     'movie_data': {}
    #   }
    #   return render(request, 'search.html', context)
    # else:
    #   add_to_database(movie_data)

    # # TMDB
    # tmdb_api_key = settings.TMDB_API_KEY
    # tmdb_search_url = f"https://api.themoviedb.org/3/search/movie"
    # tmdb_params = {
    #     'api_key': tmdb_api_key,
    #     'query': movie_title
    # }

    # tmdb_response = requests.get(tmdb_search_url, params=tmdb_params)
    # tmdb_movie_data = tmdb_response.json()

    # tmdb_watch_providers_data = None
    # if tmdb_movie_data.get('results'):

    #     tmdb_movie_id = tmdb_movie_data['results'][0]['id']

    #     tmdb_watch_providers_url = f"https://api.themoviedb.org/3/movie/{tmdb_movie_id}/watch/providers"
    #     tmdb_providers_params = {
    #         'api_key': tmdb_api_key
    #     }
    #     tmdb_providers_response = requests.get(tmdb_watch_providers_url, params=tmdb_providers_params)
    #     tmdb_watch_providers_data = tmdb_providers_response.json()

    #     providers = tmdb_watch_providers_data.get('results', {}).get('BR', {}).get('flatrate', [])
    #     first_three_providers = providers[:3] if providers else []

    # context = {'movie_data': movie_data, 'first_three_providers': first_three_providers, 'comments': comments}
    # return render(request, 'search.html', context)
  return render(request, 'search.html', context={'comments': comments, 'watched' : watched, 'rating' : rating})
  return redirect("home")

def db_search(request, movie_id):
    movie = Movie.objects.filter(id=movie_id).first()
    render(request, "db_search.html", context={'movie': movie})

@login_required
def profile_page(request, username):
  profile = User.objects.filter(username=request.user.__str__()).first()
  u_form = UserUpdateForm()
  p_form = ProfileUpdateForm()
  movies = profile.profile.watched_movies.all()
  watched = Watched.objects.filter(user=profile).all()
  # ratings = []
  # for m in movies:
  #   w = Watched.objects.filter(movie=m).first()
  #   ratings.append(w.rating)
  return render(request, 'profile.html', {'profile': profile, 'u_form' : u_form, 'p_form' : p_form, 'movies': movies, 'watched' : watched})

@login_required
def update_profile_page(request, username):
  user = User.objects.filter(username=request.user.__str__()).first()
  if request.method == "GET":
    u_form = UserUpdateForm(instance=user)
    p_form = ProfileUpdateForm(instance=user.profile)
    return render(request, 'update_profile.html', {'u_form' : u_form, 'p_form' : p_form})
  elif request.method == 'POST':
    u_form = UserUpdateForm(request.POST, instance=user)
    p_form = ProfileUpdateForm(request.POST, request.FILES, instance=user.profile)
    if u_form.is_valid() and p_form.is_valid():
      u_form.save()
      p_form.save()
      return redirect(f'/profile/{username}/')
    return render(request, 'update_profile.html', {'user': user, 'u_form' : u_form, 'p_form' : p_form})

@login_required
def add_watched_movie(request, username, movie_id):
  id = int(movie_id[2:])
  user = User.objects.filter(username=request.user.__str__()).first()
  movie = Movie.objects.filter(id=id).first()
  if request.method == 'GET':
    return render(request, 'add_watched.html', context={"movie": movie, "user":user, })
  if request.method == 'POST' and movie:
    rate = int(request.POST['rating'])
    w = Watched.objects.create(rating=rate, movie=movie)
    w.user.add(user)
    user.profile.watched_movies.add(movie)
    user.save()
    return redirect(f"/profile/{username}/")
  return redirect("/home/")


@login_required
def recommendation(request):
  profile = User.objects.filter(username=request.user.__str__()).first()
  
  genre = request.GET.get('genre')
  rated = request.GET.get('rated')
  director = request.GET.get('director')
  country = request.GET.get('country')
  recommend_new = request.GET.get('recommend_new')
  min_rating = request.GET.get('min_rating')
  if not min_rating: min_rating = 5 
  min_votes = request.GET.get('min_votes')
  if not min_votes: min_votes = 1000
  min_year = request.GET.get('min_year')
  if not min_year: min_year = 1900
  max_year = request.GET.get('max_year')
  if not max_year: max_year = 2100
  min_runtime = request.GET.get('min_runtime')
  if not min_runtime: min_runtime = 0
  max_runtime = request.GET.get('max_runtime')
  if not max_runtime: max_runtime = 10000
  watched = profile.profile.watched_movies.all()
  
  
  query = Q(imdb_rating__gte=min_rating, imdb_votes__gte=min_votes, year__gte=min_year, year__lte=max_year, runtime__gte=min_runtime, runtime__lte=max_runtime)
  
  if genre:
    query &= Q(genre__icontains=genre)
  if rated:
    query &= Q(rated__lte=rated)
  if director:
    query &= Q(director__icontains=director)
  if country:
    query &= Q(country__icontains=country)

  
  movies = Movie.objects.filter(query)
  if recommend_new:
    movies = movies.exclude(id__in=watched)
  movie_amount = movies.count()
  if (movie_amount > 0):
    index = randint(0, movie_amount - 1)
    movie = movies[index]
    
    # Pesquisa na API
    omdb_api_key = settings.OMDB_API_KEY
    omdb_url = f"http://www.omdbapi.com/?apikey={omdb_api_key}&t={movie.title}"
    omdb_response = requests.get(omdb_url)
    movie_data = omdb_response.json()
    
    # TMDB
    tmdb_api_key = settings.TMDB_API_KEY
    tmdb_search_url = f"https://api.themoviedb.org/3/search/movie"
    tmdb_params = {
        'api_key': tmdb_api_key,
        'query': movie.title,
    }
    tmdb_response = requests.get(tmdb_search_url, params=tmdb_params)
    tmdb_movie_data = tmdb_response.json()
    tmdb_watch_providers_data = None
    if tmdb_movie_data.get('results'):
        tmdb_movie_id = tmdb_movie_data['results'][0]['id']
        tmdb_watch_providers_url = f"https://api.themoviedb.org/3/movie/{tmdb_movie_id}/watch/providers"
        tmdb_providers_params = {
            'api_key': tmdb_api_key
        }
        tmdb_providers_response = requests.get(tmdb_watch_providers_url, params=tmdb_providers_params)
        tmdb_watch_providers_data = tmdb_providers_response.json()
        providers = tmdb_watch_providers_data.get('results', {}).get('BR', {}).get('flatrate', [])
        first_three_providers = providers[:3] if providers else []
    comments = Comment.objects.filter(movie=movie)
    context = {'movie_data': movie_data, 'first_three_providers': first_three_providers, 'comments': comments}
    return render(request, 'search.html', context)
  else:
    movie_data = {}
  context = {
    'movie_data': movie_data
  }
  return render(request, 'search.html', {'movie_data': {}})


@login_required
def import_database(request):
  omdb_api_key = settings.OMDB_API_KEY
  for i in range(100000, 100050):
    n = 7 - len(str(i))
    movie_id = 'tt' + '0' * n + str(i)
   
    omdb_url = f"http://www.omdbapi.com/?apikey={omdb_api_key}&i={movie_id}"
    response = requests.get(omdb_url)
    movie_data = response.json()
    print(movie_data)
    if movie_data.get('Response') == 'False':
      movie_data = {}
    
    add_to_database(movie_data)

  return render(request, 'home.html')


def add_to_database(movie_data):
  movie_id = int(movie_data['imdbID'][2:])
  
  movie = Movie(id = movie_id,
    title = movie_data['Title'],
    rated = movie_data['Rated'],
    released = movie_data['Released'],
    genre = movie_data['Genre'],
    director = movie_data['Director'],
    writer = movie_data['Writer'],
    actors = movie_data['Actors'],
    plot = movie_data['Plot'],
    language = movie_data['Language'],
    country = movie_data['Country'],
    awards = movie_data['Awards'],
    poster = movie_data['Poster'],
    imdb_id = movie_data['imdbID'],
    type = movie_data['Type'])
  
  if movie_data['imdbRating'] != 'N/A':
    movie.imdb_rating = float(movie_data['imdbRating'])
  else:
    movie.imdb_rating = None
  
  for [string, parameter, remove] in [['Runtime', 'runtime', ' min'], 
                                      ['Metascore', 'metascore', ''],
                                      ['imdbVotes', 'imdb_votes', ',']]:
    if movie_data[string] != 'N/A':
      setattr(movie, parameter, int(movie_data[string].replace(remove, '')))
    else:
      setattr(movie, parameter, None)
  
  if movie.type == 'movie':
    movie.dvd = movie_data['DVD']
    if movie_data['Year'] != 'N/A':
      movie.year = int(movie_data['Year'])
    else:
      movie.year = None
    if movie_data['BoxOffice'] != 'N/A':
      movie.box_office = int(movie_data['BoxOffice'].replace(',', '').replace('$', ''))
    else:
      movie.box_office = None
    movie.production = movie_data['Production']
    movie.website = movie_data['Website']
  elif movie.type == 'series':
    if movie_data['Year'] != 'N/A' and '–' in movie_data['Year']:
      start_year = movie_data['Year'].split('–')[0]
      end_year = movie_data['Year'].split('–')[1]
      if start_year:
        movie.year = int(start_year)
      else:
        movie.year = None
      if end_year:
        movie.end_year = int(end_year)
      else:
        movie.end_year = None
    elif movie_data['Year'] != 'N/A':
      movie.year = int(movie_data['Year'])
    else:
      movie.year = None
      movie.end_year = None
    movie.total_seasons = movie_data['totalSeasons']

  movie.save()
  return

def movies(request):

  tmdb_api_key = settings.TMDB_API_KEY
  tmdb_popular_url = f"https://api.themoviedb.org/3/movie/popular"
  tmdb_top_rated_url = f"https://api.themoviedb.org/3/movie/top_rated"
  tmdb_params = {
      'api_key': tmdb_api_key
  }
  
  #POPULAR
  tmdb_response = requests.get(tmdb_popular_url, params=tmdb_params)
  tmdb_popular_data = tmdb_response.json()
  popular_movies = [{'title': movie['title'], 'id': movie['id']} for movie in tmdb_popular_data.get('results', [])]

  #TOP RATED
  tmdb_response = requests.get(tmdb_top_rated_url, params=tmdb_params)
  tmdb_top_rated_data = tmdb_response.json()
  top_rated_movies = [{'title': movie['title'], 'id': movie['id']} for movie in tmdb_top_rated_data.get('results', [])]

  #POPULAR
  omdb_api_key = settings.OMDB_API_KEY
  for movie in popular_movies:
    title = movie['title']
    omdb_url = f"http://www.omdbapi.com/?apikey={omdb_api_key}&t={title}"
    omdb_response = requests.get(omdb_url)
    omdb_data = omdb_response.json()
    poster_url = omdb_data.get('Poster')
    movie["url"] = poster_url

  #TOP RATED
  for movie in top_rated_movies:
    title = movie['title']
    omdb_url = f"http://www.omdbapi.com/?apikey={omdb_api_key}&t={title}"
    omdb_response = requests.get(omdb_url)
    omdb_data = omdb_response.json()
    poster_url = omdb_data.get('Poster')
    movie["url"] = poster_url

  #ACTION
  action_movies = Movie.objects.filter(genre__icontains='Action').order_by('?')[:20]
  action_movies_data = []
  for movie in action_movies:
      omdb_url = f"http://www.omdbapi.com/?apikey={omdb_api_key}&t={movie.title}"
      omdb_response = requests.get(omdb_url)
      omdb_data = omdb_response.json()
      poster_url = omdb_data.get('Poster')
      # poster_url = movie.poster
      # if poster_url and poster_url!="N/A":
      #   response_poster = requests.get(poster_url, verify=False)
      #   if response_poster.status_code == 200:
      #     action_movies_data.append({'title': movie.title, 'url': poster_url})
      action_movies_data.append({'title': movie.title, 'url': poster_url})


  #ADVENTURE
  adventure_movies = Movie.objects.filter(genre__icontains='Adventure').order_by('?')[:20]
  adventure_movies_data = []
  for movie in adventure_movies:
      omdb_url = f"http://www.omdbapi.com/?apikey={omdb_api_key}&t={movie.title}"
      omdb_response = requests.get(omdb_url)
      omdb_data = omdb_response.json()
      poster_url = omdb_data.get('Poster')
      # poster_url = movie.poster
      # if poster_url and poster_url!="N/A":
      #   response_poster = requests.get(poster_url, verify=False)
      #   if response_poster.status_code == 200:
      #     adventure_movies_data.append({'title': movie.title, 'url': poster_url})
      adventure_movies_data.append({'title': movie.title, 'url': poster_url})

  #COMEDY
  comedy_movies = Movie.objects.filter(genre__icontains='Comedy').order_by('?')[:20]
  comedy_movies_data = []
  for movie in comedy_movies:
      omdb_url = f"http://www.omdbapi.com/?apikey={omdb_api_key}&t={movie.title}"
      omdb_response = requests.get(omdb_url)
      omdb_data = omdb_response.json()
      poster_url = omdb_data.get('Poster')
      # poster_url = movie.poster
      # if poster_url and poster_url!="N/A":
      #   response_poster = requests.get(poster_url, verify=False)
      #   if response_poster.status_code == 200:
      #     comedy_movies_data.append({'title': movie.title, 'url': poster_url})
      comedy_movies_data.append({'title': movie.title, 'url': poster_url})

  #DRAMA
  drama_movies = Movie.objects.filter(genre__icontains='Drama').order_by('?')[:20]
  drama_movies_data = []
  for movie in drama_movies:
      omdb_url = f"http://www.omdbapi.com/?apikey={omdb_api_key}&t={movie.title}"
      omdb_response = requests.get(omdb_url)
      omdb_data = omdb_response.json()
      poster_url = omdb_data.get('Poster')
      # poster_url = movie.poster
      # if poster_url and poster_url!="N/A":
      #   response_poster = requests.get(poster_url, verify=False)
      #   if response_poster.status_code == 200:
      #     drama_movies_data.append({'title': movie.title, 'url': poster_url})
      drama_movies_data.append({'title': movie.title, 'url': poster_url})

  #HORROR
  horror_movies = Movie.objects.filter(genre__icontains='Horror').order_by('?')[:20]
  horror_movies_data = []
  for movie in horror_movies:
      omdb_url = f"http://www.omdbapi.com/?apikey={omdb_api_key}&t={movie.title}"
      omdb_response = requests.get(omdb_url)
      omdb_data = omdb_response.json()
      poster_url = omdb_data.get('Poster')
      # poster_url = movie.poster
      # if poster_url and poster_url!="N/A":
      #   response_poster = requests.get(poster_url, verify=False)
      #   if response_poster.status_code == 200:
      #     horror_movies_data.append({'title': movie.title, 'url': poster_url})
      horror_movies_data.append({'title': movie.title, 'url': poster_url})

  #Sci-Fi
  Sci_Fi_movies = Movie.objects.filter(genre__icontains='Sci-Fi').order_by('?')[:20]
  Sci_Fi_movies_data = []
  for movie in Sci_Fi_movies:
      omdb_url = f"http://www.omdbapi.com/?apikey={omdb_api_key}&t={movie.title}"
      omdb_response = requests.get(omdb_url)
      omdb_data = omdb_response.json()
      poster_url = omdb_data.get('Poster')
      # poster_url = movie.poster
      # if poster_url and poster_url!="N/A":
      #   response_poster = requests.get(poster_url, verify=False)
      #   if response_poster.status_code == 200:
      #     Sci_Fi_movies_data.append({'title': movie.title, 'url': poster_url})
      Sci_Fi_movies_data.append({'title': movie.title, 'url': poster_url})

  #ROMANCE
  Romance_movies = Movie.objects.filter(genre__icontains='Romance').order_by('?')[:20]
  Romance_movies_data = []
  for movie in Romance_movies:
      omdb_url = f"http://www.omdbapi.com/?apikey={omdb_api_key}&t={movie.title}"
      omdb_response = requests.get(omdb_url)
      omdb_data = omdb_response.json()
      poster_url = omdb_data.get('Poster')
      # poster_url = movie.poster
      # if poster_url and poster_url!="N/A":
      #   response_poster = requests.get(poster_url, verify=False)
      #   if response_poster.status_code == 200:
      #     Romance_movies_data.append({'title': movie.title, 'url': poster_url})
      Romance_movies_data.append({'title': movie.title, 'url': poster_url})

  #DOCUMENTARY
  Documentary_movies = Movie.objects.filter(genre__icontains='Documentary').order_by('?')[:20]
  Documentary_movies_data = []
  for movie in Documentary_movies:
      omdb_url = f"http://www.omdbapi.com/?apikey={omdb_api_key}&t={movie.title}"
      omdb_response = requests.get(omdb_url)
      omdb_data = omdb_response.json()
      poster_url = omdb_data.get('Poster')
      # poster_url = movie.poster
      if poster_url and poster_url!="N/A":
        response_poster = requests.get(poster_url, verify=False)
        if response_poster.status_code == 200:
          Documentary_movies_data.append({'title': movie.title, 'url': poster_url})
      # Documentary_movies_data.append({'title': movie.title, 'url': poster_url})

  #MUSIC
  Music_movies = Movie.objects.filter(genre__icontains='Music').order_by('?')[:20]
  Music_movies_data = []
  for movie in Music_movies:
      omdb_url = f"http://www.omdbapi.com/?apikey={omdb_api_key}&t={movie.title}"
      omdb_response = requests.get(omdb_url)
      omdb_data = omdb_response.json()
      poster_url = omdb_data.get('Poster')
      # poster_url = movie.poster
      if poster_url and poster_url!="N/A":
        response_poster = requests.get(poster_url, verify=False)
        if response_poster.status_code == 200:
          Music_movies_data.append({'title': movie.title, 'url': poster_url})
      # Music_movies_data.append({'title': movie.title, 'url': poster_url})

  
  context = {
      'popular_movies': popular_movies,
      'top_rated_movies': top_rated_movies,
      'action_movies':action_movies_data,
      'adventure_movies':adventure_movies_data,
      'comedy_movies':comedy_movies_data,
      'drama_movies': drama_movies_data,
      'horror_movies': horror_movies_data,
      'sci_fi_movies': Sci_Fi_movies_data,
      'romance_movies': Romance_movies_data,
      'documentary_movies': Documentary_movies_data,
      'music_movies': Music_movies_data,
  }
  return render(request, 'movies.html', context)
  

def movies2(request):
  tmdb_api_key = settings.TMDB_API_KEY
  tmdb_params = {
      'api_key': tmdb_api_key
  }
  omdb_api_key = settings.OMDB_API_KEY
  genre_set = ['Action', 'Adventure', 'Animation', 'Comedy', 'Documentary', 'Drama', 'Horror', 'Sci-Fi', 'Romance', 'Music']
  context = {}

  for category in ['popular', 'top_rated']:
    tmdb_url = f"https://api.themoviedb.org/3/movie/{category}"
    tmdb_response = requests.get(tmdb_url, params=tmdb_params)
    tmdb_data = tmdb_response.json()
    
    movies = [{'title': movie['title'], 'id': movie['id']} for movie in tmdb_data.get('results', [])]
    for movie in movies:
      title = movie['title']
      omdb_url = f"http://www.omdbapi.com/?apikey={omdb_api_key}&t={title}"
      omdb_response = requests.get(omdb_url)
      omdb_data = omdb_response.json()
      poster_url = omdb_data.get('Poster')
      movie["url"] = poster_url
      context[category] = movies
  
  for genre in genre_set:
    movies = Movie.objects.filter(genre__icontains=genre).order_by('?')[:20]
    movies_data = []
    if genre == "Sci-Fi":
      genre = "Sci_Fi"
    for movie in movies:
        poster_url = movie.poster
        if poster_url and poster_url!="N/A":
          response_poster = requests.get(poster_url)
          if response_poster.status_code == 200:
            movies_data.append({'title': movie.title, 'url': poster_url})
        context[genre] = movies_data
  return render(request, 'movies2.html', context)


#def comment(request):
#  if request.method == 'POST':
#    form = CommentsForm(request.POST)
#    if form.is_valid():
#      form.save()
#      return redirect('home')
#  else:
#    form = CommentsForm()
#  return render(request, 'search.html', {'form': form})

def comments(request, username, movie_title):
  profile = User.objects.filter(username=username).first().profile
  movie = Movie.objects.filter(title=movie_title).first()
  if request.method == 'POST':
    comment = Comment.objects.create(
      comment = request.POST["comment"],
      movie = movie,
      )
    comment.profile.clear()
    comment.profile.add(profile)
    comment.save()
    return redirect(f"/search?title={movie.title}")
  return redirect(f"/search?title={movie.title}")
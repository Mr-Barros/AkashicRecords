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
  comments = Comment.objects.all()
  if request.method == "POST":
      movie_title = request.POST.get("search")

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

          # TESTE ID
          print(f"TMDB Movie ID: {tmdb_movie_id}")

          tmdb_watch_providers_url = f"https://api.themoviedb.org/3/movie/{tmdb_movie_id}/watch/providers"
          tmdb_providers_params = {
              'api_key': tmdb_api_key
          }
          tmdb_providers_response = requests.get(tmdb_watch_providers_url, params=tmdb_providers_params)
          tmdb_watch_providers_data = tmdb_providers_response.json()

          providers = tmdb_watch_providers_data.get('results', {}).get('BR', {}).get('flatrate', [])
          first_three_providers = providers[:3] if providers else []
        #TESTE ONDE ASSITIR
          #print(first_three_providers)

    
      context = {'movie_data': movie_data, 'first_three_providers': first_three_providers, 'comments': comments}
      return render(request, 'search.html', context)
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
    if tmdb_movie_data.get('results'):

        tmdb_movie_id = tmdb_movie_data['results'][0]['id']

        # TESTE ID
        print(f"TMDB Movie ID: {tmdb_movie_id}")

        tmdb_watch_providers_url = f"https://api.themoviedb.org/3/movie/{tmdb_movie_id}/watch/providers"
        tmdb_providers_params = {
            'api_key': tmdb_api_key
        }
        tmdb_providers_response = requests.get(tmdb_watch_providers_url, params=tmdb_providers_params)
        tmdb_watch_providers_data = tmdb_providers_response.json()

        providers = tmdb_watch_providers_data.get('results', {}).get('BR', {}).get('flatrate', [])
        first_three_providers = providers[:3] if providers else []
      #TESTE ONDE ASSITIR
        #print(first_three_providers)


    context = {'movie_data': movie_data, 'first_three_providers': first_three_providers, 'comments': comments}
    return render(request, 'search.html', context)
  return render(request, 'search.html', context={'comments': comments})
  return redirect("home")


@login_required
def profile_page(request, username):
  profile = User.objects.filter(username=request.user.__str__()).first()
  u_form = UserUpdateForm()
  p_form = ProfileUpdateForm()
  movies = profile.profile.watched_movies.all()
  return render(request, 'profile.html', {'profile': profile, 'u_form' : u_form, 'p_form' : p_form, 'movies': movies})

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
      print("DEU RUIM")
    return render(request, 'update_profile.html', {'user': user, 'u_form' : u_form, 'p_form' : p_form})


@login_required
def add_watched_movie(request, username):
  user = User.objects.filter(username=request.user.__str__()).first()
  movie = Movie.objects.filter(id=request.POST.get('imdb_id')).first()
  if request.method == 'GET':
    return redirect("/search/")
  if request.method == 'POST' and movie:
    user.profile.watched_movies.add(movie)
    user.save()
    return redirect("/search/")
  return redirect("/search/")


@login_required
def recommendation(request):
  genre = request.GET.get('genre')
  
  base_query = Q(imdb_rating__gt=5, imdb_votes__gt=1000)
  
  if genre:
    genre_query = Q(genre__icontains=genre)
    movies = Movie.objects.filter(base_query & genre_query)
  else:
    movies = Movie.objects.filter(base_query)
    
  movie_amount = movies.count()
  if (movie_amount > 0):
    index = randint(0, movie_amount - 1)
    movie = movies[index]
    # Pesquisa na API
    omdb_api_key = settings.OMDB_API_KEY
    omdb_url = f"http://www.omdbapi.com/?apikey={omdb_api_key}&t={movie.title}"
    omdb_response = requests.get(omdb_url)
    movie_data = omdb_response.json()
    context = {'movie_data': movie_data}
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
      movie.year = int(movie_data['Year'].split('–')[0])
      movie.end_year = int(movie_data['Year'].split('–')[1])
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
    
  context = {
      'popular_movies': popular_movies,
      'top_rated_movies': top_rated_movies
  }
  return render(request, 'movies.html', context)
  

#def comment(request):
#  if request.method == 'POST':
#    form = CommentsForm(request.POST)
#    if form.is_valid():
#      form.save()
#      return redirect('home')
#  else:
#    form = CommentsForm()
#  return render(request, 'search.html', {'form': form})

def comments(request):
 comments = Comment.objects.all()
 if request.method == 'POST':
   Comment.objects.create(
     comment= request.POST["comment"]
   )
   return redirect('/search/')
 return render(request, 'search.html', context={'comments': comments})
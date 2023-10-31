from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
import requests
from django.conf import settings


def home(request):
  genre = request.GET.get('genre')
  context = {'genre': genre}
  print(genre)
  return render(request, 'home.html', context)

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
      # Retrieve the movie title from the search bar
      movie_title = request.POST.get("search")

      # Make a request to the OMDB API to fetch movie information
      omdb_api_key = settings.OMDB_API_KEY
      omdb_url = f"http://www.omdbapi.com/?apikey={omdb_api_key}&t={movie_title}"
      response = requests.get(omdb_url)
      movie_data = response.json()

      if movie_data.get('Response') == 'False':
          # Movie data not found
          movie_data = {}

      # Pass the movie information to the template for rendering
      context = {'movie_data': movie_data}
      return render(request, 'search.html', context)

  return redirect("home")


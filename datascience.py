from bs4 import BeautifulSoup
import requests
import pandas as pd

# Downloading IMDB feature film and MyAnimeList popularity data
headers = {'Accept-Language': 'en-US,en;q=0.8'}
url1 = 'https://www.imdb.com/search/title/?title_type=feature&sort=num_votes,desc'
url2 = 'https://myanimelist.net/topanime.php?type=bypopularity'
response1 = requests.get(url1,headers=headers)
response2 = requests.get(url2,headers=headers)
soup1 = BeautifulSoup(response1.text, "html.parser")
soup2 = BeautifulSoup(response2.text, "html.parser")

movie_title = []
link = []
year = []
certificate = []
movie_runtime = []
genre = []

anime_title = []
anime_link = []
type = []
anime_runtime = []
members = []



for t in soup1.select('h3.lister-item-header a'):
  movie_title.append(t.get_text())
  link.append("https://www.imdb.com" + t.attrs.get('href') + "?ref_=adv_li_tt")

for t in soup1.select('h3.lister-item-header span.lister-item-year'):
    year.append(t.get_text().replace("(","").replace(")",""))

for t in soup1.select('p.text-muted span.certificate'):
    certificate.append(t.get_text())

for t in soup1.select('p.text-muted span.runtime'):
    movie_runtime.append(t.get_text())

for t in soup1.select('p.text-muted span.genre'):
    genre.append(t.get_text().replace("\n","").replace(" ",""))

for t in soup2.select('h3.anime_ranking_h3 a.hoverinfo_trigger'):
    anime_title.append(t.get_text())
    anime_link.append(t.attrs.get('href'))

for t in soup2.select('div.information'):
    info = t.get_text().strip().split('\n')
    type.append(info[0].strip())
    anime_runtime.append(info[1].strip())
    members.append(info[2].strip())

df1 = pd.DataFrame(
    {'movie title': movie_title,
     'link': link,
     'year': year,
     'certificate': certificate,
     'runtime': movie_runtime,
     'genre': genre}
    )
df2 = pd.DataFrame(
    {'anime title': anime_title,
     'anime link': anime_link,
     'type': type,
     'anime runtime': anime_runtime,
     'members': members}
)

print(df1.head())
print(df2.head())

df1.to_csv('moviesrating.csv', index=False)
df2.to_csv('animerating.csv', index=False)



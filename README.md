# NYC Concerts
A map of  your favorite artists' upcoming concerts. This repo uses the Songkick API with the Spotify API to map concerts in the NYC metro area (localized to myself, but variable). 

1: The python script reads a users Favorite and Followed Artists and writes a csv file of their names (top_artists.csv)

2: The R script gets all the shows in a metro area (NYC) in the next 3 months, keeps only the shows of artists in the csv, and maps them

Make sure to have Spotify, Songkick, and Mapbox tokens- they are all free. 

Resulting map should look like this:
![alt text](https://github.com/david-mateos/NYC_Concerts/blob/master/resulting_map_preview.png?raw=true)

Note: NYC has a lot of shows, in the winter there were over 1700 shows! Pagination of Songkick data could take up 45 seconds depending on the max_date parameter

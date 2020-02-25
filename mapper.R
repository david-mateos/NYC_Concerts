
library(httr)
library(tidyverse)
library(stringi)
library(plotly)

setwd("/Users/davidmateos/Downloads/Concerts-In-My-Area/")
 
# get the metro id for NYC
api_key <<- Sys.getenv("SONGKICK_API_KEY") # your Songkick API key

get_metroID <- function(query){
  
  formatted_query <- gsub(" ", "+", query)
  call <- paste("https://api.songkick.com/api/3.0/search/locations.json?query=",
                formatted_query, "&apikey=", api_key, sep="")
  result <- content(GET(call, accept_json()))
  metroID <- result$resultsPage$results$location[[1]]$metroArea$id
  return(metroID)
  
}

get_dataPage <- function(metroID, min_date, max_date, page){
  call <- paste("https://api.songkick.com/api/3.0/metro_areas/",
                metroID, "/calendar.json",
                "?apikey=", api_key,
                "&min_date=", min_date,
                "&max_date=", max_date,
                "&page=", page,
                sep = "")
  onePage <- content(GET(call, accept_json()))$resultsPage$results$event
  return(onePage)
} 

get_totalEntries <- function(metroID, min_date, max_date){
  call <- paste("https://api.songkick.com/api/3.0/metro_areas/",
                metroID, "/calendar.json",
                "?apikey=", api_key,
                "&min_date=", min_date,
                "&max_date=", max_date,
                sep = "")
  totalEntries <- content(GET(call, accept_json()))$resultsPage$totalEntries
  return(totalEntries)
} 

## get all the concerts in NYC for the next 3 months
metroID <- get_metroID("New York City")
min_date <- Sys.Date()
max_date <- min_date %m+% months(3)
totalConcerts <- get_totalEntries(metroID, min_date, max_date)

i = 1
all_results <- list()
while ((totalConcerts/((i-1)*50)) > 1){
  one_page <- get_dataPage(metroID, min_date, max_date, i)
  all_results <- append(all_results, one_page)
  i= i+1
}

i = 1
artist <- c()
venue <- c()
date <- c()
lat <- c()
lng <- c()

while( totalConcerts >= i ){
  if (all_results[[i]]$type == "Concert"){
    if(is.null(all_results[[i]]$location$lng) == F){
      artist[i] <- all_results[[i]]$performance[[1]]$artist$displayName
      venue[i] <- all_results[[i]]$venue$displayName
      date[i] <- all_results[[i]]$start$date
      lat[i] <- all_results[[i]]$location$lat
      lng[i] <- all_results[[i]]$location$lng
      i= i+1
    }
    else{ i= i+1 }
  }
  else{ i= i+1}
}

all_concerts <- as_tibble(data.frame(artist, venue, date, lat, lng))
all_concerts <- all_concerts %>% 
                    drop_na() %>% 
                    mutate(fdate = format(as.Date(date), "%b %d %Y")) 

# read in my top artists from Python script
top_artists <- read.csv("top_artists.csv", header = F, stringsAsFactors = F)
top_artists <- as_tibble(t(top_artists))
names(top_artists) <- "artist"
### clean artist names before cross checking
top_artists$artist = stri_trans_general(str = top_artists$artist, id = "Latin-ASCII")

# only map concerts from your favorite artists
my_concerts <- all_concerts %>% 
                  inner_join(top_artists) %>% 
                  mutate(fdate = format(as.Date(date), "%b %d %Y")) 
  
# plot it!              
plot_mapbox(my_concerts, x = ~lng, y = ~lat, 
              sizec = 2,
              type = "scattermapbox",
              mode = "markers",
              text= ~paste(artist, venue, fdate, sep = "<br>")) %>%
  layout(plot_bgcolor = '#191A1A', 
         paper_bgcolor = '#191A1A', 
         mapbox = list(zoom = 11,
                       style = 'dark',
                       center = list(lat = ~median(lat),
                                     lon = ~median(lng))
                       )
         ) %>%
  config(mapboxAccessToken = Sys.getenv("MAPBOX_TOKEN")) # only do this once

# Frontend Test Plan
Requirements
- Backend must be running locally on port 5000
- Postgres must be running locally on port 5432

## Testing on-load UI
App should look like below on startup:
![Alt text](/assets/image.png)


## Testing the app ID search functionality

### Correct functionality
- Insert ID "447188370" into the search box and press the Search button
- The app should succesfully load the reviews and look like below
![Alt text](/assets/image-1.png)

### Incorrect functionality
- Insert ID "fake id" into the search box and press the Search button
- App should gracefully handle malformed IDs and look like below:
![Alt text](/assets/image-2.png)

## Testing the filters

### Testing the time filter
- Insert ID "447188370" into the search box and press the Search button
- Given the reviews (which are dynamic), move the day filter to check and see if older reviews are filtered out as you use the slider
- Make sure the text for the filter changes accordingly

### Testing the rating filter
- Insert ID "447188370" into the search box and press the Search button
- Given the ratings (which are dynamic), move the ratings filter to check and see if high rated reviews are filtered out as you use the slider
- Make sure the text for the filter changes accordingly

### Testing reversibility of the filters
We need to make sure that the internal state of the app caches the entire review payload correctly even when filters are set to a subset of the payload
- Before searching, set both the time and rating filters to a level near the middle of the sliders
- Insert ID "447188370" into the search box and press the Search button
- After the reviews populate, move both of the sliders up to the maximum (right-most) value for both sliders. Check that both higher rated reviews and older reviews correctly populate according to the sliders.
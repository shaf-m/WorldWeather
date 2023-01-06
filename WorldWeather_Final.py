#  FINAL VERSION


# Shaf's Weather Widget: WorldWeather
# This program is a widget application that uses web-scraping to obtain weather data based on a user's inputted city.


# Import modules and custom classes
from customDarkButton import *  # Custom class consisting of button for dark mode
from customLightButton import *  # Custom class consisting of button for light mode
from requests_html import HTMLSession  # Essential class for web-scraping requests VIA Google
import emoji  # Pre-created module for emoticon unicode decryption


# the main() function consists of all the application's code, compressed into one function
def main(mode):
    # initialize the background, primary, and secondary colours
    # colours are specified using the RGB format
    # to test colours, copy and paste the RGB colour-code into Google
    backgroundRGB = color_rgb(53, 51, 54)
    primaryRGB = color_rgb(213, 213, 213)
    secondaryRGB = color_rgb(100, 100, 100)

    # if the user selects dark-mode, the following colour-profile is used
    if mode == "dark":
        backgroundRGB = color_rgb(53, 51, 54)
        primaryRGB = color_rgb(213, 213, 213)
        secondaryRGB = color_rgb(100, 100, 100)

    # if the user selects light-mode, the following colour-profile is used
    if mode == "light":
        backgroundRGB = color_rgb(213, 213, 213)
        primaryRGB = color_rgb(71, 71, 71)
        secondaryRGB = color_rgb(156, 156, 156)

    # create a window with width = 300 and height = 300
    win = GraphWin("WorldWeather", 300, 300)
    win.setCoords(0, 0, 300, 300)
    win.setBackground(backgroundRGB)

    # as part the "WorldWeather" logo, the "World" part is created and displayed below
    world_label = Text(Point(95, 190), "World")
    world_label.setSize(30)
    world_label.setFace("helvetica")
    world_label.setFill(secondaryRGB)
    world_label.draw(win)
    # as part the "WorldWeather" logo, the "Weather" part is created and displayed below
    weather_label = Text(Point(191, 190), "Weather")
    weather_label.setSize(30)
    weather_label.setFace("helvetica")
    weather_label.setFill(primaryRGB)
    weather_label.draw(win)

    # an entry box (search-bar) is created to allow for the user to input the city name
    city_entry = Entry(Point(140, 150), 22)
    city_entry.draw(win)
    city_entry.setFill(secondaryRGB)

    # check() verifies the user's input, ensures the user has entered a valid city
    def check():
        while True:
            try:
                pt = win.getMouse()
                while not search_button.clicked(pt):
                    pt = win.getMouse()

                # obtain text input from the search-bar
                user_city = city_entry.getText()
                user_city = user_city.lower()
                city_test = user_city

                # initializes a web-scraping session and opens the URL attached with the user's input
                s_test = HTMLSession()
                url_test = f'https://www.google.com/search?q=weather+{city_test}'
                # bypasses Google's bot verification security measure
                req_test = s_test.get(url_test, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel '
                                                                       'Mac OS X 10_15_7) '
                                                                       'AppleWebKit/537.36 (KHTML, like Gecko) '
                                                                       'Chrome/96.0.4664.93 '
                                                                       'Safari/537.36'})
                # attempts to scrape the current temperature of the user's specified location
                temp_test = req_test.html.find('span#wob_tm', first=True).text

            # an AttributeError occurs if an element is not present on a webpage
            # an AttributeError means the user's input is invalid and the user is prompted to retry input
            except AttributeError:
                # if an AttributeError is raised, an error prompt is displayed to the user
                error_label = Text(Point(137, 110), "Invalid city, try again")
                error_label.setSize(11)
                error_label.setFace("helvetica")
                error_label.setFill(primaryRGB)
                error_label.draw(win)
                # the verification loop continues until the user enters a valid, verified city.
                continue
            else:
                # when a valid, verified city is finally entered,
                # the name of the tested city (city_test) is returned to the main program
                return city_test

    # under the search-bar (input box), the user is prompted to enter the name of the city
    enter_city = Text(Point(135, 125), "Enter City")
    enter_city.setFill(secondaryRGB)
    enter_city.setSize(10)
    enter_city.draw(win)

    # if light mode is selected, the corresponding button for the search (magnifying-glass) icon is created & activated
    if mode == "light":
        search_button = LightButton(win, Point(240, 150), 40, 25, " ")
        search_button.activate()
    # if dark mode is selected, the corresponding button for the search (magnifying-glass) icon is created & activated
    if mode == "dark":
        search_button = DarkButton(win, Point(240, 150), 40, 25, " ")
        search_button.activate()

    # a magnifying-glass icon is created in two parts
    # the circular glass part is created and displayed
    mag_glass = Circle(Point(239, 152), 5)
    mag_glass.setOutline(primaryRGB)
    mag_glass.setWidth(2)
    mag_glass.draw(win)
    # the handle part is created and displayed
    mag_glass_handle = Line(Point(243, 148), Point(250, 142))
    mag_glass_handle.setOutline(primaryRGB)
    mag_glass_handle.setWidth(2)
    mag_glass_handle.draw(win)

    # the verification function is called to validate the user's input
    city_test = check()

    # initializes a web-scraping session and opens the URL attached with the user's input
    s = HTMLSession()
    url = f'https://www.google.com/search?q=weather+{city_test}'
    # bypasses Google's bot verification security measure
    req = s.get(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                                            'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 '
                                            'Safari/537.36'})

    # the current temperature of the user's location is obtained using web-scraping
    temp = req.html.find('span#wob_tm', first=True).text
    # the unit temperature is obtained using web-scraping
    unit = req.html.find('div.vk_bk.wob-unit span.wob_t', first=True).text
    # the current weather description of the user's location is obtained using web-scraping
    desc = req.html.find('span#wob_dc', first=True).text
    # Accounting for longer weather descriptions, shorten length to fit within dimensions
    if "Clear" in desc:
        desc = "Clear"
    if "rain" in desc:
        desc = "Showers"
    # the current probability of precipitation (POP) of the user's location is obtained using web-scraping
    precipitation = req.html.find('div.wtsRwe', first=True).find('span#wob_pp', first=True).text
    # the current humidity level of the user's location is obtained using web-scraping
    humidity = req.html.find('div.wtsRwe', first=True).find('span#wob_hm', first=True).text
    # the current wind-speed of the user's location is obtained using web-scraping
    wind_speed = req.html.find('div.wtsRwe', first=True).find('span#wob_ws', first=True).text
    # the precise location (ie. city, province, state, country, postal code) is obtained using web-scraping
    locationGoogle = req.html.find('div.VQF4g', first=True).find('div.wob_loc', first=True).text
    # the time of data publication by Google is obtained using web-scraping
    time = req.html.find('div.VQF4g', first=True).find('div.wob_dts', first=True).text

    # all obtained data is stored within a 2D array/list
    data = [["Temperature", "POP", "Humidity", "Wind-Speed", "Description"],
            [(temp + unit), precipitation, humidity, wind_speed, desc]]

    # the obtained data, stored in the 2D list/array is displayed neatly in the Python console
    max_number_of_digits = 0
    for row in data:
        for cell in row:
            number_of_digits = len(str(cell))
            if number_of_digits > max_number_of_digits:
                max_number_of_digits = number_of_digits
    print("\n")
    print(' ' * 8, "Weather Data in", locationGoogle.title(), "as of", time)
    for row in data:
        print_row = ''
        for cell in row:
            # fill with space on the left side of the string
            # the padding has to be at least one higher than the max_number_of_digits
            # the higher the number you add, the wider the padding
            print_row += f'{cell}'.center(max_number_of_digits + 3, ' ')
        print(print_row)

    # decide which emoticon to use
    # decision is made based on the obtained weather description.
    # keywords are looked for to aid in decision
    # standard emoticons are used where decryption module fails to operate
    icon = ''
    if desc == "Sunny" or desc == "Clear":
        icon = emoji.emojize(' :sun:')
    if desc == "Fog" or desc == "Haze":
        icon = '🌫'
    if "snow" in desc.lower():
        icon = ' ❄️ '
    if "rain" in desc.lower() or "showers" in desc.lower():
        icon = ' 🌧️'
    if desc == "Partly cloudy" or desc == "Mostly cloudy":
        icon = ' ⛅'
    if desc == "Cloudy":
        icon = '☁️'
    if desc == "Smoke":
        icon = '💨'

    # a new window is created by removing all previous graphical elements on the primary/main screen
    # this is done to accommodate a secondary screen to display all weather information/data
    city_entry.undraw()
    new_win = Rectangle(Point(0, 300), Point(300, 0))
    new_win.setOutline(backgroundRGB)
    new_win.setFill(backgroundRGB)
    new_win.draw(win)

    # the text "Weather in" is displayed
    weather_in = Text(Point(120, 220), "Weather in")
    weather_in.setSize(20)
    weather_in.setFace("helvetica")
    weather_in.setFill(secondaryRGB)
    weather_in.draw(win)

    # the name of the location, as per Google, is displayed
    # depending on the length of the location, the size is altered to accommodate dimensions/formatting
    location = Text(Point(122, 195), locationGoogle.title())
    if len(locationGoogle) > 20:
        location.setSize(11)
    elif len(locationGoogle) > 15:
        location.setSize(16)
    elif len(locationGoogle) > 13:
        location.setSize(18)
    else:
        location.setSize(22)
    location.setFace("helvetica")
    location.setFill(primaryRGB)
    location.draw(win)

    # the current temperature is displayed
    currentTemp = Text(Point(108, 142), str(temp + unit).ljust(5))
    currentTemp.setSize(20)
    currentTemp.setFill(primaryRGB)
    currentTemp.setFace("helvetica")
    currentTemp.draw(win)

    # the current weather description is displayed
    currentDesc = Text(Point(195, 142), desc.rjust(5))
    currentDesc.setSize(18)
    currentDesc.setFill(secondaryRGB)
    currentDesc.setFace("helvetica")
    currentDesc.draw(win)

    # an icon (emoticon) corresponding to the weather description is displayed
    weatherIcon = Text(Point(223, 205), icon)
    weatherIcon.draw(win)
    weatherIcon.setSize(32)

    # all other information (POP, humidity level, and wind-speed) is displayed
    otherInfo = Text(Point(157, 80), ("Chance of precipitation: " + precipitation +
                                      "\n" + "Humidity: " + humidity + "\n"
                                      + "Wind-speed: " + wind_speed).rjust(4))
    otherInfo.setSize(13)
    otherInfo.setFace("helvetica")
    otherInfo.setFill(secondaryRGB)
    otherInfo.draw(win)

    # the data and time of the published weather data, as per Google, is displayed
    dataTime = Text(Point(60, 10), time.center(2))
    dataTime.setSize(11)
    dataTime.setFill(secondaryRGB)
    dataTime.draw(win)

    # the source of data (Google®) is credited
    dataSource = Text(Point(235, 10), "Weather data provided by Google®".rjust(2))
    dataSource.setSize(8)
    dataSource.setFill(secondaryRGB)
    dataSource.draw(win)

    # creates buttons for the user to toggle between light and dark modes while creating a new widget
    # formatting and colours are specified based on the users selection between light and dark mode
    addLightWidget_button = 0  # initialize button
    if mode == "light":
        # create button to switch to create a new widget in light mode
        addLightWidget_button = LightButton(win, Point(30, 280), 40, 25, "+ Light")
        addLightWidget_button.activate()
    if mode == "dark":
        # create button to switch to create a new widget in light mode
        addLightWidget_button = DarkButton(win, Point(30, 280), 40, 25, "+ Light")
        addLightWidget_button.activate()
    addDarkWidget_button = 0  # initialize button
    if mode == "light":
        # create button to switch to create a new widget in dark mode
        addDarkWidget_button = LightButton(win, Point(30, 255), 40, 25, "+ Dark")
        addDarkWidget_button.activate()
    if mode == "dark":
        # create button to switch to create a new widget in dark mode
        addDarkWidget_button = DarkButton(win, Point(30, 255), 40, 25, "+ Dark")
        addDarkWidget_button.activate()

    # a button to close widgets is created
    # formatting and colours are specified based on the users selection between light and dark mode
    quit_button = 0
    if mode == "light":
        # create quit button if user is in light mode
        quit_button = LightButton(win, Point(280, 280), 40, 25, "X")
        quit_button.activate()
    if mode == "dark":
        # create quit button if user is in dark mode
        quit_button = DarkButton(win, Point(280, 280), 40, 25, "X")
        quit_button.activate()

    # obtain the user's mouse click to determine next decision
    pt2 = win.getMouse()

    # if the button to add a widget in dark mode is clicked, then do so
    if addDarkWidget_button.clicked(pt2):
        main("dark")  # rerun the function in dark mode
    # if the button to add a widget in light mode is clicked, then do so
    if addLightWidget_button.clicked(pt2):
        main("light")  # rerun the function in light mode
    # if the button to add close widgets is clicked, then do so
    if quit_button.clicked(pt2):
        win.close()  # conclude program (terminate)


# initially run program in dark mode
# user can toggle between light and dark mode as program progresses (secondary screen)
main("dark")

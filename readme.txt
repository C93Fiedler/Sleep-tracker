This program takes sleep data saved in data\sleep.txt and displays a bar chart of this data. Pygame is required. Written 9th January 2020.




Visual aspects:
The y-axis of the chart is time in hours and the x-axis is day of the month. Gray fill means there is no data, green means time spent awake, blue means time spent sleeping. Note that the days always go to 31 no matter what month is chosen, but those will always remain gray for relevant months. There are horizontal coloured lines that separate each hour. These can be hidden with the "Hide time grid" button in the top right corner, and re-enabled with the same button. Under this button is the current year displayed. If there are entries spanning multiple years, arrows will appear to allow navigation between those years, otherwise there will be no arrows present. List of months is found under the year display; each month can be clicked to navigate to that month. Underneath that is a calendar displaying the days of the month and their corresponding day of the week. Each day can be selected (note: can be selected on the calendar, not on the chart). At the bottom there is a summary of the total time spent asleep and awake for the selected month and the selected day.






Data input:
I have started recording my sleep times before I thought to make this program, that's why some of this seems unnecessary. It is probably easier to see the example file than read this section.

All data needs to be stored in the sleep.txt file in the data folder. There is a file there already with an example. The first line of the file is not read by the program. Each following line should start with:

"a dd/mm/yyyy: "

where "a" can be any string that does not contain a space, "dd" is day, "mm" is 
month and "yyyy" is year. There is no need to include leading zeroes, but it does make reading the file in person more comfortable. The date needs to be followed by a character that is not a space or "/", because the program splits the line where spaces are, and takes the string "dd/mm/yyyy:" and removes the last character. Another space needs to be put after ":", then sleeping/waking up times can be written in. The syntax for this is 

"sleep at hh:mm" 

and 

"woke up hh:mm" 

where "hh" is hour and mm is "minute". The words "at" and "up" are not actually read by the program, but a string needs to be in that place as this is how I recorded this before making the program. Note that 5 minutes represents a height of 1 pixel, so the program only calculates in 5 minute intervals. in principle time can be entered as "1:23" but the program will always round down, in this case to 1:20. Any combination of sleep/woke entries can be made in each line.

For example
"Monday 06/01/2020: sleep at 00:00 woke up 00:05 sleep randomword 00:10 woke anotherword 1:50"
is a valid line. Note that if this line started with "Tuesday 06/01/2020..." the program would still assign this data to monday 1/1/2020 as the first word is not read.

Another example
"Monday 06/01/2020: sleep at 00:00 sleep up 00:05 sleep randomword 00:10 woke anotherword 1:50"
this would still work, but time between 00:00 and 1:50 would count as time spent sleeping.

Note that the dates need to be put in chronologically, with earliest date at the top. Likewise, the change of state (awake/asleep) need to be typed in chronologically, otherwise they will overwrite each other. 

Finally, I assumed I would never not sleep for a whole month (pretty reasonable), so if the file has something like
"a 02/01/2020:...
b 01/03/2020:..."
then the month of February will be empty. Other than that, the program will fill in any days (so if a whole day went by without sleeping it will appear green).




Known issues
 - Currently there is no way to indicate that a day should be left empty (ie. leave a column gray). This was going to be handled in line 200-201. The idea was to add "dd/mm/yyyy 0" to indicate leaving a day not filled in. However I found no need for this as even making a guess that is +/-1 hour of the actual time is better to me than leaving a day off.

 - The totals displayed at the bottom are no truncated, but for my own purposes I saw no need for this. If I were to add some other stats like averages I would probably do that then.
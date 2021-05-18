# Final Report

## Goals and Motivations

This project is an effort to create a publicly accessible digital archive of Williamstown Police Department records. Users will be able to text-search years of police records, including day-to-day logs, incident reports, and arrest and summons reports. Users will also be able to access and download a csv file containing the information from these logs and reports, which can be used in statistical analysis.

We are motivated by the need for immediate police transparency in our community and hundreds of other similarly-sized communities nationwide. We are motivated in particular by the recent history of the Williamstown Police Department. The *Williams Record* provides good coverage of some of the recent events that inspired this work. [This](https://williamsrecord.com/352894/news/lawsuit-brought-by-wpd-sergeant-alleges-sexual-assault-racial-harassment-by-williamstown-police-chief-and-unnamed-officers/) is an excellent starting place.

We conducted interviews with students and community members and identified questions that need to be examined. Key questions include examining police activity by time of day, identifying patterns of activity of individual officers, identifying patterns of police activity at the elementary school, and looking for evidence for the broad reasons for ticket-writing. For more information, please contact Chad Topaz.

We are hopeful that this project will provide inspiration and useful information to others engaging in similar work in other communities. If you are interested in connecting with researchers working on this project, please contact Chad Topaz.

## Materials

For this project, we began with physical documents provided by the Williamstown Police Department. We divided the documents into three different categories: logs, incident reports, and arrests/summons reports.

The logs consisted of short records providing basic information on seemingly every action taken by an officer or dispatcher. They included information such as the date, time, location, the call taker, and in some cases, a short narrative on the events that occured. The events covered by the log included building checks, investigations of suspicious activity, traffic citations, and more.

The incident reports provided more detail on specific events described in some of the logs. They included detailed information on the parties involved such as suspects and victims, if any. Additionally, each log provided a more detailed narrative of the officer's actions compared to the logs. Due to the large level of detail--such as private information like witness names, phone numbers, or addresses--provided in these reports, much of the information provided to us has been redacted. The summons/arrest reports are very similar to those of the incident reports except in these cases, a person has been arrested or will be a defendant in court.

Overall, the logs provide a more holistic view on the actions of the Williamstown Police Department. As a result, the majority of our work so far has been on processing these documents. All of the logs and reports, however, have been scanned as PDF documents for future use and ease of access. 

##Process

## Current State of Things
Currently, we have developed a small set of Python scripts that assist in the processing
of the multiple files in a pipelined fashion. We decided that there were a few separable steps
in which we could interpret our data, and we list them below.

1. Paper to PDF Scanning
2. PDF to Text via OCR
3. Text Cleaning
4. Analysis

First, we scanned in all the physical documents we had for parsing. Then, we utilized the 
Tesseract Open Source OCR Engine to convert all PDFs we had into a text file that we could 
manipulate in code. Since the OCR results were not very clean, we needed another script that 
would clean the text, removing characters that were incorrect and fixing characters that had 
been interpreted incorrectly. These fixes were first identified manually, and then reparied 
using regular expressions and pattern matching. Then, this raw data text was converted into
a Pandas Dataframe so that we could more easily manipulate it. After the dataframe was created,
we were able to perform analysis, such as mapping out the locations, utilizing fuzzy pattern 
matching to search for keywords, and performing elementary data analysis.

## Next Steps

Some possible next steps may include, but are not limited to:
- cleaning some of the data and verifying its legitimacy (the log number and date are not done, status is mostly done, the dispatcher is mostly done, the location data is done) 
- generating the data in a time series (folium has a cloropleth package feature that may be useful, but other programs may be needed)
- create a dashboard where the public can easily view this data and make searches on specific keywords using fuzzy (OIT can likely host the database and the website for users to see)
- try to perform some general statistics on the data (which officers are involved in the most serious logs, where do they occur, are logs distributed evenly or pile up on weekends?)
- Look into potential correlations with the races of police vs those being arrested/cited
- There are a series of questions/notes that we received from DIRE
- get more years' worth of data (hopeful the past 10)

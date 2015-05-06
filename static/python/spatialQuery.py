__author__ = 'Mario'

import psycopg2
import cgi
import cgitb
cgitb.enable()
# https://docs.python.org/2/library/cgi.html info on cgi
# advice on passing value from javascript to python (not sure if even necessary): http://stackoverflow.com/questions/464040/how-are-post-and-get-variables-handled-in-python
try:
    conn = psycopg2.connect("dbname='nyc' user='Mario' host='localhost' password=''")
except:
    print "I am unable to connect to the database"

cur = conn.cursor()

cur.execute("""SELECT SUM(build.calcpop), SUM(build.height_roo) from allcity_buildings as build, welikia_blocks as block
WHERE ST_DWithin(block.geom, 'SRID=4326;POINT(-8231959 4966645)', 0) AND ST_DWithin(block.geom, build.geom, 0)""")

rows = cur.fetchall()
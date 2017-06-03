import time
import os

print(  time.time () )

print ( time.localtime ( time.time()  )   )


print ( time.gmtime ( time.time()  )   )

print( time.tzname )

#print(os.environ['TZ'])

os.environ['TZ'] = 'EET'

print (os.environ['TZ'])

print ( time.asctime (time.localtime ( time.time() )  ) )

# tmprime =

print('hard')

print ( time.asctime ( time.gmtime ( time.time()  )  ) )


print (time.daylight)

#time.tzset()

tmptime = time.gmtime ( time.time() )


print(tmptime)

#tmptime.tm_hour += 3

#print(tmptime)

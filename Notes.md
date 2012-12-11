State: 
 * iterate all bulbs and their state, set back the previous state when setting on/off
 * pulse.py does this to some extent

Timed\Schedule: 
 * fade on to full at 7am.  off at 7:30, on at 3:30, dim at 10, off at 11
 * Handled by fadeon/setlight scripts and cron
 * Pull events from iCal and set state based on them (Automator task?)
 * Suppress events based on iCal (If an all day "vacation" event, don't turn on wake up lights)

Network: 
 * On when iPhone is detected, off when gone
 * watch.py script does this using DHCPMonitor class 

Notification: 
 * Pulse on event (Growl, Mail, etc).  Color based on value (stock, weather, site activity, network usage)
 * Pulsing is easy enough with pulse.py script, but getting apps to send it notifications is nontrivial
 * Colorizing based on some other parameter shouldn't be hard, but requires the rgb->xy algorithm being better understood



phhueapp:// is the Hue (iOS) app's url schema

Resources:
http://www.nerdblog.com/2012/10/a-day-with-philips-hue.html
http://rsmck.co.uk/hue
http://www.everyhue.com/?page_id=38



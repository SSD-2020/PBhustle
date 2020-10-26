 
1. Error 404 : Ramdom URL

2. When Pb Huslte rating is -10000 and open PbHustle

3. Connection Error

4. Api not responding

5. Api taking more time that expected . Connection Time Out ~30seconds.

6. Leaderboard not updating unless user has not updated his ratings.

7. Update Ratings Button

Internal Server Error: /userhome/update/
Traceback (most recent call last):
  File "C:\Users\Sparsh\AppData\Local\Programs\Python\Python37\lib\site-packages\django\core\handlers\exception.py", line 47, in inner
    response = get_response(request)
  File "C:\Users\Sparsh\AppData\Local\Programs\Python\Python37\lib\site-packages\django\core\handlers\base.py", line 179, in _get_response
    response = wrapped_callback(request, *callback_args, **callback_kwargs)
  File "C:\Users\Sparsh\Desktop\PBhustle\PointBlank\CPtracker\views.py", line 163, in update
    return userhome(request)
  File "C:\Users\Sparsh\Desktop\PBhustle\PointBlank\CPtracker\views.py", line 121, in userhome
    PB_rating=ratings['PB']
KeyError: 'PB'
[26/Oct/2020 07:41:12] "GET /userhome/update/ HTTP/1.1" 500 67365
[26/Oct/2020 07:41:39] "GET /userhome/codeforces/ HTTP/1.1" 200 3488546
Internal Server Error: /userhome/
Traceback (most recent call last):
  File "C:\Users\Sparsh\AppData\Local\Programs\Python\Python37\lib\site-packages\django\core\handlers\exception.py", line 47, in inner
    response = get_response(request)
  File "C:\Users\Sparsh\AppData\Local\Programs\Python\Python37\lib\site-packages\django\core\handlers\base.py", line 179, in _get_response
    response = wrapped_callback(request, *callback_args, **callback_kwargs)
  File "C:\Users\Sparsh\Desktop\PBhustle\PointBlank\CPtracker\views.py", line 121, in userhome
    PB_rating=ratings['PB']
KeyError: 'PB'
[26/Oct/2020 07:41:56] "GET /userhome/ HTTP/1.1" 500 64027
Internal Server Error: /userhome/
Traceback (most recent call last):
  File "C:\Users\Sparsh\AppData\Local\Programs\Python\Python37\lib\site-packages\django\core\handlers\exception.py", line 47, in inner
    response = get_response(request)
  File "C:\Users\Sparsh\AppData\Local\Programs\Python\Python37\lib\site-packages\django\core\handlers\base.py", line 179, in _get_response
    response = wrapped_callback(request, *callback_args, **callback_kwargs)
  File "C:\Users\Sparsh\Desktop\PBhustle\PointBlank\CPtracker\views.py", line 121, in userhome
    PB_rating=ratings['PB']
KeyError: 'PB'
[26/Oct/2020 07:42:04] "GET /userhome/ HTTP/1.1" 500 64164
Internal Server Error: /userhome/
Traceback (most recent call last):
  File "C:\Users\Sparsh\AppData\Local\Programs\Python\Python37\lib\site-packages\django\core\handlers\exception.py", line 47, in inner
    response = get_response(request)
  File "C:\Users\Sparsh\AppData\Local\Programs\Python\Python37\lib\site-packages\django\core\handlers\base.py", line 179, in _get_response
    response = wrapped_callback(request, *callback_args, **callback_kwargs)
  File "C:\Users\Sparsh\Desktop\PBhustle\PointBlank\CPtracker\views.py", line 121, in userhome
    PB_rating=ratings['PB']
KeyError: 'PB'
path_wkhtmltopdf_win = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
path_wkhtmltopdf_lin = r'/bin/wkhtmltopdf'  # in docker container

ALL_PORTFOLIOS = 'All_portfolios'


# in filescache.py
TIME_CACHE_USER_PORTFOLIO_DATA = 60 * 3
TIME_CACHES_EXCHANGER_DATA = 60 * 3
TIME_CACHES_BLOCKCHAIN_DATA = 60 * 3

# in templatetags files
TIME_CACHE_ALL_COINS = 60*60*24
TIME_CACHES_DATA = 60*10
TIME_CACHES_COINS = 60*5
TIME_CACHES_USERS = 60

# tasks
FILE_AGE_IN_MINUTES = 60 * 15  # for task core.tasks.del_old_files_in_media_xlsx_files


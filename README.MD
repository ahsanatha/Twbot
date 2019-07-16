# Twbot

Twbot is a web app to manipulate twitter account.

build with Django, Redis, Tweepy and Firebase.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install twbot.

```bash
pip install -r requirements.txt
```
- register to firebase, get the relatime database credentials  [more](https://firebase.google.com/docs/admin/setup) and place it in root folder

- register to twitter developer, and put your consumer key in core/utils.py

- then deploy to heroku [more](https://devcenter.heroku.com/articles/getting-started-with-python?singlepage=true)

- make sure you add heroku add-on called "RedisToGo"

- run this command to open your app 
```bash
heroku open
```

## Functionality

- Delete All your tweets
- [soon](#)


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)

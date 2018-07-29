[![Build Status](https://api.travis-ci.org/dmitrybelyakov/shift-content.svg?branch=master)](https://travis-ci.org/dmitrybelyakov/shift-content)
[![Coverage Status](https://coveralls.io/repos/github/dmitrybelyakov/shift-content/badge.svg?branch=master)](https://coveralls.io/github/dmitrybelyakov/shift-content?branch=master)

# shift-content
Lightweight headless CMF. Not ready for use yet.


## Troubleshooting

### Mysql Unicode Issues

You might run into issues when trying to insert unicode content like this:
```
I can do smilies! 😀
```

Results in an error similar to this:

```
sqlalchemy.exc.OperationalError: (_mysql_exceptions.OperationalError) (1366, 'Incorrect string value: \'\\xF0\\x9F\\x98\\x80"}\'
```

Please make sure your database and python driver are bot set to use `utf8mb4`.

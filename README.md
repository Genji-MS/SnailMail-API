# Snail-Mail-API
![Logo of the project](https://github.com/Genji-MS/SnailMail-API/blob/master/static/Snail_Mail_blueicon_Liz.png)

> Scan Letters or Packages and send the recipient a slack message that they have mail for them.

## Usage

visit https://ms-snailmail.herokuapp.com
call the api with url/api/name%20of%20recipient

Returns JSON:{ 

    'success' true/false :boolean

    'error': null or string (name not found, or other Slack API errors)

    'name': users unformatted slack name (not the string passed into the url)

    'note': null or string (optional notes to the person scanning the mail, EX. 'moved to rm #101')

}

### Fuzzy name search notes:

The API will take the name and remove honorifics, remove accents, sort each name alphabetically and convert the result into a double metaphone. Search the dictionary for the metaphone and return the slack users unique ID if it exists. This is all done to help with small misspellings of a name. We then call the Slack API to send the user a message.

## included scripts and links

Flask https://pypi.org/project/Flask/

Pymongo https://pypi.org/project/pymongo/

Unidecode https://pypi.org/project/Unidecode/

Metaphone https://pypi.org/project/Metaphone/


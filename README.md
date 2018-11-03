## API測試伺服器
- 開始測試伺服器 `python manage.py startserver`
- 測試伺服器 http://localhost:5002

## 如何部署API
- 部署位置有兩個, 1個是192.168.2.52:/BigDataAPI-restful 原始資料
- 第2個是10.132.46.138:/BigDataAPI-restful 展示用

## 更新ＡＰＩ後如何在伺服器上重啟
- 更新之前, 請先在本地端確認52的資料是ＯＫ的, 再更新到102
- `sudo service flask_api restart`

## API在nginx上的設定
- 檔案位置: 192.168.2.124:/etc/nginx/conf.d/locations/api.conf

## tmux 簡易使用方式
- `tmux` 開啟新的session
- `tmux ls` 查看目前所有session
- `tmux attach -t #` 顯示特定session (簡易版指令 `tmux a -t #`)
- `tmux kill-session -t #` 刪除session
- 離開session: 先按`ctrl + b` 再按`d`


# API reponse content-type and 

# Flask REST Template

[![Code Health](https://landscape.io/github/alexandre/flask-rest-template/master/landscape.svg?style=flat)](https://landscape.io/github/alexandre/flask-rest-template/master) 
[![Build Status](https://travis-ci.org/alexandre/flask-rest-template.svg)](https://travis-ci.org/alexandre/flask-rest-template) 
[![Coverage Status](https://coveralls.io/repos/alexandre/flask-rest-template/badge.svg?branch=master)](https://coveralls.io/r/alexandre/flask-rest-template?branch=master)

# About the project (some comments):

The ideia behind the project is to create an useful and simple template for an rest app . Besides the good intentions, I tried to follow some ideas that I've learned. (see "inspirations" item).

I also tried to create useful docstrings and helpers functions. However, I did not create (yet) a documentation based on docstring (e.g. using sphinx), what [IMO] could give an idea about write docs.

Instead to use the default (from stdlib) unittest module, I prefer to use pytest. I hope it can be useful and nice.

## Python version

__Python 3.4.x__

## The module users

This module is a complete CRUD as an example of structure to facilitate a demonstration about write tests (unit and 
integration). In this mock, I used passlib to generate hashs, but just as an example...

## Flask extensions and other components

### Main requirements
* Flask-MongoEngine
* Flask-JWT
* Flask-Restful
* uWSGI

### Testing requirements
* Pytest
* pytest-cov
* pylama

## Alternative to MongoEngine + MongoDB

It's a possible issue/to-do. Create a branch using something like sqlalchemy + postgres...

## How to collaborate

There is a lot of things to do:

* Improving tests and coverage
* Updating the use of third party libs
* Improving this README.md
* Reporting an issue (typo, RFC, other kind of mistake/error)
* Adding a python2 support ( I did not verify it yet)
* and etc

# About the license:

It's a __public domain__ project. =]

# About the inspirations:

* Ideas and answers >> #pocoo IRC channel;
* cookiecutter-flask;
* Flask Snippets;
* Flask-restful-example;
* [What the Flask](http://pythonclub.com.br/tag/what-the-flask.html) a tutorial in portuguese by [Bruno Rocha](https://github.com/rochacbruno)
* Flaskbook by [Miguel Grinberg](https://github.com/miguelgrinberg)
* Some questions in Stack Overflow or tweets that I don't have a link. =P

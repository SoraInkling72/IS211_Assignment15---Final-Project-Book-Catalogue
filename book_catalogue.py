from flask import Flask, request, redirect, render_template, flash, g
import re
import sqlite3

app = Flask(__name__)
app.secret_key = 'sprigatito906'


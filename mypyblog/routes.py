from flask import render_template, flash, redirect, url_for, request, abort
from mypyblog import app, db, bcrypt, mail
from mypyblog.forms import RegistrationaForma, LoginForma, AzurirajProfilForma, PostForma, ResetPasswordForma, ZahtevajResetFormu
from mypyblog.models import Korisnik, Post
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
from PIL import Image
import secrets
import os



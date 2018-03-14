#!/usr/bin/env python
# -*- coding: utf-8 -*-

import strings

from flask_sqlalchemy import SQLAlchemy
from models import MinimumId
from sqlalchemy.sql import func
from models import MinimumId


class Database():

      database = None


      def __init__(self, app):

            app.config['SQLALCHEMY_DATABASE_URI'] = strings.POSTGRESQL_URI
            app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
            self.database = SQLAlchemy(app)


      def get_current_minimum_id(self):
            """
                  Get the minimum id.
                  
                  Return:
                        string: the minimum id stored
            """
            minimum_id = self.database.session.query(MinimumId).first()
            if(not minimum_id):
                  current_minimum_id = 1
                  minimum_id = MinimumId(str(current_minimum_id))
                  self.database.session.add(minimum_id)
                  self.database.session.commit()

            return minimum_id 


      def update_current_minimum_id(self, 
                                    current_minimum_id, 
                                    current_maximum_id):
            """
                  Update the minimum id.
                  
                  Args:
                        current_minimum_id (MinimumId): object of the class 
                        MinimumId.
                        current_maximum_id (int): maximum id from the last 
                        tweets fetching.
                  Return:
                        None
            """
            # updating minimum ID value
            current_minimum_id.value = current_maximum_id
            self.database.session.commit()


      def post_tweet(self, tweet):
            """
                  Save a single tweet on database.

                  Args:
                        tweet (string): text to be saved
                  Return:
                        None
            """
            self.database.session.add(tweet)
            self.database.session.commit()

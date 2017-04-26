# -*- coding: utf-8 -*-
db.define_table('products',
                Field('product_name', requires=IS_NOT_EMPTY()),
                Field('product_description','text',requires=IS_NOT_EMPTY()),
                Field('product_price','double',requires=IS_NOT_EMPTY()),
                Field('product_stock','integer',requires=IS_NOT_EMPTY()),
                Field('product_image','upload',requires=IS_NOT_EMPTY()),
                Field('time_stamp','datetime')
                )

db.define_table('reviews',
                Field('review_name',requires=IS_NOT_EMPTY()),
                Field('review_content','text',requires=IS_NOT_EMPTY()),
                Field('review_rating','integer',requires=IS_NOT_EMPTY()),
                Field('time_stamp','datetime')
                )

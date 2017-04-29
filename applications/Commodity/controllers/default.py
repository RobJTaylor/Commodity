# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------


def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    product = db.products
    productName = product.product_name

    product1Name = ""
    product1URL = ""
    product1Image = ""
    product1Tag1 = ""
    product1Tag2 = ""
    product1Tag3 = ""

    product2Name = ""
    product2URL = ""
    product2Image = ""
    product2Tag1 = ""
    product2Tag2 = ""
    product2Tag3 = ""

    product3Name = ""
    product3URL = ""
    product3Image = ""
    product3Tag1 = ""
    product3Tag2 = ""
    product3Tag3 = ""

    productIDURL = [0] * 4
    reviewerName = [0] * 4
    reviewerID = [0] * 4
    reviewName = [0] * 4
    reviewContent = [0] * 4
    reviewRating = [0] * 4
    reviewTimeStamp = [0] * 4
    reviewerPicture = [0] * 4
    reviewID = [0] * 4
    o = 0

    i = 0
    for row in db().select(db.products.ALL, limitby=(0,3), orderby=~db.products.time_stamp):
        if i == 0:
            product1Name = row.product_name
            product1Image = row.product_image
            product1URL = URL('viewProduct', vars=dict(productID=row.id))
            product1Tag1 = row.tag_1
            product1Tag2 = row.tag_2
            product1Tag3 = row.tag_3
            i = i + 1
        elif i == 1:
            product2Name = row.product_name
            product2Image = row.product_image
            product2URL = URL('viewProduct', vars=dict(productID=row.id))
            product2Tag1 = row.tag_1
            product2Tag2 = row.tag_2
            product2Tag3 = row.tag_3
            i = i + 1
        elif i == 2:
            product3Name = row.product_name
            product3Image = row.product_image
            product3URL = URL('viewProduct', vars=dict(productID=row.id))
            product3Tag1 = row.tag_1
            product3Tag2 = row.tag_2
            product3Tag3 = row.tag_3
            i = i + 1

    loggedIn = 0

    if not auth.is_logged_in():
        loggedIn = 0
    else:
        loggedIn = 1
        db.reviews.reviewer_name.default = auth.user.first_name
        db.reviews.reviewer_id.default = auth.user.id

    for row in db().select(db.reviews.ALL, limitby=(0,4), orderby=~db.reviews.review_rating):
        productIDURL[o] = URL('viewProduct', vars=dict(productID=row.products_id))
        reviewerName[o] = row.reviewer_name
        reviewName[o] = row.review_name
        reviewContent[o] = row.review_content
        reviewRating[o] = row.review_rating
        reviewTimeStamp[o] = row.time_stamp
        reviewID[o] = row.id
        reviewerID[o] = row.reviewer_id
        for row in db(db.auth_user.id == row.reviewer_id).select():
            reviewerPicture[o] = row.profile_image
        o = o + 1
    return locals()

def newProduct():
    form = SQLFORM(db.products).process()
    return locals()

def addRetailer():
    form = SQLFORM(db.retailers).process()
    return locals()

def viewAllProducts():
    rows = db(db.products).select()
    return locals()

def updateProduct():
    from gluon.tools import Crud
    crud = Crud(db)
    form = crud.update(db.products,request.vars.productID)
    return locals()

def viewProduct():
    product = db.products
    productID = product.id
    queryID = request.vars.productID
    query = productID == queryID
    search = db(query)
    rows = search.select()

    name = ""
    image = ""
    description = ""
    price = ""
    tag1 = ""
    tag2 = ""
    tag3 = ""
    timestamp = ""
    i = 0

    for row in rows:
        name = row.product_name
        image = row.product_image
        description = row.product_description
        price = row.product_price
        tag1 = row.tag_1
        tag2 = row.tag_2
        tag3 = row.tag_3
        timestamp = row.time_stamp
    for row in db().select(db.review_rate_link.review_id,db.review_rate_link.user_id):
        i = i + 1

    if i == 0:
        resultsArray = [0] * 1
    else:
        resultsArray = [0] * i

    i = 0

    for row in db().select(db.review_rate_link.review_id,db.review_rate_link.user_id):
        i = i + 1

    reviews = db.reviews
    rProductID = reviews.products_id
    query = rProductID == request.vars.productID
    search = db(query)

    newRows = search.select()

    loggedIn = 0

    if not auth.is_logged_in():
        loggedIn = 0
    else:
        loggedIn = 1
        db.reviews.reviewer_name.default = auth.user.first_name
        db.reviews.reviewer_id.default = auth.user.id

    db.reviews.products_id.default = request.vars.productID
    db.reviews.review_rating.default = 0
    form = SQLFORM(db.reviews).process()

    return locals()

def upvote():
    reviews = db.reviews
    reviewID = reviews.id
    query = reviewID == request.args[0]
    search = db(query)
    rows = search.select()

    for row in rows:
        reviewRating = row.review_rating
        reviewRating = reviewRating + 1
        row.update_record(review_rating=reviewRating)

    reviewID = request.args[0]
    userID = auth.user.id
    db.review_rate_link.insert(user_id=userID,review_id=reviewID)

    for row in db(db.auth_user.id == userID, db.auth_user.reviewer_score).select():
        reviewerScore = row.reviewer_score
        if reviewerScore == None:
            reviewerScore = 0
        reviewerScore = reviewerScore + 1
        row.update_record(reviewer_score=reviewerScore)

    return locals()

def downvote():
    reviews = db.reviews
    reviewID = reviews.id
    query = reviewID == request.args[0]
    search = db(query)
    rows = search.select()

    for row in rows:
        reviewRating = row.review_rating
        reviewRating = reviewRating - 1
        row.update_record(review_rating=reviewRating)

    reviewID = request.args[0]
    userID = auth.user.id
    db.review_rate_link.insert(user_id=userID,review_id=reviewID)

    for row in db(db.auth_user.id == userID, db.auth_user.reviewer_score).select():
        reviewerScore = row.reviewer_score
        if reviewerScore == None:
            reviewerScore = 0
        reviewerScore = reviewerScore - 1
        row.update_record(reviewer_score=reviewerScore)

    return locals()

def searchProduct():
    form = FORM('',
              DIV(LABEL('Product Name:',_class='control-label col-sm-3'),
                  DIV(INPUT(_name='productName', _class='form-control string'),
                      _class='col-sm-9'), _class='form-group'),

              DIV(LABEL('Product Tag:',_class='control-label col-sm-3'),
                  DIV(INPUT(_name='tagOne', _class='form-control string'),
                      _class='col-sm-9'), _class='form-group'),

              DIV(LABEL('Product Tag:',_class='control-label col-sm-3'),
                  DIV(INPUT(_name='tagTwo', _class='form-control string'),
                      _class='col-sm-9'), _class='form-group'),

              DIV(LABEL('Product Tag:',_class='control-label col-sm-3'),
                  DIV(INPUT(_name='tagThree', _class='form-control string'),
                      _class='col-sm-9'), _class='form-group'),

              DIV(DIV(INPUT(_type='submit', _class="btn btn-primary"),
                      _class='col-sm-9 col-sm-offset-3'), _class='form-group'))
    if form.accepts(request,session):
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill the form'

    searchCheck = False
    if request.vars:
        statementBuild = ""
        searchProductName = request.vars.productName
        if searchProductName == None:
            searchProductName = ""
        searchProductName = "%" + searchProductName + "%"

        searchTagOne = request.vars.tagOne
        if searchTagOne == None:
            searchTagOne = ""
        searchTagOne = "%" + searchTagOne + "%"

        searchTagTwo = request.vars.tagTwo
        if searchTagTwo == None:
            searchTagTwo = ""
        searchTagTwo = "%" + searchTagTwo + "%"

        searchTagThree = request.vars.tagThree
        if searchTagThree == None:
            searchTagThree = ""
        searchTagThree = "%" + searchTagThree + "%"

        i = 0
        for row in db(db.products.product_name.like(searchProductName) and
                     db.products.tag_1.like(searchTagOne) and
                     db.products.tag_2.like(searchTagTwo) and
                     db.products.tag_3.like(searchTagThree)).select(db.products.ALL):
            i = i + 1
        productName = [0] * i
        productDescription = [0] * i
        productImage = [0] * i
        productPrice = [0] * i
        productTag1 = [0] * i
        productTag2 = [0] * i
        productTag3 = [0] * i
        ProductTimeStamp = [0] * i
        i = 0
        for row in db(db.products.product_name.like(searchProductName) and
                     db.products.tag_1.like(searchTagOne) and
                     db.products.tag_2.like(searchTagTwo) and
                     db.products.tag_3.like(searchTagThree)).select(db.products.ALL):
            productName [i] = row.product_name
            productDescription [i] = row.product_description
            productImage [i] = row.product_image
            productPrice [i] = row.product_price
            productTag1 [i] = row.tag_1
            productTag2 [i] = row.tag_2
            productTag3 [i] = row.tag_3
            ProductTimeStamp [i] = row.time_stamp
            i = i + 1
        searchCheck = True

    return locals()

def getReviews():
    userID = request.args[0]
    userName = request.args[1]

    review = db.reviews
    reviewID = review.reviewer_id
    query = reviewID == userID
    search = db(query)
    rows = search.select()

    return locals()

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()

l=[]
        for x in no:
            v=request.POST.getlist(x,None)
            l.append(v)    
        #To insert the documents starts
        doc={
        'userid':request.user.id,
        'l':l,
        'lenofqut':lenofqut,
        'lenofqu':lenofqu,
        'questiont':questiont,
        'answer':answer,
        'tp':tp,
        'question':question,
        'typee':typee,
        'option1':option1,
        'option2':option2,
        'option3':option3,
        'option4':option4}
        # docin=collection.insert_one(doc)    #Insert only one data in collection
        # lastinsrt=docin.inserted_id    #Getting id of inserted data
        # print(lastinsrt)
        # To insert the documents end
        filter={"_id":ObjectId('6088f436349987657e800fd2')}
        cursor=collection.find(filter)
        print(cursor.count())
        
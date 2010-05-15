def create_table():
    form = FORM(TABLE(
            TR('Table Name: ', INPUT(_type='text', _name='name', _size=80)),
            TR('Table Definition: ', TEXTAREA(_type='text', _name='definition')),
            TR('', INPUT(_type='submit', _name='Submit'))))
    if form.accepts(request.vars, session):
        pass
    return dict(form=form)
    
def list_table():
    pass
    

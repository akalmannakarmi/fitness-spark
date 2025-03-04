from bson import ObjectId

class User():
    _id: ObjectId
    username: str
    email: str
    password: str

    def __init__(self,_id,username,email,password):
        self._id =_id
        self.username =username
        self.email =email
        self.password =password
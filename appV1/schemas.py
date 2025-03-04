from pydantic import BaseModel, field_validator, model_validator

class SignupModel(BaseModel):
    username:str
    email:str
    password:str

    @field_validator("username")
    @classmethod
    def username_check(cls,value:str)->str:
        if len(value) < 4:
            raise ValueError("Username must be atleast 4 character.")
        return value

class LoginModel(BaseModel):
    email:str
    password:str
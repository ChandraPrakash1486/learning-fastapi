from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

print("Admin Hash:", pwd_context.hash("iamadmin112"))
print("Guest Hash:", pwd_context.hash("guest123"))
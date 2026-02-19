contact_info ={"Reina": "123-234",
             "Festa": "534-343"
}

reina_phone = contact_info["Reina"]
print(reina_phone)

contact_info["Reina"]= "444-444"
print(contact_info)

contact_info["Renato"]= "111-111"
print(contact_info)

del contact_info["Renato"]
print(contact_info)

keys = contact_info.keys()
print(keys)

values = contact_info.values()
print(values)

items = contact_info.items()
print(items)

contact_information = {

    "Festa":{
        "phone_number" : "123-456",
        "email" : "festa@gmail.com",
        "home_address" : "Bregu i Diellit",
        "birthday" : "03/02/2003"
    },

    "Sara": {
        "phone_number": "123-123",
        "email": "sara@gmail.com",
        "home_address": "Bregu i Diellit",
        "birthday": "24/12/2007"
    },

    "Liron": {
        "phone_number": "111-123",
        "email": "liron@gmail.com",
        "home_address": "Bregu i Diellit",
        "birthday": "01/04/2008"
    }
}

print(contact_information)

sara_information = contact_information["Sara"]
print(sara_information)

contacts = {

    "Festa":("123-456", "festa@gmail.com" ),
    "Sara":("123-123", "sara@gmail.com" ),
    "Liron":("111-123", "liron@gmail.com" )
}

festa_info = contacts["Festa"]
phone_number = festa_info[0]
print(phone_number)
email = festa_info[1]
print(email)


phone_number , email = contacts["Festa"]

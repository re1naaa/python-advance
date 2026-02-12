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
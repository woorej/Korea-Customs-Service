# Data Handler from AI task organized by Korea Customs Service

## Target data
- Use
    - you should make a list
    - example
```
want_lists = ["Filename", "RegisteredNumber"]

for want_list in want_lists :
    result.append(DataHandler.get_item(want_list))
```

## Data split
- Use
    - example
        - split=True
- Not Use
    - example
        - split=False
```
want_lists = ["Filename", "RegisteredNumber"]

for want_list in want_lists :
    result.append(DataHandler.get_item(want_list), split=True)
```

## View point
- Use
    - example
        - view_point = [60, 90]
- Not Use
    - example
        - view_point = False
if you want split data from view_point condition, then give split=True
```
want_lists = ["Filename", "RegisteredNumber"]

for want_list in want_lists :
    result.append(DataHandler.get_item(want_list, split=False, view_point=[60, 90]))
```


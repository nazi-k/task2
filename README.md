## Task 2

В нас є HTMl сторінка. Відомо, що можуть бути тільки парні HTML теги.
Завдання: знайти всі незакриті теги.

### Приклад:
```
<body>
<div>Some text
<div>Some text2
<div><div>Lorem</div></div>
</body>
```
Результат:
```["body.div[0]", "body.div[1]"]```
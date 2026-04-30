# Lexium

Lexium is a simple scripting language built in Python.
It is designed to be easy to learn and powerful enough to create small games and logic-based programs.

---

## ✨ Features

* Variables and expressions
* Functions with return values
* Object system (`enemy.hp`)
* Control flow (`if`, `repeat`)
* Game-style scripting

---

## 📦 Installation

Make sure you have Python installed.

Clone this repository or download the files.

---

## ▶️ How to Run

```bash
python lexium.py example.lx
```

---

## 🧪 Example

```lx
spawn enemy

func damage target:
    target.hp = target.hp - 20
    return target.hp

say damage enemy
```

### Output

```
enemy spawned
80
```

---

## 🧠 Basic Syntax

### Variables

```lx
let x = 10
say x
```

### Functions

```lx
func add a b:
    return a + b

say add 5 5
```

### Conditions

```lx
if x > 5:
    say x
```

### Loops

```lx
repeat 3:
    say 1
```

---

## 🎮 Example Use Case

Lexium can be used to simulate simple game logic:

```lx
spawn enemy

repeat 3:
    attack enemy
    say enemy.hp
```

---

## 🚀 Future Plans

* Input system
* Better expression handling
* GUI / game integration
* VS Code support

---

## 📌 About

Lexium is a custom-built programming language created as a learning project to understand how interpreters and scripting systems work.

---

## 📄 License

Free to use and modify.

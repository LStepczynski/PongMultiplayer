class test:
    def __init__(self) -> None:
        self.s = 1


awd = ["siema"]
print(awd)
awd.append('123')
print(awd)
awd.append(test())
print(awd)